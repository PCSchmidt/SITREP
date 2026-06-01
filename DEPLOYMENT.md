# SITREP Deployment Guide

# Railway + Supabase Production Deployment

## Prerequisites

- Railway account (https://railway.app)
- Supabase account (https://supabase.com)
- OpenRouter API key
- Git repository pushed to GitHub

---

## STEP 1: Railway Account Setup

1. Go to https://railway.app
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub account
4. Verify your account (email confirmation)
5. **Result**: Railway dashboard should be visible

---

## STEP 2: Supabase Project Setup

1. Go to https://supabase.com
2. Click "Start your project" → "Sign in with GitHub"
3. Authorize Supabase
4. Click "New project"
   - Organization: Create new or use existing
   - Project name: `sitrep-production`
   - Database password: Generate strong password (save this!)
   - Region: Choose closest to your users (e.g., US East)
   - Pricing plan: Free tier
5. Click "Create new project" (takes ~2 minutes)
6. **Result**: Project dashboard with connection details

### Create Database Schema

Once project is ready:

1. Go to "SQL Editor" in left sidebar
2. Run this SQL to create briefings table:ay

```sql
-- Briefings table for caching
CREATE TABLE briefings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  region TEXT NOT NULL,
  briefing_data JSONB NOT NULL,
  pdf_url TEXT,
  generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for fast region lookups
CREATE INDEX idx_briefings_region ON briefings(region);
CREATE INDEX idx_briefings_generated_at ON briefings(generated_at DESC);

-- Function to auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to call function
CREATE TRIGGER update_briefings_updated_at
    BEFORE UPDATE ON briefings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

3. Copy connection credentials:
   - Go to "Project Settings" → "Database"
   - Note "Connection string" (Pooler mode recommended)

---

## STEP 3: Railway Project Deployment

1. **Create Railway Project**:

   - Go to Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select `SITREP` repository
   - Railway will detect Python and start deploying
2. **Configure Root Directory**:

   - Click on your service
   - Go to "Settings" tab
   - Under "Build", set Root Directory: `api`
   - Click "Save"
3. **Add Environment Variables**:

   - Still in "Settings" tab
   - Scroll to "Variables" section
   - Add the following variables:

   ```
   OPENROUTER_API_KEY=<your-openrouter-api-key>
   SUPABASE_URL=<your-supabase-project-url>
   SUPABASE_KEY=<your-supabase-anon-key>
   PYTHON_VERSION=3.11
   ```

   Get Supabase credentials from:

   - Project Settings → API
   - Copy "Project URL" → SUPABASE_URL
   - Copy "anon public" key → SUPABASE_KEY
4. **Deploy**:

   - Railway will auto-deploy after adding variables
   - Monitor "Deployments" tab for build logs
   - Wait for "Success" status (~3-5 minutes)
5. **Get Production URL**:

   - Go to "Settings" tab
   - Under "Networking", click "Generate Domain"
   - Copy the generated URL (e.g., `sitrep-production.up.railway.app`)
   - **Save this URL** - you'll need it for mobile app configuration

---

## STEP 4: Automated Scheduling (no extra service needed)

Scheduling is handled **inside the backend** by an in-app APScheduler job
(`api/scheduler.py`, `CronTrigger(hour=6, minute=0, tz=UTC)`), started on app
startup in `main.py`. It runs the full pipeline **daily at 06:00 UTC** by calling
`POST /pipeline/run-weekly` (legacy endpoint name — it runs daily, not weekly).

- **No separate Railway "Cron" service is required.** As long as the web service
  is running, the daily job is scheduled automatically.
- A standalone Railway Cron service (if one exists in the project) is **redundant**
  and can be removed.
- Confirm it's live: `GET /` reports `scheduler` status and the next run time.

---

## STEP 5: Verify Deployment

1. **Test Health Endpoint**:

   ```bash
   curl https://YOUR-RAILWAY-URL.up.railway.app/health
   ```

   Expected: `{"status":"ok"}` (GET `/` reports the version, currently 0.21.0)
2. **Test Manual Pipeline Trigger**:

   ```bash
   curl -X POST https://YOUR-RAILWAY-URL.up.railway.app/pipeline/run-weekly
   ```

   Expected: Pipeline runs and caches briefings to Supabase
3. **Check Supabase**:

   - Go to Supabase project → Table Editor
   - Select `briefings` table
   - Verify 4 rows exist (one per region)

---

## STEP 6: Update Mobile App

Update mobile API base URL to point to Railway:

1. Edit `mobile/api/client.ts`:

   ```typescript
   const API_BASE_URL = 'https://YOUR-RAILWAY-URL.up.railway.app';
   ```
2. Test mobile app with production backend

---

## Troubleshooting

### Build Fails

- Check Railway logs in "Deployments" tab
- Verify `requirements.txt` is in `api/` directory
- Verify Python version is 3.11+

### API Returns 500 Errors

- Check Railway logs in "Deployments" → "View Logs"
- Verify environment variables are set correctly
- Check Supabase connection (wrong URL/key)

### Automated Scheduler Not Running

- The scheduler is in-app (APScheduler), not a Railway cron service — check the **web service** logs at startup for "scheduler configured"
- `GET /` reports scheduler status + next run time; if "Not initialized", the startup hook failed (check logs)
- Manually trigger to test: POST to `/pipeline/run-weekly`

### Playwright Fails in Railway

- Playwright requires system dependencies
- Add to `nixpacks.toml` if needed (Railway uses Nixpacks)

---

## Cost Estimate

- Railway: $5/month (Hobby plan, includes 500 hours)
- Supabase: $0 (Free tier, up to 500MB database)
- Total: **$5/month**

---

## v0.10 Deployment Status (2026-05-26)

**✅ DEPLOYED AND OPERATIONAL**

- **Production URL**: https://sitrep-production-6aac.up.railway.app
- **Version**: v0.10.0
- **Build System**: Dockerfile (replaced Nixpacks for Playwright compatibility)
- **Automated Scheduler**: Configured for Sunday 6 AM UTC
- **Last Pipeline Run**: 16 articles scraped, 4/4 regions processed, 0 errors

**Key Technical Decisions:**
- Switched from Nixpacks to Dockerfile to persist Playwright Chromium installation
- Data paths use `data/*` (not `../data/*`) since WORKDIR is `/app/api`
- Supabase caching falls back to file storage (ON CONFLICT constraint issue remains)
- Only ISW scraper operational (Defense One, Breaking Defense, IISS deferred to v0.3+)

**Verified Working:**
- ✅ Scraping (16 ISW articles)
- ✅ Region filtering (Middle East, Indo-Pacific, Europe/Africa)
- ✅ LLM synthesis (DeepSeek V4 Flash, $0.001/briefing)
- ✅ PDF generation (all 4 regions)
- ✅ File-based briefing storage
- ✅ Mobile API integration
- ✅ Weekly cron automation

---

## Next Steps After Deployment

1. ✅ Monitor first cron execution (check logs Sunday 6AM UTC)
2. Verify 2 consecutive weeks of successful runs
3. Add Sentry for error tracking (v0.11)
4. Add Mixpanel for analytics (v0.11)
5. Proceed to v0.12 (Legal & Disclaimers)
