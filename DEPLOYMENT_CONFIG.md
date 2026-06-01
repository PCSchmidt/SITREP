# DEPLOYMENT_CONFIG.md
# SITREP | Production Deployment Configuration
# Updated: 2026-05-31

---

## ARCHITECTURE

```
Mobile (React Native + Expo)
  ↓ HTTPS API calls
Railway (FastAPI backend)
  ↓ Cached briefings
Supabase (PostgreSQL)
  ↑ Daily in-app APScheduler (06:00 UTC)
  Playwright + RSS/httpx + Guardian API + GDELT → LLM → composite Global → PDF (v3)
```

**Production URL**: https://sitrep-production-6aac.up.railway.app
**Schedule**: Daily 06:00 UTC via the backend's **internal APScheduler** (`scheduler.py`, `CronTrigger(hour=6)`), not a separate Railway cron service. The job triggers `POST /pipeline/run-weekly` (legacy endpoint name; runs daily). Any standalone Railway "Cron" service is redundant with the in-app scheduler.

---

## RAILWAY (Backend)

Dashboard: railway.app → SITREP project

### Services
| Service | Type | Status |
|---------|------|--------|
| SITREP | Web (Dockerfile) | ✅ Running — hosts the in-app daily APScheduler |
| humorous-manifestation | Cron | ⚠️ Legacy/redundant — scheduling now lives in-app (safe to remove) |

### Environment Variables
Set in Railway dashboard → Service → Variables:

```
OPENROUTER_API_KEY=sk-or-...        # Required — LLM synthesis
SUPABASE_URL=https://...supabase.co # Required — briefing cache
SUPABASE_KEY=eyJ...                 # Required — Supabase anon key
```

### Deployment
- Trigger: push to `main` branch auto-deploys
- Build: Dockerfile in repo root
- Health check: GET /health → `{"status":"ok"}`; GET / reports `version` (currently 0.21.0) + scheduler status
- Logs: Railway dashboard → Service → Logs

### Manual pipeline trigger
```bash
curl -X POST https://sitrep-production-6aac.up.railway.app/pipeline/run-weekly
```

---

## SUPABASE (Database)

Dashboard: supabase.com → sitrep-production

### Tables
| Table | Purpose |
|-------|---------|
| briefings | Cached regional + global briefings (JSON) |

### Connection
- Pool port: 6543 (used in production)
- Direct port: 5432 (used for migrations)
- RLS: configured (anon key only reads briefings)

### Backup
File-based fallback is automatic — if Supabase unreachable, briefings
saved to `data/briefings/` on Railway ephemeral storage.

---

## OPENROUTER (LLM)

Dashboard: openrouter.ai → API Keys

### Models (waterfall)
1. `deepseek/deepseek-v4-flash` — primary ($0.001/briefing)
2. `deepseek/deepseek-v3.2` — fallback
3. `moonshotai/kimi-k2.5` — final fallback

### Cost ceiling
$20/month total. 4 regional + 1 global briefing/week = 5 × $0.001 = $0.005/week.

---

## EXPO / MOBILE APP

### Development build workflow (for physical device testing)
```bash
# Terminal 1 — ADB port forward (USB connected)
"C:/Users/pchri/AppData/Local/Android/Sdk/platform-tools/adb.exe" reverse tcp:8081 tcp:8081

# Terminal 2 — Metro bundler
cd mobile
npx expo start

# On Samsung S25+ — open SITREP app → exp://localhost:8081
```

### Rebuild dev APK (after adding native modules)
```bash
cd mobile
npx expo run:android
# Build time: ~10 minutes
# Device ID: R5CY10TXT0H (Samsung S25+)
```

### Production build (App Store / Play Store)
```bash
# Requires Expo Application Services (EAS) account
cd mobile
npx eas build --platform android --profile production
npx eas build --platform ios --profile production
```

### Analytics tokens (.env.local — gitignored)
```
EXPO_PUBLIC_MIXPANEL_TOKEN=<from mixpanel.com → Project Settings → Token>
EXPO_PUBLIC_SENTRY_DSN=<from sentry.io → Project → Client Keys → DSN>
```

---

## GITHUB

Repository: github.com/PCSchmidt/SITREP (or equivalent)

### Branch strategy
- `main` — production (auto-deploys to Railway on push)
- Feature work directly on main for personal project

### Commit hook
Co-Authored-By lines stripped by `.git/hooks/commit-msg` hook.
Reinstall: `bash ~/.claude/hooks/strip-coauthor.sh`

---

## PRE-DEPLOY CHECKLIST

Before any production deploy:

- [ ] `git status` clean (no uncommitted changes)
- [ ] All API endpoint tests passing (`python -m pytest api/test_api_endpoints.py`)
- [ ] TypeScript clean (`npx tsc --noEmit` in mobile/)
- [ ] OPENROUTER_API_KEY set in Railway environment
- [ ] SUPABASE_URL + SUPABASE_KEY set in Railway environment
- [ ] Health check passes: `curl https://sitrep-production-6aac.up.railway.app/health`

---

## COMMON FAILURE MODES

| Failure | Symptom | Fix |
|---------|---------|-----|
| Playwright not installed | `browserType.launch: Executable doesn't exist` | RUN playwright install chromium in Dockerfile |
| Path mismatch | `FileNotFoundError: data/briefings` | Paths relative to `api/` not project root |
| OpenRouter 401 | `Authentication failed` | Check OPENROUTER_API_KEY in Railway env vars |
| Supabase timeout | Falls back to file storage | Normal — file fallback is active |
| GDELT rate limited | 0 articles from GDELT scraper | Expected on first run after development; Railway IP resets weekly |
| region name bug | `assert 'Europe' == 'Europe/Africa'` | Restart local uvicorn server (stale in-memory code) |

---

## STATIC VALUES

```
BACKEND_URL:      https://sitrep-production-6aac.up.railway.app
BUNDLE_ID (iOS):  com.pcschmidt.sitrep
PACKAGE (Android): com.pcschmidt.sitrep
SCHEDULE:         daily 06:00 UTC (in-app APScheduler CronTrigger(hour=6))
PYTHON_VERSION:   3.11
API_VERSION:      0.21.0
```
