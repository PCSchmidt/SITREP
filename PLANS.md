# PLANS.md
# Blueprint v11 | Pending Work and Known Issues
# Created during active development sessions to track context between stops

---

## CURRENT WORK (v0.11+ - Next Gates)

**v0.10 COMPLETE** (Production Deployment - 10h actual vs 10h estimated, 0% variance)

**What Shipped (2026-05-26):**

- ✅ Railway deployment with Dockerfile (Playwright + Chromium)
- ✅ Supabase PostgreSQL database integration for briefing caching
- ✅ Railway cron job for weekly automation (Sundays 6 AM UTC)
- ✅ Production URL configured: <https://sitrep-production-6aac.up.railway.app>
- ✅ Mobile API client updated to Railway production URL
- ✅ Environment variables configured (OPENROUTER_API_KEY, SUPABASE_URL, SUPABASE_KEY)
- ✅ End-to-end pipeline verified: scraping → region filtering → LLM synthesis → PDF generation
- ✅ Manual pipeline trigger endpoint working (/pipeline/run-weekly)
- ✅ All 4 regions processing successfully (Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere)
- ✅ DeepSeek V4 Flash LLM generating briefings ($0.001/briefing)

**Infrastructure Details:**

- Railway service: SITREP (main API) - Online, fully functional
- Railway cron service: humorous-manifestation - Next run Sunday 6 AM UTC
- Supabase project: sitrep-production with briefings table (RLS configured, fallback to file storage working)
- Deployment configs: Dockerfile, nixpacks.toml
- Last pipeline run: 16 articles scraped, 3 regions with content, 4/4 regions successful, 0 errors

**Technical Fixes During v0.10:**
- Fixed Playwright browser installation in Docker (RUN playwright install chromium)
- Fixed path mismatch issue (changed ../data/* to data/* in main.py)
- Fixed OpenRouter API authentication

**Upcoming Gates** (per VERSION_ROADMAP.md):

- v0.11: Analytics Integration (Mixpanel + Sentry) - 6h estimated
- v0.12: Legal & Disclaimers - 4h estimated
- v0.13: App Store Prep - 6h estimated
- v0.14: Beta Testing - 8-16h estimated
- v1.0: Production Live - 6-12h estimated

**Immediate Next Steps** (v0.11 - Analytics Integration):

1. Integrate Mixpanel SDK for user event tracking
2. Integrate Sentry SDK for crash reporting and error tracking
3. Add event tracking: app_open, briefing_view, region_filter, pdf_view, pdf_share
4. Verify telemetry in Mixpanel and Sentry dashboards
5. Test crash reporting and error tracking

---

## DEFERRED WORK (Post-v0.2)

### Scraper Fixes (v0.3 or later)

**Defense One** (`api/scrapers/defenseone_scraper.py`):
- Status: Scaffold created, selectors untested
- Issue: HTML selectors need debugging (likely similar to ISW fix)
- Estimated: 1-2h to fix selectors and test
- Priority: Medium (ISW covers enough sources for v0.2.2)

**Breaking Defense** (`api/scrapers/breakingdefense_scraper.py`):
- Status: Scaffold created, selectors untested
- Issue: HTML selectors need debugging
- Estimated: 1-2h to fix selectors and test
- Priority: Medium

**IISS** (`api/scrapers/iiss_scraper.py`):
- Status: Scaffold created, selectors untested
- Issue: HTML selectors need debugging
- Estimated: 1-2h to fix selectors and test
- Priority: Medium

**How to Fix**:
1. Run debug script (similar to `api/debug_isw.py`)
2. Inspect HTML structure with BeautifulSoup
3. Find correct selectors for:
   - Article list items
   - Title links
   - Date elements
   - Content container
4. Update scraper selectors
5. Test and validate JSON output

---

## TECHNICAL NOTES

### Scraping Lessons Learned

**What Worked**:
- Playwright alone (no CloakBrowser needed for open sources)
- Base scraper class with retry logic and JSON export
- Parallel execution with error handling (orchestrator pattern)
- Region inference from keywords in content

**Selector Patterns** (for future scrapers):
- ISW: `h3 a` for titles, `article` for content
- Date parsing: Regex from title text when not in dedicated element
- Content cleaning: Remove `script`, `style`, `nav`, `footer`, `header`

**Debugging Process**:
1. Create debug script to fetch page HTML
2. Use BeautifulSoup to test selectors
3. Save HTML to file for manual inspection if needed
4. Update scraper with working selectors

**Common Issues**:
- Sites use different HTML structures (no standard)
- Selectors are fragile and break when sites update
- Date formats vary widely across sources
- Paywalls may require CloakBrowser (not needed yet)

---

## COST TRACKING

**v0.2.1 Costs**: $0 (Playwright is free, scraping is local)  
**v0.2.2 Expected**: $0-0.50 (Gemini free tier, DeepSeek fallback ~$0.014/briefing)

---

## SESSION NOTES

**2026-05-23**:
- Completed v0.2.1 scraper infrastructure
- ISW scraper fully working (16 articles, 400KB JSON)
- Fixed HTML selectors after initial test failures
- Deferred other 3 scrapers to post-v0.2
- Starting v0.2.2 (LLM Synthesis)

---

## STOP EVENT RESUME

If session stops during v0.2.2:
- ISW scraper working: `data/scraped/isw_2026-05-23.json`
- Resume with: `/start` → continue v0.2.2 synthesis work

## AUTO-COMPACT WARNING: 2026-05-23T13:25:21Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 83cec48 v0.3 - PDF Generation Backend
Tests: 3 skipped, 3 warnings in 0.35s

## AUTO-COMPACT WARNING: 2026-05-23T14:32:36Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 106a899 Capture context: DeepSeek model validation and pending decision
Tests: 6 passed, 4 skipped, 9 warnings, 5 errors in 85.44s (0:01:25)

## AUTO-COMPACT WARNING: 2026-05-24T17:11:29Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 14b90f5 v0.7 - Mobile-Backend Integration
Tests: 6 passed, 4 skipped, 9 warnings, 5 errors in 102.47s (0:01:42)

## AUTO-COMPACT WARNING: 2026-05-25T01:01:29Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 14b90f5 v0.7 - Mobile-Backend Integration
Tests: 6 passed, 4 skipped, 9 warnings, 5 errors in 127.20s (0:02:07)

## AUTO-COMPACT WARNING: 2026-05-25T11:04:36Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 14b90f5 v0.7 - Mobile-Backend Integration
Tests: 6 passed, 4 skipped, 9 warnings, 5 errors in 90.83s (0:01:30)

## AUTO-COMPACT WARNING: 2026-05-26T14:03:27Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 87d4f73 Add nixpacks.toml for Railway deployment
Tests: 1 failed, 5 passed, 4 skipped, 8 warnings, 5 errors in 29.57s

## AUTO-COMPACT WARNING: 2026-05-26T15:32:11Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 4c9a7ba Fix: Add Playwright browser installation to Railway build
Tests: 6 passed, 4 skipped, 9 warnings, 5 errors in 36.81s

## AUTO-COMPACT WARNING: 2026-05-26T17:12:14Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: d31fc05 Fix: Remove railway.toml to let Dockerfile CMD control start command
Tests: 1 failed, 5 passed, 4 skipped, 8 warnings, 5 errors in 51.10s
