# PLANS

Open work, known gaps, and deferred material for SITREP, with the older plan history kept as a record. Facts in the first two sections are verified 2026-09-12; everything under a "historical" heading is dated material, not current state.

| | |
| --- | --- |
| Current backend version | v0.21.11 (`APP_VERSION` in `api/main.py`) |
| Live API | **https://sitrep-production-6aac.up.railway.app** |
| Web app | https://pcschmidt.github.io/sitrep/ |
| Facts checked | 2026-09-12 |

---

## Open work (verified 2026-09-12)

1. **Google Play submission is next.** The closed-testing gate is 20 testers for 14 days. The production AAB is built with `eas build --profile production`.
2. **Apple App Store submission comes after Play**, once the Play result is known.
3. **Store assets are still to produce:** 5 screenshots and a 1024x500 feature graphic. Neither exists in the repo.
4. **`SITREP_ADMIN_TOKEN` is not set on Railway**, so `/pipeline/run-weekly`, `/synthesize`, `/synthesize/global`, `/briefing/generate-pdf` and `/debug/*` are still unauthenticated in production. The token guard is opt-in: it logs a warning per request and allows it while the variable is unset.
5. **There is no automated PDF archive in object storage.** PDFs are cached to `data/pdfs/` on disk and rebuilt from the stored briefing when missing or stale.
6. **`/debug/supabase` `briefings_count` does not include the Global row.** It counts the four regional briefings only.

Items 1 and 2 are the next planned work. Items 3 to 6 are known gaps; none of them is scheduled.

---

## Historical: app store prep through v0.16 (not current)

Superseded by "Open work" above. The build is now v0.21.11 and the app-store gate below closed long ago; this section is the state as recorded on 2026-05-29 and 2026-06-01.

**Recent completions (2026-05-29):**

- **v0.11 COMPLETE** (Source Expansion, 12h) — RSSBaseScraper; 6 scrapers; ~84 articles/week
- **v0.12 COMPLETE** (Global Briefing, 5h) — /briefing/global; synthesize_global(); ALL tab
- **v0.13 COMPLETE** (Analytics, 4h) — Mixpanel + Sentry; 5 events; services/analytics.ts
- **v0.14 COMPLETE** (Legal, 3h) — PRIVACY_POLICY.md + TERMS_OF_SERVICE.md; in-app screens; PDF footer
- **v0.15 COMPLETE** (GDELT, 4h) — GDELTScraper; 3 regional queries; LatAm/Africa/SE Asia local sources; 7 total scrapers

**Upcoming Gates** (per VERSION_ROADMAP.md):

- v0.16: App Store Prep - 6h ← NEXT
- v0.17: Beta Testing - 8-16h
- v1.0: Production Live - 6-12h

**Immediate Next Steps** (v0.16 - App Store Prep):

1. App icons — 1024×1024 for iOS + Android adaptive icon
2. Splash screen — dark military aesthetic, SITREP wordmark
3. App store screenshots — iOS (6.7") + Android showing home, detail, PDF viewer
4. App store listing copy — title, description, keywords, category
5. Bundle ID verified — com.pcschmidt.sitrep (already set in app.json)
6. Android signing keystore — generate release keystore
7. iOS signing — configure Expo managed credentials
8. Privacy Policy URL — host PRIVACY_POLICY.md at pcschmidt.github.io/sitrep/privacy
9. Rebuild dev APK to activate analytics native modules (Mixpanel + Sentry)

---

## Upcoming tasks (flagged 2026-06-01) - historical

Superseded by "Open work" above. Item A is done; item B below is now tracked as open work items 1 to 3 and the mobile notes are kept for reference.

### A. Documentation reconciliation and codebase cleanup (done 2026-06-01)

- [x] **Aligned/reconciled docs** to v0.21: README, SPEC.md, VERSION_ROADMAP.md
  (added v0.17–v0.21 rows), DEPLOYMENT.md + DEPLOYMENT_CONFIG.md (corrected the
  stale "weekly Railway cron" → in-app daily APScheduler), APP_STORE_LISTING.md
  (Sunday→daily, source list), DESIGN_SYSTEM.md. (No CLAUDE.md/CHANGELOG.md at
  root.) FUTURE_VISION.md left as an explicitly point-in-time aspirational doc.
- [x] **Removed superseded files**: `pdf_generator.py`, `pdf_generator_v2.py`,
  `pdf_generator_reportlab.py` (v3 is the only generator wired in), `iiss_scraper.py`.
- [x] **Untracked accidental artifacts**: 509 `__pycache__`/`.pyc`, `mobile/api/venv/`,
  sample `data/pdfs|briefings|scraped/`, `.claude/state`; broadened `.gitignore`.
- [x] **Moved one-off test scripts** → `api/scripts/`.
- Note: Optional remaining: archive dated scratch logs (`scratchnotes.md`,
  `SESSION_NOTES_2026-05-27.md`) — low priority; left in place as history.

### B. Mobile app-store deployment (first-time notes, historical)

- **Google Play Store FIRST**, then Apple App Store ~weeks later after seeing
  how Google goes. User is new to app deployment.
- Builds on v0.16 App Store Prep (EAS config + store listing + checklist).
- Lead-time prerequisites to gather EARLY:
  - Google Play Console account ($25 one-time)
  - Hosted **Privacy Policy URL** (REQUIRED — app uses Mixpanel + Sentry;
    PRIVACY_POLICY.md exists, needs public hosting e.g. GitHub Pages)
  - **Production AAB** build (not the preview APK) via EAS, with Play App Signing
  - Store assets: icon, feature graphic (1024×500), phone screenshots,
    short (80 char) + full (4000 char) descriptions, category
  - Play **Data Safety** form + **content rating** questionnaire
  - Start on **internal/closed testing** track before production rollout

---

## Deferred work (post-v1.0) - planned, not started

Nothing in this section is in the v0.21.11 build.

### Source expansion Wave 2 (v1.1+)

**Goal**: reach 20-50 sources. The "Current count: 6 (v0.11)" line that stood here is stale. As of 2026-09-12, 13 scrapers run by default and `api/scrapers/` holds 14 files; `GuardianAPIScraper` runs only when `GUARDIAN_API_KEY` is set. A full run pulls about 540 articles. Target: 20+ sources by v1.1, 50 long-term.

Checked against `api/scrapers/` and SPEC.md on 2026-09-12. Sources named in this section that are already live: The Diplomat (`rss_scraper.py` feed table), Council on Foreign Relations (`cfr_scraper.py`), Foreign Policy (`foreignpolicy_scraper.py`), CSIS and the World Bank (both in `rss_scraper.py`), and Americas Quarterly (`americasquarterly_scraper.py`, which this section does not list at all). The rest have no scraper yet. SPEC.md lists the live set the same way. Read the tables below as the 2026-05-29 probe record, not as an accurate open-source backlog. `LatAmBackupScraper` is registered in `orchestrator.py` but disabled: its feed list is empty.

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

#### CloakBrowser priority targets

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

#### API and structured data sources (different integration pattern)

These are authoritative but require REST API integration rather than RSS scraping. Useful for adding economic/data context to briefings.

| Source | API | Value |
|--------|-----|-------|
| World Bank | data.worldbank.org/api | Economic indicators for all countries |
| CEPAL/ECLAC | api.cepal.org | LatAm macroeconomic forecasts + data |
| AfDB | api.afdb.org | African development data; 54 countries |
| SIPRI datasets | sipri.org/databases | Arms trade, military expenditure, conflict data |

### Scraper archive (v0.2 era) - historical

Superseded by the live scrapers in `api/scrapers/`. Two of the three files below are now real RSS scrapers registered in `orchestrator.py` (`defenseone_scraper.py`, `breakingdefense_scraper.py`); `iiss_scraper.py` was removed. The notes are kept as a record of the v0.2 debugging work.

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

## Technical notes - historical

The v0.2 scraper record, superseded by the pipeline described in SPEC.md. The selector and debugging notes are still the practical reference for adding a scraper.

### Scraping lessons learned

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

## Cost tracking - historical

Superseded by the cost model in SPEC.md. Current state: about $0.013 per daily run on `deepseek/deepseek-v4-flash`, roughly $5-6/month typical. The v0.2 figures below are the record of that gate.

**v0.2.1 Costs**: $0 (Playwright is free, scraping is local)  
**v0.2.2 Expected**: $0-0.50 (Gemini free tier, DeepSeek fallback ~$0.014/briefing)

---

## Session notes - historical

Superseded by the v0.21.11 state at the top of this file. Kept as the v0.2.1 record.

**2026-05-23**:
- Completed v0.2.1 scraper infrastructure
- ISW scraper fully working (16 articles, 400KB JSON)
- Fixed HTML selectors after initial test failures
- Deferred other 3 scrapers to post-v0.2
- Starting v0.2.2 (LLM Synthesis)

---

## Stop event resume - historical (v0.2.2)

Superseded by the current state at the top of this file. These steps refer to the v0.2.2 session and the old `/start` flow.

If session stops during v0.2.2:
- ISW scraper working: `data/scraped/isw_2026-05-23.json`
- Resume with: `/start` → continue v0.2.2 synthesis work

## Auto-compact warnings - historical

Superseded: these are timestamped records of v0.2-v0.21 development sessions that hit context auto-compaction. The test counts and git states are as reported on those dates, not today.

## Auto-compact warning: 2026-05-23T13:25:21Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 83cec48 v0.3 - PDF Generation Backend
Tests: 3 skipped, 3 warnings in 0.35s

## Auto-compact warning: 2026-05-23T14:32:36Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 106a899 Capture context: DeepSeek model validation and pending decision
Tests: 6 passed, 4 skipped, 9 warnings, 5 errors in 85.44s (0:01:25)

## Auto-compact warning: 2026-05-24T17:11:29Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 14b90f5 v0.7 - Mobile-Backend Integration
Tests: 6 passed, 4 skipped, 9 warnings, 5 errors in 102.47s (0:01:42)

## Auto-compact warning: 2026-05-25T01:01:29Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 14b90f5 v0.7 - Mobile-Backend Integration
Tests: 6 passed, 4 skipped, 9 warnings, 5 errors in 127.20s (0:02:07)

## Auto-compact warning: 2026-05-25T11:04:36Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 14b90f5 v0.7 - Mobile-Backend Integration
Tests: 6 passed, 4 skipped, 9 warnings, 5 errors in 90.83s (0:01:30)

## Auto-compact warning: 2026-05-26T14:03:27Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 87d4f73 Add nixpacks.toml for Railway deployment
Tests: 1 failed, 5 passed, 4 skipped, 8 warnings, 5 errors in 29.57s

## Auto-compact warning: 2026-05-26T15:32:11Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 4c9a7ba Fix: Add Playwright browser installation to Railway build
Tests: 6 passed, 4 skipped, 9 warnings, 5 errors in 36.81s

## Auto-compact warning: 2026-05-26T17:12:14Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: d31fc05 Fix: Remove railway.toml to let Dockerfile CMD control start command
Tests: 1 failed, 5 passed, 4 skipped, 8 warnings, 5 errors in 51.10s

## Auto-compact warning: 2026-05-27T13:29:46Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: f3dca97 Docs: Update deployment status for v0.10 completion
Tests: 6 passed, 4 skipped, 9 warnings, 5 errors in 63.54s (0:01:03)

## Auto-compact warning: 2026-05-30T14:45:14Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: b79357b Fix: Temporarily disable Sentry plugin for production build
Tests: 6 passed, 4 skipped, 9 warnings, 6 errors in 62.17s (0:01:02)

## Auto-compact warning: 2026-05-30T20:24:50Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: fbc85c6 Fix: Replace urllib with httpx in RSS scraper for reliability
Tests: 6 passed, 4 skipped, 9 warnings, 6 errors in 52.37s

## Auto-compact warning: 2026-05-31T10:59:53Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: bb6e1df Add Global PDF generation + improve source attribution
Tests: 6 passed, 4 skipped, 9 warnings, 6 errors in 55.16s

## Auto-compact warning: 2026-05-31T13:21:05Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: 41026bd v0.18: Professional PDF redesign + enhanced synthesis depth
Tests: 6 passed, 4 skipped, 9 warnings, 6 errors in 44.12s

## Auto-compact warning: 2026-05-31T19:03:45Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: dab339d Add feedparser dependency for RSS scrapers
Tests: 1 error in 1.04s

## Auto-compact warning: 2026-06-01T13:39:34Z
Context auto-compacted. 70-80% of detail was lost.
Session backup saved to: .claude/backups/
Resume with /start option 2 and read this file carefully.
Last git state: f6f3853 Docs: reconcile README to v0.21 state
Tests: 6 errors in 1.98s

---

## See also

- [README.md](README.md) - what SITREP is and how to run it
- [SPEC.md](SPEC.md) - current specification, sources, and cost model
- [VERSION_ROADMAP.md](VERSION_ROADMAP.md) - gate-by-gate history and the remaining v1.0 work
- [DECISIONS.md](DECISIONS.md) - architecture decisions and their rationale
