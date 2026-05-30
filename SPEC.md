# SPEC.md
# Blueprint v11 | Project Specification
# Written during SCOPE CONFIRMED phase. Updated at each gate close.

## PROJECT

**App name**: SITREP  
**Current gate**: v0.17 - IN PROGRESS  
**Status**: Beta Testing Phase - Android functional, working toward Play Store Internal Testing  
**Build type**: Production / GA  
**Target launch**: 2026-08-21 (3 months)  

---

## ELEVATOR PITCH

SITREP delivers military-grade geopolitical intelligence briefings to mobile. It scrapes open-source defense publications (ISW, Defense One, IISS, Breaking Defense), synthesizes them using AI, and presents weekly threat assessments in professional BLUF format—the same structure used by military intelligence products. Deployed to App Store and Play Store as a portfolio showcase.

---

## v1.0 FEATURES

### Core Intelligence Briefing
- ✅ Weekly automated briefing generation (Railway Cron)
- ✅ BLUF (Bottom Line Up Front) format matching The LOWDOWN aesthetic
- ✅ 4 geographic regions: Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere
- ✅ Cited sources from Tier 1 defense publications
- ✅ Heavy AI-generated content disclaimers
- ✅ **PDF export** - Auto-generated professional PDF report (15-20 pages, all regions)

### Mobile Experience
- ✅ React Native + Expo (iOS + Android)
- ✅ Dark military aesthetic UI (near-black + amber accents, AMOLED-ready)
- ✅ Region filtering via tabs
- ✅ **PDF viewer** - In-app full-screen PDF viewing with pinch-to-zoom
- ✅ **PDF sharing** - Share via iOS/Android share sheet (email, messages, AirDrop)
- ✅ **PDF save** - Save to Files app / Downloads for offline access
- ✅ **PDF open** - Open in external apps (Adobe, Apple Books, etc.)
- ✅ Save/bookmark briefings locally on device
- ✅ Offline reading support
- ✅ Smooth navigation and loading states
- ✅ ALL tab shows global combined briefing (cross-regional synthesis) instead of 4 separate cards

### Infrastructure
- ✅ FastAPI backend on Railway
- ✅ Supabase for briefing caching
- ✅ Playwright for scraping open-source news (CloakBrowser optional for paywalls)
- ✅ Multi-model LLM synthesis (DeepSeek V4 Flash → V3.2 → Kimi K2.5 fallback via Open Router, 99% cost reduction)
- ✅ Cost-optimized: single cached briefing per week served to all users (~$0.001/briefing)
- ✅ 7 working scrapers (ISW + Defense One + War on the Rocks + The War Zone + Al Jazeera + Foreign Policy + CFR, 109 articles from latest scrape)
- ✅ Global combined briefing endpoint /briefing/global for cross-regional synthesis

### Monitoring & Analytics
- ✅ Mixpanel for user behavior tracking (services/analytics.ts, 5 events)
- ✅ Sentry for crash reporting and error tracking (Sentry.wrap root, EXPO_PUBLIC_SENTRY_DSN)
- ✅ Weekly automation monitoring with failure alerts

### Compliance
- ✅ Privacy Policy (PRIVACY_POLICY.md + in-app privacy screen)
- ✅ Terms of Service (TERMS_OF_SERVICE.md + in-app terms screen)
- 🔲 App Store and Play Store approval (v1.0)
- ✅ AI content disclaimers throughout UI

---

## v1.1+ DEFERRED FEATURES

🔲 User authentication (Supabase Auth)  
🔲 Personalized region preferences  
🔲 Push notifications for new briefings  
🔲 Save favorite articles to user account  
🔲 Search/filter past briefings  
🔲 Share briefings via social media  

---

## SCRAPING SOURCES

**Active (v0.17, 7 sources working, 109 articles latest scrape):**

- ISW - Ukraine/Russia, Iran daily assessments (Playwright, 17 articles)
- Defense One - Pentagon policy, military tech (RSS via httpx, 15 articles)
- War on the Rocks - Strategic analysis (RSS via httpx, 18 articles)
- The War Zone - Military aviation, weapons systems (RSS via httpx, 20 articles)
- Al Jazeera - Non-Western perspective, Middle East/Africa (RSS via httpx, 8 articles)
- Foreign Policy - Geopolitical analysis (RSS via httpx, 20 articles)
- Council on Foreign Relations (CFR) - Expert analysis (RSS via httpx, 11 articles)

**Not working (DNS/feed issues):**

- Breaking Defense - Feed returning DNS errors
- Americas Quarterly - Feed returning DNS errors
- GDELT DOC 2.0 - Rate limited to 0 articles in recent runs

**Wave 2 targets (v1.1, RSS confirmed working):**
- The Diplomat - Asia-Pacific geopolitics (96 items/feed)
- The Africa Report - Pan-African political/business coverage
- Americas Society/AS-COA - Latin America policy and economics
- Council on Foreign Relations (CFR) - Multi-region expert analysis
- International Crisis Group - Conflict-focused, country-level depth
- Foreign Policy - Broad international, significant free content

**Wave 2 targets (v1.1, RSS likely on Railway):**
- East Asia Forum (ANU) - Indo-Pacific economics and security
- Lowy Institute - Australia foreign policy, South Pacific focus
- ISS Africa - Sub-Saharan Africa conflict and governance
- NACLA - Latin American politics and social movements
- SIPRI - Arms, conflict, security economics globally

**Wave 3 targets (v1.2+, need CloakBrowser or special handling):**
- IISS - Military Balance data; 403 on all requests
- Chatham House - UK foreign policy research; 403 on RSS
- Africa Confidential - Diplomat-grade Africa intelligence; paywalled
- Jane's - Order-of-battle, equipment specs; paywalled
- Geopolitical Futures (deeper) - George Friedman; soft paywall
- Defense News, Bellingcat, Foreign Policy (deeper)

**API/structured data (future, different integration pattern):**
- World Bank API - Economic indicators, all countries
- CEPAL/ECLAC API - Latin American macroeconomic data
- AfDB API - African Development Bank, 54-country data
- SIPRI datasets - Arms trade, military expenditure structured exports

---

## TECHNICAL ARCHITECTURE

```
Mobile (React Native + Expo)
  ↓ TanStack Query
FastAPI Backend (Railway)
  ↓ Cached briefings
Supabase (PostgreSQL)
  ↑ Weekly cron job
Scraping → LLM Synthesis Pipeline
  ↑ Playwright + Open Router (DeepSeek V4 Flash)
```

**Weekly Pipeline:**
1. Railway Cron triggers scraping (Sunday 06:00 UTC)
2. Playwright scrapes sources → raw articles JSON
3. Multi-model LLM synthesis (DeepSeek V4 Flash primary, V3.2/Kimi K2.5 fallback)
4. Generate BLUF briefing per region with ReportLab PDF
5. Cache in Supabase
6. Mobile apps fetch cached briefing on refresh

---

## COST MODEL

**Operational ceiling**: $20/month  
**Build budget**: < $50 total LLM usage  

**Cost breakdown (estimated):**
- DeepSeek V4 Flash (Open Router): ~$0-1/month (4 briefings × $0.001 = $0.004 typical, 99% reduction vs GPT-4o Mini)
- Railway backend: $5/month (free tier likely sufficient)
- Supabase: $0 (free tier)
- Sentry: $0 (free tier)
- Mixpanel: $0 (free tier)
- Fallback models: $0/month if DeepSeek V4 Flash fails (DeepSeek V3.2/Kimi K2.5, rare)

**Total**: $5-6/month typical, $10/month worst case

---

## v0.1 COMPLETION SUMMARY

**Goal**: Mobile Foundation - Expo app configuration, design system, component library, navigation

**What Shipped**:
- ✅ App configured with SITREP bundle ID (com.pcschmidt.sitrep)
- ✅ Dark mode enforced (AMOLED-optimized)
- ✅ NativeWind + Tailwind CSS configured with design system colors
- ✅ Design tokens file (colors, typography, spacing, regions)
- ✅ Component library: BriefingCard, RegionTab, BLUFSection, DisclaimerBanner, SourceCitation
- ✅ Expo Router file-based navigation (home, detail, about screens)
- ✅ Mock briefing data and TypeScript types
- ✅ Dependencies: Expo Router, NativeWind, TanStack Query, Zustand, react-native-pdf
- ✅ TypeScript strict mode with NativeWind types

**Completion criteria**:
- ✅ App displays military aesthetic dark UI
- ✅ Navigation between screens working
- ✅ Components render placeholder content correctly
- ✅ Git committed cleanly (2 commits)

**Estimated hours**: 8h  
**Actual hours**: ~3h (62% under estimate - efficient component library build)  
**Status**: ✅ COMPLETE (2026-05-22)

---

## v0.2 WORK IN PROGRESS

**Goal**: Scraping Pipeline + LLM Synthesis - Prove end-to-end pipeline works

### v0.2.1 Scraping Pipeline - IN PROGRESS

**What Shipped**:
- ✅ Playwright-based scraper infrastructure (base class, orchestrator, retry logic)
- ✅ ISW scraper fully working (16 articles scraped, 400KB JSON output)
- ✅ JSON schema implemented (source, url, title, date, author, content, region_tags)
- ✅ Automatic region inference from content (Middle East, Indo-Pacific, etc.)
- ✅ Date filtering (7-day rolling window)
- ⏳ Defense One scraper - needs selector fixes
- ⏳ Breaking Defense scraper - needs selector fixes
- ⏳ IISS scraper - needs selector fixes

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
- ✅ At least 1 source scraping successfully
- ✅ JSON output validated
- ✅ Content extraction working (not just metadata)
- ⏳ All 4 sources working (deferred to v0.3+)

**Estimated hours**: 8h  
**Actual hours**: ~4h (50% under estimate - one source sufficient for v0.2.2)  
**Status**: ✅ SUFFICIENT FOR v0.2.2 (2026-05-23)

---

### v0.2.2 LLM Synthesis - COMPLETE

**Goal**: Generate BLUF-format briefing using multi-model waterfall

**What Shipped**:
- ✅ Open Router client with automatic model fallback
- ✅ Multi-model waterfall: DeepSeek V4 Flash → DeepSeek V3.2 → Kimi K2.5 (99% cost reduction)
- ✅ BLUF synthesizer with professional military intelligence format
- ✅ System prompt engineered for BLUF output (JSON schema)
- ✅ Markdown code fence parsing for robust JSON extraction
- ✅ Test synthesis successful: Europe/Africa briefing generated

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
- ✅ LLM integration working
- ✅ BLUF format validated
- ✅ Source citations present
- ✅ Output saved to JSON
- ✅ Cost under $20/month ceiling

**Estimated hours**: 12h  
**Actual hours**: ~3h (75% under estimate - prompt worked on first iteration)  
**Status**: ✅ COMPLETE (2026-05-23)

---

## v0.2 OVERALL SUMMARY

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

**Status**: ✅ COMPLETE (2026-05-23)

---

## v0.3 PDF Generation Backend - COMPLETE

**Goal**: Generate professional PDF briefings from BLUF JSON

**What Shipped**:
- ✅ ReportLab-based PDF generator (Windows-compatible)
- ✅ Military aesthetic with amber (#FFA500) styling
- ✅ Cover page with classification markings and AI disclaimer
- ✅ BLUF summary with highlighted formatting
- ✅ Detailed sections with source citations
- ✅ GET /briefing/latest/pdf API endpoint
- ✅ POST /briefing/generate-pdf API endpoint

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
- ✅ PDF generation working
- ✅ Professional military aesthetic
- ✅ API endpoint serving PDFs
- ✅ Windows compatibility verified
- ✅ Output validated (3 pages, proper formatting)

**Estimated hours**: 8h  
**Actual hours**: ~2h (75% under estimate - ReportLab simpler than HTML/CSS templates)  
**Status**: ✅ COMPLETE (2026-05-23)

---

## v0.6 Backend API - COMPLETE

**Goal**: FastAPI REST endpoints for scraping, synthesis, and briefing retrieval

**What Shipped**:
- ✅ POST /scrape endpoint (triggers ISW scraper orchestrator)
- ✅ POST /synthesize endpoint (generates BLUF briefing from articles)
- ✅ GET /briefing/latest endpoint (returns cached briefing JSON)
- ✅ POST /briefing/generate-pdf endpoint (generates PDF from briefing)
- ✅ GET /briefing/latest/pdf endpoint (serves PDF file)
- ✅ File-based caching (data/briefings/, data/pdfs/)
- ✅ Comprehensive API test suite

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
- ✅ POST /scrape working
- ✅ POST /synthesize working
- ✅ GET /briefing/latest working
- ✅ API endpoints tested end-to-end
- ✅ Local backend fully functional
- ⏸️ Supabase deferred to deployment gate

**Estimated hours**: 8h  
**Actual hours**: ~4h (50% under estimate - endpoints simpler than expected)  
**Status**: ✅ COMPLETE (2026-05-23)

---

## v0.7 Mobile-Backend Integration - COMPLETE

**Goal**: Connect mobile app to FastAPI backend with React Query for data fetching

**What Shipped**:
- ✅ TanStack Query setup (QueryClientProvider with offline-first config)
- ✅ API client (mobile/api/client.ts) with network IP configuration (10.0.0.201:8001)
- ✅ Backend data transformation (BLUF format → mobile Briefing type)
- ✅ React Query hooks (mobile/hooks/useBriefings.ts) for data fetching
- ✅ Updated index.tsx with real API calls replacing mock data
- ✅ Updated detail/[id].tsx with dynamic briefing fetching
- ✅ Loading states (ActivityIndicator) for all async operations
- ✅ Error handling with user-friendly messages
- ✅ Offline support (5min stale time, 10min cache time, auto-retry)

**Technical Details**:
- API base URL configured for local network testing (not localhost)
- Transform function maps backend sections/sources to mobile format
- Query keys structure: `['briefings', 'all-regions']` and `['briefings', 'region', region]`
- Error messages guide user to check backend availability
- Region filtering works client-side on cached data

**Integration Verified**:
- ✅ Backend accessible on local network (http://10.0.0.201:8001/health)
- ✅ API endpoint returns briefing data (http://10.0.0.201:8001/briefing/latest)
- ✅ TypeScript compilation passes with no errors
- ✅ Mobile code properly configured for network requests

**Testing Status**:
- ✅ API integration verified via curl testing
- ✅ Backend serving data correctly on local network
- ⏸️ E2E mobile testing blocked by Babel configuration issue (`.plugins is not a valid Plugin property`)
- ⏸️ Network connectivity issues (Comcast router) preventing physical device testing

**Deferred**:
- Babel plugin configuration debugging (NativeWind/Reanimated conflict)
- Physical device E2E testing (pending network stability)
- Android emulator E2E testing (pending Babel fix)

**Completion criteria**:
- ✅ TanStack Query configured
- ✅ API client created with fetch functions
- ✅ React Query hooks implemented
- ✅ Mock data replaced with real API calls
- ✅ Loading and error states added
- ✅ Offline caching configured
- ⏸️ End-to-end visual testing (blocked by environment issues)

**Estimated hours**: 6h  
**Actual hours**: ~3h integration work + ~3h environment debugging (Babel, network, emulator setup)  
**Status**: ✅ CODE COMPLETE (2026-05-24) - Testing pending environment resolution

---

## v0.8 PDF Mobile Integration - COMPLETE

**Goal**: Full in-app PDF viewing with Share and Save functionality

**What Shipped**:
- ✅ react-native-pdf library integrated (v7.0.4)
- ✅ react-native-blob-util native module (v0.24.9) with custom development build
- ✅ expo-file-system for PDF download/caching
- ✅ expo-sharing for native share sheet integration
- ✅ Full-screen PDF viewer screen ([mobile/app/pdf/[id].tsx](mobile/app/pdf/[id].tsx))
- ✅ Lazy-loaded PDF component (prevents startup errors)
- ✅ Share button - Opens Android/iOS share sheet (Drive, Gmail, Messages, Print, Bluetooth)
- ✅ Save button - Downloads PDF to device Downloads folder
- ✅ Centered header layout (Share/Save buttons don't overlap gear icon)
- ✅ Loading states and error handling with detailed logging
- ✅ "View as PDF" button added to briefing detail screen

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
- ✅ PDF loads and displays 3-page briefing document
- ✅ Pinch-to-zoom, scrolling, and pagination working
- ✅ Share button opens native share sheet with all system options
- ✅ Save button downloads PDF and shows "Briefing saved to Downloads" alert
- ✅ Header layout centered, no gear icon overlap
- ⚠️ Android backgrounding behavior when Share dialog opens (normal OS behavior)

**Known Limitations**:
- App may be killed by Android when Share dialog is open (OS memory management)
- Requires custom development build (cannot use Expo Go for testing)
- PDF caching uses device storage (expo-file-system cacheDirectory)

**Completion criteria**:
- ✅ PDF viewer displays briefings
- ✅ Share functionality working
- ✅ Save functionality working
- ✅ UI polished (centered buttons, proper spacing)
- ✅ Error handling and logging implemented
- ✅ Backend PDF endpoint accessible and serving valid PDFs

**Estimated hours**: 6h  
**Actual hours**: ~6h (3h initial setup + native module debugging, 2h build time, 1h testing/fixes)  
**Status**: ✅ COMPLETE (2026-05-25)

---

## v0.9 Regional Filtering - COMPLETE

**Goal**: Enable all 4 geographic regions with unique briefings and region filter persistence

**What Shipped**:
- ✅ Backend briefings generated for all 4 regions (Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere)
- ✅ Backend PDFs generated for all 4 regions
- ✅ Mobile region filter persistence with AsyncStorage (remembers user's last selection)
- ✅ Debug PDF test button removed from home screen
- ✅ API endpoints verified working for all regions

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
- ✅ All 4 regions have unique briefings generated
- ✅ Backend API serves all 4 regions correctly
- ✅ Mobile region filter persistence implemented
- ✅ PDFs generated for all 4 regions
- ✅ End-to-end testing verified

**Estimated hours**: 6h  
**Actual hours**: ~6h (2h backend synthesis, 1h PDF generation, 2h mobile AsyncStorage, 1h testing)  
**Status**: ✅ COMPLETE (2026-05-26)

---

## v0.0 COMPLETION SUMMARY

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
- ✅ Mobile app displays "Hello SITREP" on both platforms
- ✅ FastAPI returns `{"status": "ok"}` on GET /health
- ⏳ Supabase connection verified (requires user setup)
- ✅ All dependencies installed without errors
- ✅ Git repo initialized with initial commit
- ✅ Backend server verified running on localhost:8000
- ✅ Mobile dependencies verified (471 packages)
- ✅ Backend dependencies verified (44 packages)
- ✅ OSINT source research complete (80+ sources identified)

**Estimated hours**: 4h (2h raw × 2.0x calibration)  
**Actual hours**: ~4h  
**Status**: ✅ COMPLETE (2026-05-21)
