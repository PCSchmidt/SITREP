# SPEC

Current specification for SITREP: what ships in v1.0, what is deferred, and the sources and pipeline behind it. Gate-by-gate history is in the appendix at the end. Facts here verified 2026-09-12.

| | |
| --- | --- |
| Backend | v0.21.11 (`APP_VERSION` in `api/main.py`), FastAPI on Railway |
| Live API | https://sitrep-production-6aac.up.railway.app |
| Web app | https://pcschmidt.github.io/sitrep/ (Expo web export) |
| Mobile | Expo / React Native (Expo SDK ~56.0.8, React Native 0.85.3, React 19.2.3, `expo-router` ~56.2.8); Android package `com.pcschmidt.sitrep`, versionCode 7 |
| Data store | Supabase Postgres for briefings; PDFs generated on demand, not archived |
| Status | Pre-launch: Google Play submission next, then Apple App Store |

## Project

| | |
| --- | --- |
| App name | SITREP |
| Current gate | v0.21.11 - backend live in production |
| Status | Pre-launch. Android preview build runs on device. Google Play submission is next, then Apple App Store |
| Build type | Production / GA |
| Target launch | No fixed date. Google Play closed testing (20 testers, 14 days) has to pass first |

---

## Elevator pitch

SITREP delivers daily geopolitical intelligence briefings to mobile. It scrapes open-source defense, economic, and think-tank publications (ISW, Defense One, War on the Rocks, Reuters, Bloomberg, CFR, and more), synthesizes them with a multi-model AI pipeline, and presents the result in BLUF format: the Bottom Line Up Front structure used by military intelligence products.

Everything in it comes from public reporting and is written by a language model. The app says so on every screen. The target is App Store and Play Store release as a portfolio project; Google Play submission is the next step.

---

## Current state (verified 2026-09-12)

**Backend v0.21.11 is live** at <https://sitrep-production-6aac.up.railway.app>; the web export is live at <https://pcschmidt.github.io/sitrep/>. Checked that day:

| Check | Result |
| --- | --- |
| Five briefings (4 regional + Global) via the API | 200 |
| Five PDFs via `/briefing/latest/pdf` | 200 |
| Briefing storage | Supabase Postgres. Remote restarts no longer lose briefings |
| PDF storage | Not stored. `/briefing/latest/pdf` loads the newest briefing (Supabase first, `data/briefings/*.json` fallback), regenerates the PDF when missing or older than `generated_at`, caches it to `data/pdfs/{slug}_{YYYY-MM-DD}.pdf`, and serves it inline |
| Admin write endpoints | Unauthenticated in production. `X-Admin-Token` is enforced only when `SITREP_ADMIN_TOKEN` is set, and that Railway variable is not set yet |
| `api/tests/` | 11 passing (`pytest` from `api/`) |

Known gaps, stated plainly:

- `Global` is not counted by `/debug/supabase` `briefings_count`; that count covers the four regional rows only.
- There is no automated PDF archive in object storage. Every PDF is rebuilt from the stored briefing when the cached file is missing or stale.
- The GitHub Actions daily workflow and `refresh_railway_briefings.py` send `X-Admin-Token` only when `SITREP_ADMIN_TOKEN` is set, so the endpoints stay open until the variable exists.
- Any push to `main` or any Railway variable change restarts the container. Briefings survive now; only a short warm-up is lost.
- `GET /health` reported a hardcoded `0.10.0`; fixed on 2026-09-12 to return `APP_VERSION`, so `/health`, `/`, and `/openapi.json` now agree.

### API surface

Live routes (`/openapi.json`, 2026-09-12). Write and debug routes accept the optional `X-Admin-Token` header.

| Method | Path | Notes |
| --- | --- | --- |
| GET | `/` | Service identity, reports `APP_VERSION` |
| GET | `/health` | Liveness. Version string here is stale |
| GET | `/briefing/latest` | Newest briefing for one region, Supabase first |
| GET | `/briefing/global` | Composite Global briefing |
| GET | `/briefing/latest/pdf` | PDF for one region, inline, rebuilt when stale |
| POST | `/scrape` | Scrape one region |
| POST | `/synthesize` | Synthesize one regional briefing |
| POST | `/synthesize/global` | Synthesize the Global briefing |
| POST | `/briefing/generate-pdf` | Force PDF generation for one region |
| POST | `/pipeline/run-weekly` | Full job, about 20 minutes |
| GET | `/debug/supabase` | `storage`, `key_role`, `client_initialized`, `briefings_count` |
| POST | `/debug/upload-briefing` | Push a briefing to Supabase |

There is no `/refresh` and no `/scrape/status` route.

---

## v1.0 features

Checked items are shipped in v0.21.11. The only open v1.0 item is store approval.

### Core intelligence briefing
- [x] Daily automated briefing generation (Internal APScheduler)
- [x] BLUF (Bottom Line Up Front) format matching The LOWDOWN aesthetic
- [x] 4 geographic regions: Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere
- [x] Cited sources from Tier 1 defense publications
- [x] Heavy AI-generated content disclaimers
- [x] **PDF export** - Auto-generated executive-design PDF report (PT Serif + Lato editorial layout, hyperlinked sources) per region + composite Global

### Mobile experience
- [x] React Native + Expo (iOS + Android)
- [x] Dark military aesthetic UI (near-black + amber accents, AMOLED-ready)
- [x] Region filtering via tabs
- [x] **PDF viewer** - In-app full-screen PDF viewing with pinch-to-zoom
- [x] **PDF sharing** - Share via iOS/Android share sheet (email, messages, AirDrop)
- [x] **PDF save** - Save to Files app / Downloads for offline access
- [x] **PDF open** - Open in external apps (Adobe, Apple Books, etc.)
- [x] Save/bookmark briefings locally on device
- [x] Offline reading support
- [x] Smooth navigation and loading states
- [x] ALL tab shows composite Global briefing - all four regions stitched in full plus a cross-regional executive summary (not a thin condensed synthesis)

### Infrastructure
- [x] FastAPI backend on Railway
- [x] Supabase for briefing caching
- [x] Playwright for scraping open-source news (CloakBrowser optional for paywalls)
- [x] Multi-model LLM synthesis via Open Router: `deepseek/deepseek-v4-flash` → `deepseek/deepseek-v3.2` → `moonshotai/kimi-k2.5` (99% cost reduction; empty content and rate limits fall through to the next model)
- [x] Cost-optimized: single cached briefing per day served to all users (~$0.013/run regardless of user count)
- [x] 13 scrapers, ~540 articles/run (defense + RSS economic/think-tank feeds via Google News proxy + Guardian API + US/UK government + GDELT)
- [x] Composite Global briefing endpoint /briefing/global - all four regions in full + cross-regional executive summary

### Monitoring and analytics
- [x] Mixpanel for user behavior tracking (services/analytics.ts, 5 events)
- [x] Sentry for crash reporting and error tracking (Sentry.wrap root, EXPO_PUBLIC_SENTRY_DSN)
- [x] Weekly automation monitoring with failure alerts

### Compliance
- [x] Privacy Policy (PRIVACY_POLICY.md + in-app privacy screen), published at https://pcschmidt.github.io/sitrep/privacy-policy
- [x] Terms of Service (TERMS_OF_SERVICE.md + in-app terms screen), published at https://pcschmidt.github.io/sitrep/terms
- [ ] Google Play Store approval, then Apple App Store approval (v1.0)
- [x] AI content disclaimers throughout UI

---

## v1.1+ deferred features

Planned, not started. Nothing in this list is in the v0.21.11 build.

- [ ] User authentication (Supabase Auth)
- [ ] Personalized region preferences
- [ ] Push notifications for new briefings
- [ ] Save favorite articles to user account
- [ ] Search/filter past briefings
- [ ] Share briefings via social media

---

## Scraping sources

**Active (v0.21.11, 13 scrapers by default, ~540 articles/run):**

`api/scrapers/` holds 14 scrapers; `GuardianAPIScraper` is added only when `GUARDIAN_API_KEY` is set, which is why a run shows 13. Each attempt has a 60s timeout and 2 retries per source. The 2026-09-12 run produced 30 articles per regional desk and 120 articles for the Global briefing.

Defense / direct:
- ISW - Ukraine/Russia, Iran daily assessments (Playwright, domcontentloaded)
- Defense One - Pentagon policy, military tech (RSS via httpx)
- War on the Rocks - Strategic analysis (RSS via httpx)
- The War Zone - Military aviation, weapons systems (RSS via httpx)
- Al Jazeera - Non-Western perspective, Middle East/Africa (RSS via httpx)
- Foreign Policy - Geopolitical analysis (RSS via httpx)
- Council on Foreign Relations (CFR) - Expert analysis (RSS via httpx)

Economic / think-tank (revived via Google News RSS proxy `site:DOMAIN when:7d`, except where noted):
- Reuters, Bloomberg - markets, economic security (proxy: both block or have dropped RSS)
- World Bank, Brookings, Carnegie Endowment - development and policy analysis (proxy)
- CSIS - native feed (csis.org/rss.xml)
- Financial Times, The Economist - international business and analysis (native RSS)

Mainstream international (multi-feed RSS in `api/scrapers/rss_scraper.py`):
- BBC World, BBC Business, The Guardian World - broad coverage
- The Diplomat - Asia-Pacific (native `/feed/`, confirmed live 2026-09-12)
- Middle East Eye - Middle East and North Africa
- Military Times, Task & Purpose, The Aviationist - defense trade coverage

Aggregators / structured:
- Guardian API (open-platform key) - broad international coverage
- US/UK government sources - official statements/releases
- GDELT DOC 2.0 - local-language sources machine-translated (FIPS 10-4 country codes + OR-wrapped keywords; best-effort, headline fallback on timeout)

**Known-fragile / best-effort:**
- GDELT - aggressive per-IP rate-limiting (429); returns 0 gracefully when throttled
- Google News proxy feeds - depend on news.google.com redirect links (headline + snippet, not full body)

**Wave 2 / future targets (v1.1+).** The Diplomat was on this list and is live now; see the active list above.
- The Africa Report, Americas Society/AS-COA, International Crisis Group
- East Asia Forum (ANU), Lowy Institute, ISS Africa, NACLA, SIPRI
- Americas Quarterly is already live for Latin America (`api/scrapers/americasquarterly_scraper.py`)

**Wave 3 targets (v1.2+, need CloakBrowser or special handling):**
- IISS - Military Balance data; 403 on all requests
- Chatham House - UK foreign policy research; 403 on RSS
- Africa Confidential - Diplomat-grade Africa intelligence; paywalled
- Jane's - Order-of-battle, equipment specs; paywalled
- Geopolitical Futures (deeper) - George Friedman; soft paywall

**API/structured data (future, different integration pattern):**
- World Bank API - Economic indicators, all countries
- CEPAL/ECLAC API - Latin American macroeconomic data
- AfDB API - African Development Bank, 54-country data
- SIPRI datasets - Arms trade, military expenditure structured exports

---

## Technical architecture

```
Mobile (React Native + Expo)          Web (Expo web export)
  ↓ TanStack Query                      ↓ fetch + <iframe> PDF view
FastAPI Backend (Railway, uvicorn)
  ↓ briefings (write via service key)   ↑ PDF built on demand
Supabase Postgres                       data/pdfs/*.pdf (cache only)
  ↑ Daily APScheduler (06:00 UTC)
Scraping → LLM Synthesis → Composite Global → PDF (pdf_generator_v3)
  ↑ Playwright + RSS/httpx + Open Router
```

**Daily pipeline (about 20 minutes end to end):**

1. The internal APScheduler triggers the full pipeline daily at 06:00 UTC. The same job is exposed as `POST /pipeline/run-weekly`, which needs a short client timeout: the client times out, the server finishes. A second request while a run is in progress is refused.
2. 13 scrapers run with per-scraper asyncio timeouts → raw articles JSON (~540 articles per run).
3. Multi-model LLM synthesis per region. Waterfall order from `api/synthesis/openrouter_client.py`:
   `deepseek/deepseek-v4-flash` → `deepseek/deepseek-v3.2` → `moonshotai/kimi-k2.5`. Null content raises so the next model fires.
4. Compose the Global briefing: all four regions stitched in full plus a cross-regional executive summary.
5. Generate the executive-design PDF (`pdf_generator_v3`, PT Serif + Lato) per region and for Global.
6. Store the briefings in Supabase. PDFs are cached to disk only and rebuilt on demand. Mobile refetches on foreground with `cache:false`.

---

## Cost model

**Operational ceiling**: $20/month  
**Build budget**: < $50 total LLM usage  

**Cost breakdown (estimated):**
- DeepSeek V4 Flash (`deepseek/deepseek-v4-flash`, Open Router): ~$0.013/daily run (5 briefings: 4 regional + composite Global) → ~$0.40/month; fixed regardless of user count (single cached briefing served to all)
- Railway backend: $5/month (free tier likely sufficient)
- Supabase: $0 (free tier)
- Sentry: $0 (free tier)
- Mixpanel: $0 (free tier)
- Fallback models: $0/month if DeepSeek V4 Flash fails (DeepSeek V3.2/Kimi K2.5, rare)

**Total**: $5-6/month typical, $10/month worst case

---

## Appendix: gate completion log (historical)

Everything below this line is the gate-by-gate record written during the build, from v0.0 (2026-05-21) to v0.9 (2026-05-26). It is history, not current state. Dates, hour estimates, and file paths are as recorded at the time; for example the file-based cache and the anon-key notes here were replaced later by Supabase storage with the service key. Current state is in the section at the top of this file.

---

## v0.1 completion summary

**Goal**: Mobile Foundation - Expo app configuration, design system, component library, navigation

**What Shipped**:
- [x] App configured with SITREP bundle ID (com.pcschmidt.sitrep)
- [x] Dark mode enforced (AMOLED-optimized)
- [x] NativeWind + Tailwind CSS configured with design system colors
- [x] Design tokens file (colors, typography, spacing, regions)
- [x] Component library: BriefingCard, RegionTab, BLUFSection, DisclaimerBanner, SourceCitation
- [x] Expo Router file-based navigation (home, detail, about screens)
- [x] Mock briefing data and TypeScript types
- [x] Dependencies: Expo Router, NativeWind, TanStack Query, Zustand, react-native-pdf
- [x] TypeScript strict mode with NativeWind types

**Completion criteria**:
- [x] App displays military aesthetic dark UI
- [x] Navigation between screens working
- [x] Components render placeholder content correctly
- [x] Git committed cleanly (2 commits)

**Estimated hours**: 8h  
**Actual hours**: ~3h (62% under estimate - efficient component library build)  
**Status**: COMPLETE (2026-05-22)

---

## v0.2 work in progress

**Goal**: Scraping Pipeline + LLM Synthesis - Prove end-to-end pipeline works

### v0.2.1 Scraping pipeline - in progress

**What Shipped**:
- [x] Playwright-based scraper infrastructure (base class, orchestrator, retry logic)
- [x] ISW scraper fully working (16 articles scraped, 400KB JSON output)
- [x] JSON schema implemented (source, url, title, date, author, content, region_tags)
- [x] Automatic region inference from content (Middle East, Indo-Pacific, etc.)
- [x] Date filtering (7-day rolling window)
- [ ] Defense One scraper - needs selector fixes
- [ ] Breaking Defense scraper - needs selector fixes
- [ ] IISS scraper - needs selector fixes

**Data Quality** (ISW):
- Articles: 16 from last 7 days
- Content length: ~26k chars/article (full text extraction)
- File size: 400KB JSON
- Sample: `data/scraped/isw_2026-05-23.json`

**Technical Decisions**:
- Playwright alone sufficient for open-source sites like ISW (no CloakBrowser needed)
- HTML selectors are site-specific and fragile (expected)
- ISW uses `<h3 a>` for article links, `<article>` for content
- Date parsing from article titles (ISW format: "Title, May 22, 2026")

**Known Issues**:
- Defense One, Breaking Defense, IISS scrapers need HTML selector debugging
- Each site has different structure (requires 1-2h per site to fix)
- Deferred to post-v0.2 cleanup

**Completion criteria**:
- [x] At least 1 source scraping successfully
- [x] JSON output validated
- [x] Content extraction working (not just metadata)
- [ ] All 4 sources working (deferred to v0.3+)

**Estimated hours**: 8h  
**Actual hours**: ~4h (50% under estimate - one source sufficient for v0.2.2)  
**Status**: SUFFICIENT FOR v0.2.2 (2026-05-23)

---

### v0.2.2 LLM synthesis - complete

**Goal**: Generate BLUF-format briefing using multi-model waterfall

**What Shipped**:
- [x] Open Router client with automatic model fallback
- [x] Multi-model waterfall: DeepSeek V4 Flash → DeepSeek V3.2 → Kimi K2.5 (99% cost reduction)
- [x] BLUF synthesizer with professional military intelligence format
- [x] System prompt engineered for BLUF output (JSON schema)
- [x] Markdown code fence parsing for robust JSON extraction
- [x] Test synthesis successful: Europe/Africa briefing generated

**Output Quality**:
- Generated briefing: `data/briefings/europe_africa_2026-05-23.json`
- BLUF: Clear executive summary with strategic implications
- Sections: 2 thematic sections (Russian Offensive, Iran Strait of Hormuz)
- Citations: 3 sources per section, properly attributed
- Key developments: 3 actionable bullet points
- Outlook: Forward-looking assessment
- Structure: Valid JSON matching schema

**Model Performance**:
- Primary model: DeepSeek V4 Flash (DeepSeek AI)
- Tokens used: ~8,000 (7,000 prompt + 1,000 completion typical)
- Cost: ~$0.001/briefing (99% reduction vs GPT-4o Mini)
- Quality: Production-ready for portfolio showcase

**Technical Decisions**:
- Open Router unified API (simpler than managing 3 separate APIs)
- DeepSeek V4 Flash as primary (excellent quality, 99% cheaper than GPT-4o Mini)
- JSON schema enforcement in system prompt
- Automatic markdown code fence stripping

**Completion criteria**:
- [x] LLM integration working
- [x] BLUF format validated
- [x] Source citations present
- [x] Output saved to JSON
- [x] Cost under $20/month ceiling

**Estimated hours**: 12h  
**Actual hours**: ~3h (75% under estimate - prompt worked on first iteration)  
**Status**: COMPLETE (2026-05-23)

---

## v0.2 overall summary

**Gate**: v0.2 Scraping Pipeline + LLM Synthesis  
**Goal**: Prove end-to-end pipeline (scrape → synthesize → briefing)

**What Shipped**:
- Scraping: ISW scraper working (16 articles, 400KB JSON)
- Synthesis: BLUF briefing generation (DeepSeek V4 Flash via Open Router, 99% cost reduction)
- Output: Professional intelligence briefing in JSON format

**Time**:
- Estimated: 20h (8h scraping + 12h synthesis)
- Actual: ~7h (6h total across both sub-gates)
- Variance: -65% (significantly faster than estimated)

**Deferred**:
- Defense One, Breaking Defense, IISS scrapers (selector fixes needed)
- Additional prompt iteration (current quality sufficient)
- Middle East specific briefing (tested with Europe/Africa instead)

**Status**: COMPLETE (2026-05-23)

---

## v0.3 PDF generation backend - complete

**Goal**: Generate professional PDF briefings from BLUF JSON

**What Shipped**:
- [x] ReportLab-based PDF generator (Windows-compatible)
- [x] Military aesthetic with amber (#FFA500) styling
- [x] Cover page with classification markings and AI disclaimer
- [x] BLUF summary with highlighted formatting
- [x] Detailed sections with source citations
- [x] GET /briefing/latest/pdf API endpoint
- [x] POST /briefing/generate-pdf API endpoint

**Output Quality**:
- Generated PDF: `data/pdfs/europe_africa_2026-05-23.pdf`
- File size: 5.8 KB (3 pages)
- Format: Professional intelligence briefing layout
- Styling: Military aesthetic with structured sections
- Compatibility: Works on Windows (ReportLab vs WeasyPrint)

**Technical Decisions**:
- ReportLab programmatic generation > WeasyPrint HTML→PDF
- Letter size, 0.75" margins
- Paragraph styles: CoverTitle, SectionHeader, BLUF, BodyJustified, Source
- Amber border highlights for BLUF and section headers
- Classification markings: UNCLASSIFIED // AI-GENERATED

**Completion criteria**:
- [x] PDF generation working
- [x] Professional military aesthetic
- [x] API endpoint serving PDFs
- [x] Windows compatibility verified
- [x] Output validated (3 pages, proper formatting)

**Estimated hours**: 8h  
**Actual hours**: ~2h (75% under estimate - ReportLab simpler than HTML/CSS templates)  
**Status**: COMPLETE (2026-05-23)

---

## v0.6 Backend API - complete

**Goal**: FastAPI REST endpoints for scraping, synthesis, and briefing retrieval

**What Shipped**:
- [x] POST /scrape endpoint (triggers ISW scraper orchestrator)
- [x] POST /synthesize endpoint (generates BLUF briefing from articles)
- [x] GET /briefing/latest endpoint (returns cached briefing JSON)
- [x] POST /briefing/generate-pdf endpoint (generates PDF from briefing)
- [x] GET /briefing/latest/pdf endpoint (serves PDF file)
- [x] File-based caching (data/briefings/, data/pdfs/)
- [x] Comprehensive API test suite

**API Functionality**:
- Scraping: Orchestrator runs all scrapers, returns statistics
- Synthesis: Async LLM synthesis with proper error handling
- Briefing retrieval: Latest briefing by region
- PDF generation: ReportLab integration via API
- PDF serving: FileResponse with proper media type

**Technical Details**:
- Fixed async/await for synthesize_region() call
- Fixed JSON loading for wrapper format (articles key)
- Timezone-aware datetime (datetime.now(timezone.utc))
- Proper HTTPException handling for 404/500 errors

**Test Results**:
- All 6 endpoints passing
- Scraping: 16 articles from ISW
- Synthesis: 2-section briefing generated
- PDF: 5.8 KB, 3 pages

**Deferred**:
- Supabase integration (moved to v0.10 Weekly Automation / Railway deployment)
- File-based caching sufficient for local development

**Completion criteria**:
- [x] POST /scrape working
- [x] POST /synthesize working
- [x] GET /briefing/latest working
- [x] API endpoints tested end-to-end
- [x] Local backend fully functional
- [ ] Supabase deferred to deployment gate

**Estimated hours**: 8h  
**Actual hours**: ~4h (50% under estimate - endpoints simpler than expected)  
**Status**: COMPLETE (2026-05-23)

---

## v0.7 Mobile-backend integration - complete

**Goal**: Connect mobile app to FastAPI backend with React Query for data fetching

**What Shipped**:
- [x] TanStack Query setup (QueryClientProvider with offline-first config)
- [x] API client (mobile/api/client.ts) with network IP configuration (10.0.0.201:8001)
- [x] Backend data transformation (BLUF format → mobile Briefing type)
- [x] React Query hooks (mobile/hooks/useBriefings.ts) for data fetching
- [x] Updated index.tsx with real API calls replacing mock data
- [x] Updated detail/[id].tsx with dynamic briefing fetching
- [x] Loading states (ActivityIndicator) for all async operations
- [x] Error handling with user-friendly messages
- [x] Offline support (5min stale time, 10min cache time, auto-retry)

**Technical Details**:
- API base URL configured for local network testing (not localhost)
- Transform function maps backend sections/sources to mobile format
- Query keys structure: `['briefings', 'all-regions']` and `['briefings', 'region', region]`
- Error messages guide user to check backend availability
- Region filtering works client-side on cached data

**Integration Verified**:
- [x] Backend accessible on local network (http://10.0.0.201:8001/health)
- [x] API endpoint returns briefing data (http://10.0.0.201:8001/briefing/latest)
- [x] TypeScript compilation passes with no errors
- [x] Mobile code properly configured for network requests

**Testing Status**:
- [x] API integration verified via curl testing
- [x] Backend serving data correctly on local network
- [ ] E2E mobile testing blocked by Babel configuration issue (`.plugins is not a valid Plugin property`)
- [ ] Network connectivity issues (Comcast router) preventing physical device testing

**Deferred**:
- Babel plugin configuration debugging (NativeWind/Reanimated conflict)
- Physical device E2E testing (pending network stability)
- Android emulator E2E testing (pending Babel fix)

**Completion criteria**:
- [x] TanStack Query configured
- [x] API client created with fetch functions
- [x] React Query hooks implemented
- [x] Mock data replaced with real API calls
- [x] Loading and error states added
- [x] Offline caching configured
- [ ] End-to-end visual testing (blocked by environment issues)

**Estimated hours**: 6h  
**Actual hours**: ~3h integration work + ~3h environment debugging (Babel, network, emulator setup)  
**Status**: CODE COMPLETE (2026-05-24) - Testing pending environment resolution

---

## v0.8 PDF mobile integration - complete

**Goal**: Full in-app PDF viewing with Share and Save functionality

**What Shipped**:
- [x] react-native-pdf library integrated (v7.0.4)
- [x] react-native-blob-util native module (v0.24.9) with custom development build
- [x] expo-file-system for PDF download/caching
- [x] expo-sharing for native share sheet integration
- [x] Full-screen PDF viewer screen ([mobile/app/pdf/[id].tsx](mobile/app/pdf/[id].tsx))
- [x] Lazy-loaded PDF component (prevents startup errors)
- [x] Share button - Opens Android/iOS share sheet (Drive, Gmail, Messages, Print, Bluetooth)
- [x] Save button - Downloads PDF to device Downloads folder
- [x] Centered header layout (Share/Save buttons don't overlap gear icon)
- [x] Loading states and error handling with detailed logging
- [x] "View as PDF" button added to briefing detail screen

**Technical Details**:
- Custom Expo development build required (react-native-pdf won't work in Expo Go)
- PDF source: `http://10.0.0.201:8001/briefing/latest/pdf`
- Lazy import prevents native module errors: `const Pdf = (await import('react-native-pdf')).default`
- Share workflow: Download to cache → Check availability → Open share sheet
- Save workflow: Download to documentDirectory → Show success alert
- Comprehensive logging with `[PDF Share]` and `[PDF Save]` prefixes

**Build Process**:
- Initial build: ~35 minutes (Android native compilation with CMake)
- Codegen directories generated during build for TurboModules
- Native modules: react-native-blob-util, react-native-pdf, react-native-reanimated, react-native-worklets
- Metro bundler: 1738 modules, ~6s bundle time

**Testing Verified**:
- [x] PDF loads and displays 3-page briefing document
- [x] Pinch-to-zoom, scrolling, and pagination working
- [x] Share button opens native share sheet with all system options
- [x] Save button downloads PDF and shows "Briefing saved to Downloads" alert
- [x] Header layout centered, no gear icon overlap
- Note: Android backgrounding behavior when Share dialog opens (normal OS behavior)

**Known Limitations**:
- App may be killed by Android when Share dialog is open (OS memory management)
- Requires custom development build (cannot use Expo Go for testing)
- PDF caching uses device storage (expo-file-system cacheDirectory)

**Completion criteria**:
- [x] PDF viewer displays briefings
- [x] Share functionality working
- [x] Save functionality working
- [x] UI polished (centered buttons, proper spacing)
- [x] Error handling and logging implemented
- [x] Backend PDF endpoint accessible and serving valid PDFs

**Estimated hours**: 6h  
**Actual hours**: ~6h (3h initial setup + native module debugging, 2h build time, 1h testing/fixes)  
**Status**: COMPLETE (2026-05-25)

---

## v0.9 Regional filtering - complete

**Goal**: Enable all 4 geographic regions with unique briefings and region filter persistence

**What Shipped**:
- [x] Backend briefings generated for all 4 regions (Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere)
- [x] Backend PDFs generated for all 4 regions
- [x] Mobile region filter persistence with AsyncStorage (remembers user's last selection)
- [x] Debug PDF test button removed from home screen
- [x] API endpoints verified working for all regions

**Regional Briefing Content**:
- Middle East: US-Iran negotiations, Strait of Hormuz protection racket (5.0KB JSON, 7.4KB PDF)
- Indo-Pacific: Taiwan arms sales, South Korea maritime security, Sino-Russian relations (6.2KB JSON, 8.0KB PDF)
- Europe/Africa: Ukraine war stabilization, Russia nuclear posturing, Iran negotiations (6.2KB JSON, 8.7KB PDF)
- Western Hemisphere: No recent intelligence (minimal content, 286B JSON, 3.4KB PDF)

**Technical Details**:
- AsyncStorage installed (@react-native-async-storage/async-storage)
- Region persistence key: `@sitrep_selected_region`
- useEffect hooks for loading and saving region selection
- All 4 /briefing/latest?region= endpoints tested and working
- TypeScript compilation passes with no errors

**Completion criteria**:
- [x] All 4 regions have unique briefings generated
- [x] Backend API serves all 4 regions correctly
- [x] Mobile region filter persistence implemented
- [x] PDFs generated for all 4 regions
- [x] End-to-end testing verified

**Estimated hours**: 6h  
**Actual hours**: ~6h (2h backend synthesis, 1h PDF generation, 2h mobile AsyncStorage, 1h testing)  
**Status**: COMPLETE (2026-05-26)

---

## v0.0 completion summary

**Goal**: Foundation setup - project scaffolding, dependencies, repo structure

**Tasks**:
1. Initialize React Native + Expo project (TypeScript, Expo Router)
2. Set up FastAPI backend directory structure
3. Install core dependencies:
   - Mobile: `expo-router`, `nativewind`, `@tanstack/react-query`, `zustand`
   - Backend: `fastapi`, `supabase-py`, `playwright`, `reportlab`
4. Configure Supabase project (database + connection)
5. Set up Git repository structure (mobile/, api/, docs/)
6. Write basic README with project overview
7. Verify mobile app runs on iOS Simulator and Android Emulator
8. Verify FastAPI server starts on localhost:8000

**Completion criteria**:
- [x] Mobile app displays "Hello SITREP" on both platforms
- [x] FastAPI returns `{"status": "ok"}` on GET /health
- [ ] Supabase connection verified (requires user setup)
- [x] All dependencies installed without errors
- [x] Git repo initialized with initial commit
- [x] Backend server verified running on localhost:8000
- [x] Mobile dependencies verified (471 packages)
- [x] Backend dependencies verified (44 packages)
- [x] OSINT source research complete (80+ sources identified)

**Estimated hours**: 4h (2h raw × 2.0x calibration)  
**Actual hours**: ~4h  
**Status**: COMPLETE (2026-05-21)


---

## Where to read next

- [README.md](README.md) - overview, live URLs, and how to run the project
- [VERSION_ROADMAP.md](VERSION_ROADMAP.md) - gate history and what v1.0 still needs
- [DECISIONS.md](DECISIONS.md) - dated decisions, including the 2026-09-12 storage and key fix
- [PLANS.md](PLANS.md) - open work and known gaps
- [FUTURE_VISION.md](FUTURE_VISION.md) - post-v1.0 plans, clearly marked as planned
