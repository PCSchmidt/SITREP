# PLANS.md
# Blueprint v11 | Pending Work and Known Issues
# Created during active development sessions to track context between stops

---

## CURRENT WORK (v0.9+ - Next Gates)

**v0.8 COMPLETE** (PDF Mobile Integration - 6h actual vs 6h estimated, 0% variance)

**What Shipped (2026-05-25):**
- ✅ react-native-pdf library integrated with custom Expo development build
- ✅ react-native-blob-util native module compiled (custom build required)
- ✅ Full-screen PDF viewer at [mobile/app/pdf/[id].tsx](mobile/app/pdf/[id].tsx)
- ✅ Share button opens Android/iOS share sheet (Drive, Gmail, Messages, Print)
- ✅ Save button downloads PDF to Downloads folder
- ✅ Centered header layout (Share/Save buttons don't overlap gear icon)
- ✅ Lazy-loaded PDF component prevents startup errors
- ✅ Comprehensive error handling with detailed logging ([PDF Share], [PDF Save] prefixes)
- ✅ Backend PDF endpoint verified working (3-page PDF, 5.8KB)

**Known Limitations:**
- ⚠️ Android may kill app when Share dialog opens (OS memory management, not a bug)
- ⚠️ Requires custom development build (~35min Android build time with native modules)
- ⚠️ PDF caching uses device storage (expo-file-system cacheDirectory)

**Upcoming Gates** (per VERSION_ROADMAP.md):
- v0.9: Regional Filtering (all 4 regions) - 6h estimated
- v0.10: Weekly Automation (Railway Cron) - 10h estimated
- v0.11: Analytics Integration (Mixpanel + Sentry) - 6h estimated
- v0.12: Legal & Disclaimers - 4h estimated
- v0.13: App Store Prep - 6h estimated
- v0.14: Beta Testing - 8-16h estimated
- v1.0: Production Live - 6-12h estimated

**Immediate Next Steps** (v0.9 - Regional Filtering):
1. Backend: Generate briefings for all 4 regions (Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere)
2. Backend: Update /briefing/latest endpoint to accept region parameter
3. Mobile: Implement region tabs UI component (horizontal scroll or dropdown)
4. Mobile: Wire region selection to API calls
5. Mobile: Add region filter persistence (remember user's last selection)
6. Test: Verify all 4 regions display unique content
7. Polish: Smooth transitions between region views

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
