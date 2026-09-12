---
name: deployment
description: "Where SITREP ships and what to verify afterwards. Use before deploying, when changing Railway variables, or when the user types /deploy."
---

# Deployment

SITREP ships to three places: the Railway API, the GitHub Pages web app, and the Expo mobile builds. This skill lists the targets, the pre-deploy gates, and the checks that prove a deploy worked.

| | |
| --- | --- |
| API | **https://sitrep-production-6aac.up.railway.app** - Railway, Docker, uvicorn + FastAPI, v0.21.10 |
| Health check | `curl https://sitrep-production-6aac.up.railway.app/health` returns `{"status":"ok"}` |
| Web app | **https://pcschmidt.github.io/sitrep/** - Expo web export, baseUrl `/sitrep` |
| Data store | Supabase Postgres; briefings survive redeploys, PDFs are regenerated on demand |
| Mobile | Expo SDK 56, `eas build --profile production`; Android `com.pcschmidt.sitrep`, versionCode 7 |

Verified 2026-09-12: the four regional briefings, the Global briefing, and their five PDFs all return 200.

## Pre-deploy gates

1. `cd api && python -m pytest tests -q` - 11 tests, zero failures. Pass `tests` explicitly: a bare `python -m pytest` from `api/` also collects `api/scripts/test_*.py` and aborts on six collection errors.
2. `/security` on the changed surface - zero CRITICAL or HIGH findings.
3. `/performance` if the change touches a screen or a query path.
4. User types `DEPLOY APPROVED`.

## Backend: Railway

- Deploy is a push. Merging to `main` in this repo triggers the Railway build (root `Dockerfile`, uvicorn + FastAPI) and a container restart.
- Service variables (names only): `SUPABASE_URL`, `SUPABASE_KEY` (publishable/anon), `SUPABASE_SERVICE_KEY`, `OPENROUTER_API_KEY`, `GUARDIAN_API_KEY`, plus `SITREP_ADMIN_TOKEN` once the admin guard is switched on.
- **Writes need `SUPABASE_SERVICE_KEY`.** The anon/publishable key cannot pass row-level security: inserts fail with `42501 new row violates row-level security policy` while the pipeline still reports success. `GET /debug/supabase` reports `key_role` and should read `service_role`.
- `requirements.txt` pins `supabase==2.31.0`. Do not downgrade: 2.9.0 rejects new-format `sb_secret_...` keys with "Invalid API key"; 2.16.0 is the first release that accepts them.
- Admin guard is opt-in. Write routes (`/scrape`, `/synthesize`, `/synthesize/global`, `/briefing/generate-pdf`, `/pipeline/run-weekly`, `/debug/supabase`, `/debug/upload-briefing`) accept `X-Admin-Token`. While Railway's `SITREP_ADMIN_TOKEN` is unset, the guard logs a warning and lets the request through, so those routes are currently unauthenticated. The read routes the mobile app needs (`/`, `/health`, `/briefing/latest`, `/briefing/global`, `/briefing/latest/pdf`) stay public.
- Redeploy caveat: every push to `main` and every Railway variable change restarts the container. That is now cheap - briefings live in Supabase and PDFs regenerate on demand - but expect a short warm-up and a slower first PDF request. Do not re-run the pipeline just because the container restarted.

## Web app: GitHub Pages

- Hosted from the portfolio repo `C:/Dev/AIEngineeringProjects/PCSchmidt.github.io/PCSchmidt.github.io`, not from this repo. The deployed bundle lives in that repo's `public/sitrep/`.
- That repo's `.github/workflows/deploy.yml` runs on push to its `master` branch: it runs `astro build` and publishes the site to GitHub Pages.
- Rebuild the SITREP Expo web export before pushing a web change. The local clone holds only `public/sitrep/privacy-policy.html` and `public/sitrep/terms.html`, so the clone alone does not show what produces the deployed bundle - confirm the export step before shipping a web change.
- Leave `public/sitrep/privacy-policy.html` and `public/sitrep/terms.html` in place. Store listings point at https://pcschmidt.github.io/sitrep/privacy-policy and https://pcschmidt.github.io/sitrep/terms (both return 200).
- `public/404.html` forwards `/sitrep/` deep links to `/sitrep/?redirect=...`; the app root layout follows that parameter.

## Mobile

- Production AAB: `eas build --profile production` run from `mobile/`.
- Current path: Google Play closed testing (20 testers, 14 days), then the Apple App Store. Still to produce: 5 screenshots and a 1024x500 feature graphic.
- PDF viewing differs by platform: `react-native-pdf` natively, an `<iframe>` on web (`mobile/components/PlatformPdfViewer.web.tsx`) with a 6s fallback timer. The API must keep serving PDFs with `Content-Disposition: inline`; an attachment makes the browser download the file and the web viewer stays on "Loading PDF...".

## Verify after any deploy

```bash
curl -sS https://sitrep-production-6aac.up.railway.app/
curl -sS https://sitrep-production-6aac.up.railway.app/briefing/latest
curl -sS -o /dev/null -w '%{http_code}\n' https://sitrep-production-6aac.up.railway.app/briefing/latest/pdf
curl -sS https://sitrep-production-6aac.up.railway.app/debug/supabase
```

1. `GET /` reports the expected version and `"scheduler": "Running - Daily at 06:00 UTC"`. Either route now reports the real version: `/health` used to hardcode `0.10.0` and was fixed on 2026-09-12 to return `APP_VERSION`.
2. Briefing and PDF return 200. The first PDF request after a restart is slower because it is regenerated and cached to `data/pdfs/`.
3. `/debug/supabase` reports `key_role: service_role` and `briefings_count: 4`. Global is not counted; that number covers the four regional rows only.
4. Log the deploy in DEPLOYMENT.md and add any incident to ERRORS.md.

## Pipeline runs

- `POST /pipeline/run-weekly` runs the full job: 13 default scrapers (14 exist; `GuardianAPIScraper` joins only when `GUARDIAN_API_KEY` is set), about 540 articles, four regional syntheses plus the composite Global. It takes about 20 minutes, so trigger it with a short client timeout - the client times out and the server finishes.
- A second request while a run is in progress is refused. The in-app APScheduler runs the same job daily at 06:00 UTC; startup does not run it. `.github/workflows/daily-briefing.yml` is the backup trigger at 07:00 UTC and only fires when that day's briefing is missing.

## Rollback

- Application rollback: redeploy the previous successful Railway deployment, or revert the commit on `main`, then repeat the checks above.
- A bad briefing is data, not code: re-run the pipeline instead of rolling back the app.
- Foundation-file rollback (gate tags, `.blueprint/snapshots/`) is the `rollback` skill's job, not part of a production rollback.

## Related

- Repo README: ../../../README.md
- `../rollback/SKILL.md` for reverting a gate, `../security/SKILL.md` before a production deploy, `../testing/SKILL.md` for the test command.
