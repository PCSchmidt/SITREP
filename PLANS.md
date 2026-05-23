# PLANS.md
# Blueprint v11 | Pending Work and Known Issues
# Created during active development sessions to track context between stops

---

## CURRENT WORK (v0.7+ - Next Gates)

**v0.6 COMPLETE** (Backend API - 4h actual vs 8h estimated)

**IMPORTANT PENDING DECISION (2026-05-23):**
- User requested review of DeepSeek/Kimi models vs current GPT-4o Mini
- **VALIDATED**: `deepseek/deepseek-chat` works on OpenRouter and produces quality BLUF output
- **TEST RESULTS**: DeepSeek (7,877 tokens, 3 sections) vs GPT-4o Mini (7,684 tokens, 2 sections)
- **COST**: Both ~$0.11-0.15 per briefing (similar cost, DeepSeek slightly more verbose)
- **DECISION NEEDED**: Switch from GPT-4o Mini to DeepSeek Chat as primary model?
  - Requires: Update openrouter_client.py MODELS list
  - Requires: Create DEC-009 superseding DEC-008
  - Requires: Update all docs (CONTRACT, README, VERSION_ROADMAP, SPEC)
- **NOTE**: Kimi models not found on OpenRouter under tested IDs (moonshot/* variants invalid)
- User preference: DeepSeek/Kimi are "much better and relatively cheap"

**Upcoming Gates** (per VERSION_ROADMAP.md):
- v0.4: Mobile Scaffold (skipped - already done in v0.1)
- v0.5: UI Design System (skipped - already done in v0.1)
- v0.7: Mobile-Backend Integration
- v0.8: PDF Mobile Integration (react-native-pdf)
- v0.9: Regional Filtering (all 4 regions)
- v0.10: Weekly Automation (Railway Cron)
- v0.11: Analytics Integration (Mixpanel + Sentry)
- v0.12: Legal & Disclaimers
- v0.13: App Store Prep
- v0.14: Beta Testing
- v1.0: Production Live

**Immediate Next Steps** (v0.7 - Mobile-Backend Integration):
1. Configure TanStack Query for API calls
2. Connect mobile app to local FastAPI backend (http://localhost:8001)
3. Replace mock data with real API fetches
4. Implement loading states and error handling
5. Add offline support with cached briefings
6. Test end-to-end: mobile fetch → display briefing

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
