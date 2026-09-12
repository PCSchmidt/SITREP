# DEPLOYMENT

Setup and runbook for the SITREP production stack: the Railway API, the Supabase data
store, and the GitHub Pages web export. Companion reference for variables and day-to-day
commands: [DEPLOYMENT_CONFIG.md](DEPLOYMENT_CONFIG.md).

| | |
| --- | --- |
| API | **https://sitrep-production-6aac.up.railway.app** - Railway, Docker, `uvicorn main:app` + FastAPI, v0.21.10 |
| Web app | **https://pcschmidt.github.io/sitrep/** - Expo web export, built by the portfolio repo's workflow, not by this repo |
| Data store | Supabase Postgres; briefings survive redeploys, PDFs are regenerated on demand |
| Schedule | In-app APScheduler daily at 06:00 UTC, plus a 07:00 UTC GitHub Actions backup trigger |
| Tests | `cd api && pytest tests -q` - 11 passing, offline, no keys needed |

Verified 2026-09-12: the four regional briefings, the composite Global briefing, and all
five PDFs return `200` from the production API.

## What runs where

| Piece | Host | Built from |
| --- | --- | --- |
| API + scheduler | Railway, Docker build (the repo also carries `nixpacks.toml` and `api/railway.toml` Nixpacks variants) | root `Dockerfile`, `api/` code, `uvicorn main:app` |
| Briefing storage | Supabase Postgres, `briefings` table | written by `api/database/supabase_client.py` |
| PDFs | Railway container disk cache | `api/pdf_generation/pdf_generator_v3.py`, rebuilt on demand |
| Web app | GitHub Pages | the portfolio repo exports `mobile/` and publishes to `public/sitrep/` |
| Mobile app | Google Play / App Store (in progress) | EAS build of `mobile/` |

## Prerequisites

- A Railway account and the SITREP project.
- A Supabase account with the `sitrep-production` project.
- An OpenRouter API key.
- The repo pushed to GitHub (`PCSchmidt/SITREP`).

## Step 1 - Create the Supabase project

1. Create a project named `sitrep-production` and save the database password.
2. Open the SQL Editor and run:

```sql
-- Briefings table: one row per desk, upserted by region
CREATE TABLE briefings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  region TEXT NOT NULL,
  briefing_data JSONB NOT NULL,
  pdf_url TEXT,
  generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_briefings_region ON briefings(region);
CREATE INDEX idx_briefings_generated_at ON briefings(generated_at DESC);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_briefings_updated_at
    BEFORE UPDATE ON briefings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

`pdf_url` is a legacy column: PDFs are no longer stored anywhere, so the backend leaves
it empty. Keep the column, or drop it, but do not build on it.

3. From Project Settings, note the project URL and, under API keys, the secret key.

## Step 2 - Deploy the Railway service

1. Railway dashboard, New Project, Deploy from GitHub repo, select `SITREP`.
2. Leave the root directory at the repo root. The root `Dockerfile` copies `api/`,
   installs Playwright Chromium into the image, and starts uvicorn on port 8080.
3. Add the service variables below, then let Railway redeploy.
4. Under Settings, Networking, click Generate Domain. The domain in use is
   `sitrep-production-6aac.up.railway.app`.

| Variable | Required | Purpose |
| --- | --- | --- |
| `OPENROUTER_API_KEY` | yes | model access for synthesis |
| `SUPABASE_URL` | yes | Supabase project URL |
| `SUPABASE_SERVICE_KEY` | yes | writes; new-format secret key `sb_secret_...` |
| `SUPABASE_KEY` | no | publishable/anon key; local fallback only |
| `GUARDIAN_API_KEY` | no | enables the Guardian scraper (14th source) |
| `SITREP_ADMIN_TOKEN` | no | when set, write/debug routes require `X-Admin-Token` |

**Writes need the service key.** With the publishable key, inserts fail with
`42501 new row violates row-level security policy`, and the pipeline still reports
success because file storage hides the failure. `GET /debug/supabase` reports `key_role`;
it must read `service_role`.

**The Supabase client must be 2.16.0 or newer.** `supabase-py` 2.9.0 rejects new-format
`sb_secret_...` keys with "Invalid API key". `api/requirements.txt` pins
`supabase==2.31.0`; do not downgrade it.

## Step 3 - Confirm the deployment

```bash
# health
curl https://sitrep-production-6aac.up.railway.app/health          # {"status":"ok"}

# version and scheduler
curl https://sitrep-production-6aac.up.railway.app/               # v0.21.10

# which Supabase key is in use, and how many regional briefings are stored
curl https://sitrep-production-6aac.up.railway.app/debug/supabase
```

`/health` used to return a hardcoded `0.10.0`; it now returns `APP_VERSION` (fixed
2026-09-12), so `/health`, `/`, and `/openapi.json` agree on the running version. `/debug/supabase` counts only the four regional rows, so
`briefings_count: 4` is the expected value even though a Global briefing also exists.

## Step 4 - Trigger a run

```bash
curl -X POST https://sitrep-production-6aac.up.railway.app/pipeline/run-weekly --max-time 10
```

The run scrapes 13 sources by default (14 with `GUARDIAN_API_KEY`), synthesizes four
regional desks, then stitches the composite Global briefing. It takes about 20 minutes; the client is expected to time out while the
server finishes. A second request while a run is in progress is refused. Startup does not
run the pipeline.

To check the result, read a desk and look at `generated_at`:

```bash
curl -s -G https://sitrep-production-6aac.up.railway.app/briefing/latest \
  --data-urlencode "region=Middle East"
```

## Step 5 - Scheduling

Scheduling lives inside the API. `api/scheduler.py` starts an APScheduler job at app
startup with `CronTrigger(hour=6, minute=0, timezone="UTC")` and POSTs the pipeline
endpoint. No separate Railway cron service is needed; a standalone cron service would
duplicate the run.

Because the in-app job only fires if the container is alive at 06:00 UTC,
`.github/workflows/daily-briefing.yml` is an independent backup: at 07:00 UTC it checks
whether today's briefing already exists and triggers the pipeline only if it is stale.

## Step 6 - Admin token guard (opt-in)

Every write route - `/scrape`, `/synthesize`, `/synthesize/global`,
`/briefing/generate-pdf`, `/pipeline/run-weekly`, `/debug/supabase`,
`/debug/upload-briefing` - accepts an optional `X-Admin-Token` header. Enforcement is
opt-in through the `SITREP_ADMIN_TOKEN` variable.

`SITREP_ADMIN_TOKEN` is **not set in production today**, so those routes are
unauthenticated and the guard logs a warning per request. To turn the guard on:

1. Generate a value, for example `openssl rand -hex 32`.
2. Set it on Railway and redeploy.
3. Send it from every caller: the in-app scheduler reads the variable from the
   environment; `refresh_railway_briefings.py` sends it when the variable or `--token` is
   set; the GitHub Actions workflow sends it when the `SITREP_ADMIN_TOKEN` repository
   secret exists.

Read routes stay public because the mobile app needs them: `/`, `/health`,
`/briefing/latest`, `/briefing/global`, `/briefing/latest/pdf`.

## Step 7 - PDFs

`GET /briefing/latest/pdf` is the only PDF route the app calls. It loads the newest
briefing for the desk (Supabase first, `data/briefings/*.json` fallback), regenerates the
PDF when the cached file is missing or older than the briefing's `generated_at`, caches it
to `data/pdfs/{slug}_{YYYY-MM-DD}.pdf`, and returns it with
`Content-Disposition: inline`. Inline matters: an attachment disposition made browsers
download the file instead of rendering it in the web iframe, which left the web PDF screen
stuck on its loading spinner.

The cache lives on the container disk, so a redeploy drops it. That is expected: the next
request rebuilds the PDF. There is no object-storage archive yet.

## Step 8 - Mobile and web

The mobile client points at the production API in `mobile/api/client.ts`:

```typescript
const API_BASE_URL = 'https://sitrep-production-6aac.up.railway.app';
```

The web app is published from the portfolio repo, not this one. Pushes to SITREP `main`
do not update https://pcschmidt.github.io/sitrep/. That repo's
`.github/workflows/deploy.yml` runs on push to its `master`, builds the SITREP Expo web
export into `public/sitrep/`, and leaves `public/sitrep/privacy-policy.html` and
`public/sitrep/terms.html` alone. `public/404.html` forwards `/sitrep/` deep links to
`/sitrep/?redirect=...`, which the app root layout follows.

To redeploy the web app without changing code, run that workflow manually: GitHub, the
portfolio repo, Actions, "Deploy Astro site to GitHub Pages", Run workflow. The build step
it performs is:

```bash
# portfolio repo working copy, after checking out PCSchmidt/SITREP into sitrep-src/
cd sitrep-src/mobile
npm ci --no-audit --no-fund
npx expo export --platform web --output-dir "$GITHUB_WORKSPACE/sitrep-web"
# then copy the export into public/sitrep/, replacing only app-owned files
```

`mobile/app.json` sets `experiments.baseUrl` to `/sitrep`, so the exported asset URLs
resolve under the subpath the site serves.

## Local run

Backend:

```bash
cd api
python -m venv venv
venv\Scripts\activate            # Windows; source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
cp .env.example .env             # then fill in the keys
uvicorn main:app --reload        # http://localhost:8000/docs
```

Mobile and web:

```bash
cd mobile
npm install
npx expo start                   # then: i (iOS), a (Android), w (web)
```

## Redeploys

Any push to `main` restarts the container, and so does any Railway variable change.
That used to wipe the briefings and break the PDFs. It no longer does, because briefings
live in Supabase and PDFs regenerate on demand; expect a short warm-up and a slower first
PDF request after a restart. Do not re-run the pipeline just because the container
restarted.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Writes fail with `42501 new row violates row-level security policy` | `SUPABASE_SERVICE_KEY` missing or set to the publishable key | Set the secret key; check `key_role: service_role` on `/debug/supabase` |
| `Invalid API key` on startup | `supabase-py` older than 2.16.0 cannot read `sb_secret_...` keys | Keep `supabase==2.31.0` in `api/requirements.txt` |
| PDF request returns `404` | No briefing and no cached PDF for that desk | Run the pipeline, then retry; `/briefing/latest` should return data first |
| PDF screen stuck on "Loading PDF..." | PDF served as an attachment, or an old cached file | Confirm `Content-Disposition: inline`; the web viewer also clears itself after 6 seconds |
| `browserType.launch: Executable doesn't exist` | Playwright Chromium missing from the image | The root `Dockerfile` runs `playwright install chromium`; rebuild |
| `FileNotFoundError: data/briefings` | Command run from the repo root instead of `api/` | Run uvicorn and scripts from `api/` |
| Scheduler "not initialized" in `GET /` | The startup hook failed | Check the service logs, then restart the service |
| Blank desk in the app after a redeploy | Briefing missing from Supabase and from disk | Confirm the service key, re-run the pipeline |

## Cost

| Item | Cost |
| --- | --- |
| Railway | $5/month (Hobby plan, 500 hours) |
| Supabase | $0 (free tier) |
| OpenRouter | ~$0.001 per regional briefing, ceiling $20/month |
| Total | ~$5/month plus a few cents of model usage |

## Known gaps

- `SITREP_ADMIN_TOKEN` is unset in production, so the pipeline and debug routes are open.
- `/debug/supabase` counts only the four regional rows; the Global briefing is not counted.
- PDFs have no object-storage archive; the container cache is the only copy.
- The in-app scheduler only runs if the container is alive at 06:00 UTC; the 07:00 UTC
  Actions job is the safety net, not a guarantee.
- Google Play closed testing is next (20 testers, 14 days), then production, then App
  Store. The production AAB is built with `eas build --profile production`.

## See also

- [README.md](README.md) - what SITREP is and how to run it locally.
- [DEPLOYMENT_CONFIG.md](DEPLOYMENT_CONFIG.md) - variables, failure modes, and static values.
- [api/SETUP_OPENROUTER.md](api/SETUP_OPENROUTER.md) - model access setup.
- [mobile/README.md](mobile/README.md) - the mobile and web client.
