# VERSION_ROADMAP.md
# Blueprint v11 | Full Version Roadmap
# Generated during SCOPE CONFIRMED phase.
# Covers v0.0 through the final version for this build type.

## BUILD TYPE

**Production / GA**

Ends at: **v1.0 Production Live** (App Store + Play Store deployment)

## CALIBRATION MULTIPLIER

Multiplier applied to raw estimates: **2.0x**
Source: Default (fewer than 3 ESTIMATION entries in MEMORY_CORRECTIONS.md)

## ROADMAP

Near-term gates (typically v0.0 through v0.3 or the first third of
total gates) have single-number estimates. Later gates have ranges
with a note on what drives the uncertainty.

| Version | Gate Name | Goal | Est Hours | Actual Hours | Status |
|---------|-----------|------|-----------|--------------|--------|
| v0.0 | Foundation | Project scaffolding, repo structure, dependencies installed (React Native + Expo, FastAPI, Playwright). Git configured, basic README. | 4h | 4h | ✅ DONE |
| v0.1 | Mobile Foundation | Expo app configured (bundle ID, dark mode), NativeWind + design system setup, component library built (BriefingCard, RegionTab, BLUFSection, DisclaimerBanner, SourceCitation), Expo Router navigation, placeholder screens with mock data. | 8h | 3h | ✅ DONE |
| v0.2 | Scraping Pipeline | Playwright scraping integrated, ISW working (16 articles). Raw article extraction working, stored as JSON. CloakBrowser not needed for open sources. | 8h | 4h | ✅ DONE |
| v0.2 | LLM Synthesis | Multi-model pipeline via Open Router (DeepSeek V4 Flash → V3.2 → Kimi K2.5 fallback, 99% cost reduction). Takes scraped articles → outputs BLUF-format briefing for one region (Europe/Africa). Prompt engineering validated. | 12h | 3h | ✅ DONE |
| v0.3 | **PDF Generation Backend** | **ReportLab integrated for programmatic PDF generation. Generates professional 3-page PDF from briefing JSON with military aesthetic. GET /briefing/latest/pdf endpoint working.** | **8h** | **2h** | **✅ DONE** |
| v0.4 | Mobile Scaffold | React Native + Expo app initialized. Expo Router navigation working. Placeholder screens (Home, Briefing Detail, About). App runs on iOS Simulator and Android Emulator. | 6h | - | pending |
| v0.5 | UI Design System | Military aesthetic design system: dark theme, typography, color palette (near-black + amber accents), reusable components (BriefingCard, RegionTab, SourceCitation). Mockups approved. | 10h | - | pending |
| v0.6 | Backend API | FastAPI endpoints: POST /scrape, POST /synthesize, GET /briefing/latest. Supabase connection working, briefings cached in DB. Local backend fully functional. | 8h | 4h | ✅ DONE |
| v0.7 | Mobile-Backend Integration | Mobile app fetches cached briefing from FastAPI. TanStack Query setup. Loading states, error handling, offline support. API integration complete, E2E testing pending environment fixes. | 6h | 6h | ✅ DONE |
| v0.8 | **PDF Mobile Integration** | **react-native-pdf installed. Full-screen PDF viewer screen. 'View as PDF' button in briefing detail. iOS/Android share sheet integration. Save to Files/Downloads. Open in external apps. All PDF actions working.** | **6h** | **-** | **pending** |
| v0.9 | Regional Filtering | All 4 regions working (Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere). Region tabs in UI, filter briefings by region, navigation polished. | 6h | - | pending |
| v0.10 | Weekly Automation | Railway Cron job triggers weekly scraping → synthesis → PDF generation → cache pipeline. Monitoring/logging for failures. Manual trigger endpoint for testing. Pipeline runs successfully for 2 consecutive weeks. | 10h | - | pending |
| v0.11 | Analytics Integration | Mixpanel SDK integrated (user events: app_open, briefing_view, region_filter, pdf_view, pdf_share). Sentry SDK integrated (crash reporting, error tracking). Telemetry verified in dashboards. | 6h | - | pending |
| v0.12 | Legal & Disclaimers | Privacy policy drafted. Terms of Service drafted. Heavy AI-generated disclaimers in UI (splash screen, briefing header, About page, PDF footer). App store compliance verified. | 4h | - | pending |
| v0.13 | App Store Prep | App icons (1024x1024), splash screens, app store screenshots (iOS + Android showing PDF viewer). App store listing copy written. Bundle IDs configured. Signing certificates ready. | 6h | - | pending |
| v0.14 | Beta Testing | TestFlight (iOS) + Play Store Beta (Android) deployed. 5-10 beta testers recruited. Bug fixes from feedback. PDF generation/viewing tested on real devices. Crash-free rate > 99%. | 8-16h (depends on feedback volume) | - | pending |
| v1.0 | Production Live | App Store submission approved. Google Play Store submission approved. App live and discoverable. Portfolio page (pcschmidt.github.io) updated with app store links and screenshots. | 6-12h (depends on review times) | - | pending |

**Total Estimated Hours**: ~114-124h (added 14h for PDF generation + mobile integration)  
**Timeline at 10-15h/week**: 8-12 weeks (~2-3 months)

## RULES

- No gate is skipped
- Failing tests = do not advance
- Each gate defines exactly what ships and what does NOT ship
- Gates over 6 hours should be split into sub-gates (e.g. v0.5-A, v0.5-B)
- Scope changes require re-doing SCOPE CONFIRMED; do not silently
  edit this file mid-build
- When variance > 30% at a gate close, a heads-up is printed but
  approved ranges are NOT silently edited - the user decides whether
  to re-approve

## FINAL GATE

The final gate is labeled explicitly as one of:
- `v1.0 Production Live` (Production / GA build type)
- `v1.0 Internal GA` (Internal build type)
- `v0.X Prototype Validated` (Exploratory build type, X depends on scope)
