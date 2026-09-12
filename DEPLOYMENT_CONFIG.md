# DEPLOYMENT_CONFIG

Production configuration reference for SITREP: what is deployed, which variables it reads,
and the commands and failure modes that come up day to day. Setup steps live in
[DEPLOYMENT.md](DEPLOYMENT.md).

| | |
| --- | --- |
| API | **https://sitrep-production-6aac.up.railway.app** - v0.21.11 |
| Web app | **https://pcschmidt.github.io/sitrep/** - published from the portfolio repo, not this one |
| Schedule | In-app APScheduler daily 06:00 UTC (`api/scheduler.py`, `CronTrigger(hour=6)`), plus a 07:00 UTC Actions backup |
| Runbook | [DEPLOYMENT.md](DEPLOYMENT.md) |

Updated: 2026-09-12.

## Architecture

```
Mobile (React Native + Expo)      Web (Expo web export, GitHub Pages)
        \                                   /
         \                                 /
          HTTPS  ->  Railway (FastAPI, Docker, uvicorn)
                          |
                          |  briefings (upsert by desk)
                          v
                     Supabase Postgres
        ^
        |  daily 06:00 UTC in-app APScheduler
        |  07:00 UTC GitHub Actions backup if today's briefing is missing
        |
Playwright + RSS/httpx + Guardian API + GDELT -> model waterfall -> 4 desks + composite Global -> PDF on demand
```

## Railway (backend)

Dashboard: railway.app, SITREP project.

| Service | Type | Status |
| --- | --- | --- |
| SITREP | Web (Docker) | Running - hosts the API and the in-app daily scheduler |
| humorous-manifestation | Cron | Legacy and redundant; safe to remove |

### Environment variables

Set in the Railway dashboard under Service, Variables.

| Variable | Required | Value |
| --- | --- | --- |
| `OPENROUTER_API_KEY` | yes | `sk-or-...`, model access for synthesis |
| `SUPABASE_URL` | yes | `https://<project>.supabase.co` |
| `SUPABASE_SERVICE_KEY` | yes | new-format secret key, `sb_secret_...`; writes bypass RLS |
| `SUPABASE_KEY` | no | publishable/anon key; local read fallback only |
| `GUARDIAN_API_KEY` | no | enables the Guardian Content API scraper |
| `SITREP_ADMIN_TOKEN` | no | when set, write and debug routes require `X-Admin-Token` |

Do not downgrade the Supabase client. `api/requirements.txt` pins `supabase==2.31.0`;
2.9.0 rejects new-format `sb_secret_...` keys with "Invalid API key" and 2.16.0 is the
first release that accepts them.

### Deployment

- Trigger: any push to `main`, or any change to a service variable.
- Build recipe in the repo: root `Dockerfile` (python:3.11-slim,
  `pip install -r api/requirements.txt`, `playwright install chromium`). The root
  `nixpacks.toml` and `api/railway.toml` are older Nixpacks variants; `railway.toml` was
  removed on 2026-05-26 so the Dockerfile start command wins. Check the Railway service
  settings before changing how the container starts.
- Start: `uvicorn main:app --host 0.0.0.0 --port 8080` in the Dockerfile, or
  `cd api && uvicorn main:app --host 0.0.0.0 --port $PORT` in the Nixpacks variants.
- Health check: `GET /health` returns `{"status":"ok"}` and the real version (it used to
  hardcode `0.10.0`; fixed 2026-09-12). `/` and `/openapi.json` report the same value.
- Logs: Railway dashboard, Service, Logs.

A redeploy no longer loses briefings - they live in Supabase - and PDFs regenerate on
demand. It does mean a short warm-up and a slower first PDF request.

### Manual pipeline trigger

```bash
curl -X POST https://sitrep-production-6aac.up.railway.app/pipeline/run-weekly \
  --max-time 10
# add -H "X-Admin-Token: $SITREP_ADMIN_TOKEN" only after the Railway variable is set
```

Or from the repo root:

```bash
SITREP_ADMIN_TOKEN=... python refresh_railway_briefings.py --timeout 1500
```

The run takes about 20 minutes. The client is expected to time out; the server finishes.

## Supabase (database)

Dashboard: supabase.com, `sitrep-production`.

| Table | Purpose |
| --- | --- |
| `briefings` | One row per desk (four regional rows plus the Global row), `briefing_data` as JSONB |

- RLS is enabled on `briefings`. Writes need the service key: with the publishable key,
  inserts fail with `42501 new row violates row-level security policy`, and the pipeline
  still reports success because file storage hides the failure.
- `GET /debug/supabase` reports `storage`, `key_role`, `client_initialized`, and
  `briefings_count`. Expect `key_role: service_role` and `briefings_count: 4` (the count
  covers only the four regional rows; the Global briefing is not counted).
- Pools: port 6543 for the pooler, 5432 for direct work.
- Fallback: `data/briefings/*.json` on the container disk is a read fallback for the PDF
  route, not a store. The container filesystem is ephemeral, so anything that exists only
  on disk is gone at the next redeploy.

## OpenRouter (LLM)

Dashboard: openrouter.ai, API Keys.

| Order | Model | Stated cost per briefing |
| --- | --- | --- |
| 1 | `deepseek/deepseek-v4-flash` | ~$0.001 |
| 2 | `deepseek/deepseek-v3.2` | ~$0.003 |
| 3 | `moonshotai/kimi-k2.5` | ~$0.009 |

Cost ceiling: $20/month. With one run a day, five briefings (four desks plus Global) at
about $0.001 each is roughly $0.15/month of model usage. Empty-content responses, rate
limits, and credit failures fall through to the next model, and the model that wrote the
briefing is recorded in `metadata.model_used`.

## Expo / mobile app

Expo SDK ~56.0.8, React Native 0.85.3, React 19.2.3, expo-router ~56.2.8. `app.json`
version 1.0.0, Android package `com.pcschmidt.sitrep` versionCode 7, iOS bundle
`com.pcschmidt.sitrep`.

### Development build on a physical device

```bash
# Terminal 1 - ADB port forward (USB connected)
"C:/Users/pchri/AppData/Local/Android/Sdk/platform-tools/adb.exe" reverse tcp:8081 tcp:8081

# Terminal 2 - Metro bundler
cd mobile
npx expo start

# On the device - open SITREP, then exp://localhost:8081
```

### Rebuild the dev build after adding native modules

```bash
cd mobile
npx expo run:android        # ~10 minutes
```

### Production builds

```bash
cd mobile
npx eas build --profile production    # Android AAB, used for the Play Store submission
npx eas build --platform ios --profile production
```

EAS project id: `c0284b13-8077-4be7-acc5-e0cafbf0f3e2`.

### Analytics tokens

Set in `mobile/.env.local` (git-ignored) for local runs; the values are also pinned in
`mobile/eas.json` for builds.

```
EXPO_PUBLIC_MIXPANEL_TOKEN=<mixpanel.com -> Project Settings -> Token>
EXPO_PUBLIC_SENTRY_DSN=<sentry.io -> Project -> Client Keys -> DSN>
```

### Web export

The web app is not published from this repo. The portfolio repo
(`C:/Dev/AIEngineeringProjects/PCSchmidt.github.io/PCSchmidt.github.io`) builds the SITREP
Expo web export into its `public/sitrep/` on push to its `master` branch. Pushes to SITREP
`main` only redeploy the Railway container.

## GitHub

Repository: github.com/PCSchmidt/SITREP.

| Branch | Role |
| --- | --- |
| `main` | production; every push redeploys the Railway container |

The commit-msg hook that strips `Co-Authored-By` lines is installed from
`.claude/hooks/strip-coauthor.sh` (run it from the repo root). It is not installed in a
fresh clone - check for `.git/hooks/commit-msg`.

## Pre-deploy checklist

- [ ] `git status` clean.
- [ ] `cd api && pytest tests -q` - 11 passing. Pass `tests` explicitly: a bare
      `python -m pytest` from `api/` also collects `api/scripts/test_*.py`.
- [ ] `npx tsc --noEmit` clean in `mobile/`.
- [ ] `OPENROUTER_API_KEY`, `SUPABASE_URL`, and `SUPABASE_SERVICE_KEY` set on Railway.
- [ ] `curl https://sitrep-production-6aac.up.railway.app/health` returns `{"status":"ok"}`.
- [ ] `key_role` on `/debug/supabase` reads `service_role`.

## Common failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| Missing or wrong Supabase key | `42501 new row violates row-level security policy` | Set `SUPABASE_SERVICE_KEY` to the secret key, not the publishable key |
| Old Supabase client | `Invalid API key` with an `sb_secret_...` key | Keep `supabase==2.31.0` in `api/requirements.txt` |
| Playwright not installed | `browserType.launch: Executable doesn't exist` | The Dockerfile runs `playwright install chromium`; rebuild |
| Wrong working directory | `FileNotFoundError: data/briefings` | Run uvicorn and scripts from `api/` |
| OpenRouter 401 | `Authentication failed` | Check `OPENROUTER_API_KEY` |
| PDF served as a download | Web PDF screen stuck on "Loading PDF..." | Confirm `Content-Disposition: inline` on `/briefing/latest/pdf` |
| GDELT rate limited | 0 articles from the GDELT scraper | Expected after heavy use; retry on the next run |
| Stale code after an edit | `assert 'Europe' == 'Europe/Africa'` | Restart the local uvicorn server |

## Static values

```
BACKEND_URL:       https://sitrep-production-6aac.up.railway.app
WEB_URL:           https://pcschmidt.github.io/sitrep/
LEGAL_URLS:        https://pcschmidt.github.io/sitrep/privacy-policy | .../sitrep/terms
BUNDLE_ID (iOS):   com.pcschmidt.sitrep
PACKAGE (Android): com.pcschmidt.sitrep  (versionCode 7)
EAS_PROJECT_ID:    c0284b13-8077-4be7-acc5-e0cafbf0f3e2
SCHEDULE:          daily 06:00 UTC (in-app APScheduler CronTrigger(hour=6))
PYTHON_VERSION:    3.11
API_VERSION:       0.21.11
```

## See also

- [README.md](README.md) - what SITREP is and how to run it locally.
- [DEPLOYMENT.md](DEPLOYMENT.md) - setup steps and the deploy runbook.
- [mobile/README.md](mobile/README.md) - the mobile and web client.
- [api/SETUP_OPENROUTER.md](api/SETUP_OPENROUTER.md) - model access setup.
