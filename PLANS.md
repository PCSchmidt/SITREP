# PLANS.md
# Blueprint v11 | Pending Work and Known Issues
# Created during active development sessions to track context between stops

---

## CURRENT WORK (v0.13 - Analytics Integration)

**v0.11 COMPLETE** (Source Expansion - 12h actual vs 12-16h estimated)
- RSSBaseScraper base class. 6 working scrapers: ISW, Defense One, Breaking Defense, War on the Rocks, The War Zone, Al Jazeera. ~84 articles/week.

**v0.12 COMPLETE** (Global Briefing - 5h actual vs 6h estimated)
- GET /briefing/global, synthesize_global() with cross-regional system prompt. ALL tab now shows single thematic global card. Weekly pipeline generates global briefing as Step 4.

**Upcoming Gates** (per VERSION_ROADMAP.md):

- v0.13: Analytics Integration (Mixpanel + Sentry) - 6h estimated ← NEXT
- v0.14: Legal & Disclaimers - 4h estimated
- v0.15: App Store Prep - 6h estimated
- v0.16: Beta Testing - 8-16h estimated
- v1.0: Production Live - 6-12h estimated

**Immediate Next Steps** (v0.13 - Analytics Integration):

1. Install Mixpanel React Native SDK in mobile app
2. Track events: app_open, briefing_view, region_filter, pdf_view, pdf_share
3. Install Sentry React Native SDK
4. Configure crash reporting + error tracking
5. Verify telemetry appears in Mixpanel and Sentry dashboards

---

## DEFERRED WORK (Post-v1.0)

### Source Expansion Wave 2 (v1.1+)

**Goal**: Reach 20-50 sources. Current count: 6 (v0.11). Target: 20+ by v1.1, 50 long-term.

RSS probed 2026-05-29. "Confirmed" = tested locally. "Likely" = DNS failed locally but should work on Railway Linux (same pattern as Reuters, Defense News from earlier probes).

#### Asia-Pacific

| Source | URL | RSS Status | Feed URL | Notes |
|--------|-----|------------|----------|-------|
| The Diplomat | thediplomat.com | **Confirmed** (96 items) | `/feed/` | Top Asia-Pacific geopolitics magazine |
| East Asia Forum | eastasiaforum.org | Likely (DNS local) | `/feed/` | ANU academic-policy; Indo-Pacific economics + security |
| Lowy Institute | lowyinstitute.org | Likely (DNS local) | `/rss.xml` | Australia's premier foreign policy think tank; South Pacific coverage |
| CSIS | csis.org | Partial (stale feed) | `/rss.xml` stale; need Playwright | Washington Asia programs; free content |

#### Africa

| Source | URL | RSS Status | Feed URL | Notes |
|--------|-----|------------|----------|-------|
| ISS Africa | issafrica.org | Likely (DNS local) | `/rss.xml` | Johannesburg-based; conflict, governance, crime across sub-Saharan Africa |
| The Africa Report | theafricareport.com | **Confirmed** (10 items) | `/feed/` | Pan-African business and political coverage |
| Chatham House Africa | chathamhouse.org | Blocked (403) | n/a | UK think tank; need CloakBrowser or Playwright |
| Africa Confidential | africa-confidential.com | Paywalled | n/a | Diplomat-grade Africa intelligence; need CloakBrowser |

#### Latin America

| Source | URL | RSS Status | Feed URL | Notes |
|--------|-----|------------|----------|-------|
| Americas Society / AS-COA | as-coa.org | **Confirmed** (10 items) | `/rss.xml` | Business, policy, LatAm economics |
| NACLA | nacla.org | Likely (DNS local) | `/feed/` | Politics, social movements, US-LatAm relations |
| CEPAL/ECLAC | cepal.org | API/structured | REST API | UN body; authoritative LatAm macroeconomic data |
| LADB | ladb.unm.edu | Subscription | n/a | UNM news aggregator; institutional subscription needed |

#### Multi-Region

| Source | URL | RSS Status | Feed URL | Notes |
|--------|-----|------------|----------|-------|
| Council on Foreign Relations | cfr.org | **Confirmed** (24 items) | `/feed` | Expert-authored briefs + Global Conflict Tracker |
| Crisis Group | crisisgroup.org | **Confirmed** (10 items) | `/rss.xml` | Conflict-focused; country-level granularity across Africa, Asia, LatAm |
| Geopolitical Futures | geopoliticalfutures.com | **Confirmed** (5 items) | `/feed/` | George Friedman; data-driven forecasting; limited free tier |
| Foreign Policy | foreignpolicy.com | **Confirmed** (25 items) | `/feed/` | Broad international; significant free content |
| SIPRI | sipri.org | Likely (DNS local) | `/rss.xml` | Arms, conflict, security economics; strong Africa + Asia-Pacific datasets |
| World Bank Blog | blogs.worldbank.org | 404 (wrong URL) | Try `/en/topic/*/rss` | Economic/development analysis; try topic-specific feeds |
| Chatham House | chathamhouse.org | Blocked (403) | n/a | UK foreign policy think tank; need CloakBrowser |
| AfDB | afdb.org | API/structured | REST API | African Development Bank; 54-country economic data |

#### CloakBrowser Priority Targets

When CloakBrowser is integrated (post-v1.0), these unlock high-signal paywalled content:

| Source | Why It Matters |
|--------|---------------|
| IISS (iiss.org) | Military Balance data; Strategic Survey; 403 on all requests |
| Africa Confidential | Diplomat-grade Africa intelligence; most Africa analysts subscribe |
| Chatham House | 403 on RSS; flagship UK foreign policy research |
| Geopolitical Futures (deeper) | Full articles behind soft paywall |
| Jane's (janes.com) | Order-of-battle data; premium military equipment specs |
| Defense News | DNS failures locally; procurement + strategy |
| Bellingcat | OSINT investigations; may need headers or CloakBrowser |
| Foreign Policy (deeper) | Some long-form analysis is paywalled |

#### API/Structured Data Sources (different integration pattern)

These are authoritative but require REST API integration rather than RSS scraping. Useful for adding economic/data context to briefings.

| Source | API | Value |
|--------|-----|-------|
| World Bank | data.worldbank.org/api | Economic indicators for all countries |
| CEPAL/ECLAC | api.cepal.org | LatAm macroeconomic forecasts + data |
| AfDB | api.afdb.org | African development data; 54 countries |
| SIPRI datasets | sipri.org/databases | Arms trade, military expenditure, conflict data |

### Scraper Archive (v0.2 era - superseded)

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

## AUTO-COMPACT WARNING: 2026-05-27T13:29:46Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: f3dca97 Docs: Update deployment status for v0.10 completion
Tests: 6 passed, 4 skipped, 9 warnings, 5 errors in 63.54s (0:01:03)
