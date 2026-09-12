# VERSION_ROADMAP

Gate-by-gate history of SITREP from v0.0 to v0.21.11, with the remaining work for v1.0. Every row below except the current one is history; read each Status cell as of that gate's date, not as today.

| | |
| --- | --- |
| Current version | v0.21.11 (`APP_VERSION` in `api/main.py`) |
| Live API | **https://sitrep-production-6aac.up.railway.app** |
| Web app | https://pcschmidt.github.io/sitrep/ |
| Next gate | v1.0 Production Live - Google Play submission, then Apple App Store |
| Facts checked | 2026-09-12 |

## Build type

**Production / GA**

Ends at: **v1.0 Production Live**. Store order changed after SCOPE CONFIRMED: Google Play first, then Apple App Store.

## Calibration multiplier

Multiplier applied to raw estimates: **1.0x** (revised from 2.0x default)
Source: 9 completed gates with actual hour data. SITREP consistently runs
under estimate - average variance is -35% (faster than predicted). Raw
estimates have proven accurate; no inflation needed for this project type.

Recorded around v0.16 and not recalculated since. Treat the multiplier as history.

## Roadmap

Near-term gates (typically v0.0 through v0.3 or the first third of
total gates) have single-number estimates. Later gates have ranges
with a note on what drives the uncertainty.

Hours are as recorded when each gate closed. Nothing in this table is the current state; the current build is v0.21.11.

| Version | Gate Name | Goal | Est Hours | Actual Hours | Status |
|---------|-----------|------|-----------|--------------|--------|
| v0.0 | Foundation | Project scaffolding, repo structure, dependencies installed (React Native + Expo, FastAPI, Playwright). Git configured, basic README. | 4h | 4h | DONE |
| v0.1 | Mobile Foundation | Expo app configured (bundle ID, dark mode), NativeWind + design system setup, component library built (BriefingCard, RegionTab, BLUFSection, DisclaimerBanner, SourceCitation), Expo Router navigation, placeholder screens with mock data. | 8h | 3h | DONE |
| v0.2 | Scraping Pipeline | Playwright scraping integrated, ISW working (16 articles). Raw article extraction working, stored as JSON. CloakBrowser not needed for open sources. | 8h | 4h | DONE |
| v0.2 | LLM Synthesis | Multi-model pipeline via Open Router (DeepSeek V4 Flash → V3.2 → Kimi K2.5 fallback, 99% cost reduction). Takes scraped articles → outputs BLUF-format briefing for one region (Europe/Africa). Prompt engineering validated. | 12h | 3h | DONE |
| v0.3 | **PDF Generation Backend** | **ReportLab integrated for programmatic PDF generation. Generates professional 3-page PDF from briefing JSON with military aesthetic. GET /briefing/latest/pdf endpoint working.** | **8h** | **2h** | **DONE** |
| v0.4 | Mobile Scaffold | React Native + Expo app initialized. Expo Router navigation working. Placeholder screens (Home, Briefing Detail, About). App runs on iOS Simulator and Android Emulator. | 6h | - | Not run as a separate gate. The work shipped inside v0.1 |
| v0.5 | UI Design System | Military aesthetic design system: dark theme, typography, color palette (near-black + amber accents), reusable components (BriefingCard, RegionTab, SourceCitation). Mockups approved. | 10h | - | Not run as a separate gate. The design system and components shipped inside v0.1; see DESIGN_SYSTEM.md |
| v0.6 | Backend API | FastAPI endpoints: POST /scrape, POST /synthesize, GET /briefing/latest. Supabase connection working, briefings cached in DB. Local backend fully functional. | 8h | 4h | DONE |
| v0.7 | Mobile-Backend Integration | Mobile app fetches cached briefing from FastAPI. TanStack Query setup. Loading states, error handling, vertical region tabs with improved UX. Custom development build with native modules. | 6h | 8h | DONE |
| v0.8 | **PDF Mobile Integration** | **react-native-pdf installed with custom Expo development build. Full-screen PDF viewer screen with lazy-loading. Share/Save functionality working. UI improvements: horizontal header layout, larger region fonts, proper spacing. All PDF actions tested and functional.** | **6h** | **6h** | **DONE** |
| v0.9 | **Regional Filtering** | **Backend briefings and PDFs generated for all 4 regions (Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere). Mobile region filter persistence with AsyncStorage. All API endpoints verified working. Debug button removed. TypeScript compilation passes.** | **6h** | **6h** | **DONE** |
| v0.10 | **Production Deployment** | **(The Railway weekly cron described here was replaced by the in-app daily scheduler in v0.19.)** **Railway deployment with Nixpacks, Supabase caching, Railway cron job for weekly automation. Production URL configured in mobile app. Backend fully deployed and operational at <https://sitrep-production-6aac.up.railway.app>. Cron triggers /pipeline/run-weekly every Sunday 6 AM UTC. Mobile app fully functional: development build with USB connection, regional briefings displaying, detail screens working, PDF viewer integrated (loads Railway backend PDFs). RegionTab layout fixed (removed ScrollView conflict). All navigation flows tested on physical device (Samsung S25+).** | **10h** | **16h** | **DONE** |
| v0.11 | **Source Expansion** | **RSSBaseScraper base class (stdlib XML + httpx, no new deps). Defense One, Breaking Defense rewritten to RSS. War on the Rocks added (replaces paywalled IISS). The War Zone + Al Jazeera added. 6 working scrapers, ~84 articles/week (was 16). CloakBrowser path documented for post-v1.0 expansion.** | **12-16h** | **12h** | **DONE** |
| v0.12 | **Global Briefing** | **GET /briefing/global + synthesize_global() with cross-regional system prompt (thematic sections: Great Power Competition, Energy Coercion, Alliance Dynamics). ALL tab uses useGlobalBriefing() hook. Weekly pipeline generates global briefing as Step 4. Debug console.logs removed.** | **6h** | **5h** | **DONE** |
| v0.13 | **Analytics Integration** | **@sentry/react-native + mixpanel-react-native installed. services/analytics.ts wrapper with graceful degradation. 5 events instrumented: app_open (_layout), briefing_view (detail), region_filter (index), pdf_view + pdf_share (pdf). Root wrapped with Sentry.wrap(). Tokens via EXPO_PUBLIC_ env vars. Rebuild required to activate native modules.** | **6h** | **4h** | **DONE** |
| v0.14 | **Legal & Disclaimers** | **PRIVACY_POLICY.md + TERMS_OF_SERVICE.md. In-app privacy.tsx + terms.tsx screens. About screen rewritten with stronger disclaimer + nav links. DisclaimerBanner updated. PDF gets per-page footer disclaimer on every page via onFirstPage/onLaterPages hooks. TypeScript clean.** | **4h** | **3h** | **DONE** |
| v0.15 | **GDELT Integration** | **GDELTScraper using free GDELT DOC 2.0 API (no auth). 3 queries: LatAm (BR/CO/MX/AR/VE/CU/PE/CL), sub-Saharan Africa (ZA/KE/NG/ET/GH/TZ/CI/SN), SE Asia+Oceania (ID/PH/VN/TH/MY/MM/AU/NZ/FJ/PG). Parenthesized OR syntax confirmed via live probe. Returns local-language sources machine-translated to English. 30s delays + exponential backoff on 429. Best-effort: 0 articles gracefully if rate-limited.** | **4-6h** | **4h** | **DONE** |
| v0.16 | **App Store Prep** | **EAS account + eas init, analytics tokens (Mixpanel + Sentry), privacy policy hosted at pcschmidt.github.io/sitrep/, icons verified (1024×1024), splash config updated for SDK 56, React version fixed (19.2.3), Sentry plugin removed, expo-doctor passes. App fully functional on device.** | **6h** | **8h** | **DONE** |
| v0.17 | **Beta Testing** | **RSS scraper reliability fix (urllib→httpx). 7 sources working: ISW, Defense One, War on the Rocks, The War Zone, Al Jazeera, Foreign Policy, CFR (109 articles total). Multi-source briefings synthesized for all regions. Western Hemisphere now has content (12 articles, 5 sources). Navigation bug fixed (unique briefing IDs). Android preview APK tested on Samsung S25+. Screenshots taken.** | **8-16h** | **10h** | **DONE** |
| v0.18 | **Source Expansion II / Feed Revival** | **Revived dead economic + think-tank feeds via Google News RSS proxy (Reuters, Bloomberg, World Bank, Brookings, Carnegie; CSIS native). Guardian API + US/UK government scrapers folded in as proper BaseScraper subclasses (Article.from_dict normalizer). GDELT corrected to FIPS 10-4 country codes + OR-wrapped keyword queries (was silently returning 0) with headline fallback on content-fetch timeout. Result: 13 scrapers, ~540 articles/run (was 7 sources / 109).** | **6-8h** | **6h** | **DONE** |
| v0.19 | **Daily Automation + Reliability** | **Pipeline cadence moved weekly→daily (internal APScheduler, 06:00 UTC). Per-scraper asyncio timeout (60s default, per-scraper override; ISW Playwright domcontentloaded). Model-waterfall hardened: null-content raises so fallback fires; max_tokens raised (regional 12k, global 16k); (response_text or "").strip() guards. Deterministic source-URL back-fill with isinstance guards.** | **4-6h** | **5h** | **DONE** |
| v0.20 | **Composite Global Briefing** | **The "ALL"/Global view now stitches all four regional briefings in full (regions[] → full PDF; sections[] region-prefixed → app) plus a best-effort cross-regional executive summary, rather than a thin condensed mega-synthesis. Falls back to stitched regional BLUFs if global synthesis fails. ≈4 regions / 19 sections / 120 articles. The 2026-09-12 run measured 17 Global sections, 120 articles, and 30 articles per regional desk.** | **4-6h** | **4h** | **DONE** |
| v0.21 | **Executive PDF Redesign** | **New pdf_generator_v3 (editorial aesthetic): PT Serif + Lato embedded TTFs, navy/hairline palette, two-column cover (Contents + Executive Summary), numbered hyperlinked per-section sources, composite multi-region rendering, defensive mojibake repair. Old v1/v2/reportlab generators removed. Mobile PDF cache fix (cache:false) + hardened region parsing so PDFs never pin stale/old-design files. Repo cleanup: untracked .pyc/data artifacts, broadened .gitignore, test scripts → api/scripts/, docs reconciled to v0.21.** | **6-8h** | **8h** | **DONE** |
| v0.21.5-7 | **Content Freshness & WH Fixes** | **HOTFIXES: v0.21.5 (mobile null-check for generated_at), v0.21.6 (GDELT rate limiting: 30s delays, exponential backoff 45s→90s→180s, timeout 150s→300s), v0.21.7 (Western Hemisphere keyword expansion: added 14 terms including argentina/chile/peru/ecuador/bolivia/panama/guatemala/honduras/nicaragua/southcom/northcom/oas/cartel/narco/drug trafficking/migration/border; disabled unreliable LatAm backup scraper). Result: all 5 regions generating successfully with 30 articles each.** | **—** | **6h** | **DONE** |
| v0.21.8 | **Storage recovery + endpoint guard** | **Briefing caching writes with `SUPABASE_SERVICE_KEY`; anon-key writes fail with 42501 "new row violates row-level security policy", and disk-only briefings died at every redeploy. Opt-in `X-Admin-Token` guard on the pipeline and debug routes. Web app served from /sitrep with 404 deep-link forwarding. `GET /` reports the running version.** | - | - | DONE |
| v0.21.9 | **New-format Supabase keys** | **supabase-py rejects new-format `sb_secret_` keys before 2.16.0; `api/requirements.txt` pins `supabase==2.31.0`. Server stamps `generated_at` on every briefing, because the mobile client formats that field directly and an unparseable value used to hide a whole region.** | - | - | DONE |
| v0.21.10 | **On-demand PDFs, served inline** | **`GET /briefing/latest/pdf` loads the newest briefing (Supabase first), regenerates the PDF when the cached file is missing or older than the briefing, and serves it with `Content-Disposition: inline` so the web iframe renders it instead of downloading. Mobile keeps showing the last good briefing through a backend gap. Verified 2026-09-12: all five briefings and all five PDFs return 200.** | - | - | DONE |
| v0.21.11 | **Calmer provenance copy** | **The amber "AI GENERATED CONTENT" banner is gone: a small grey footer note now states that the cited sources are real and only the paraphrase is machine-written, on both the home and detail screens. The PDF cover and page footers carry the same plain-language note. App copy corrected from weekly to daily generation. Published privacy and terms pages synced with the markdown.** | - | - | DONE (current) |
| v1.0 | Production Live | Target: Google Play submission approved, then Apple App Store. App live and discoverable. Portfolio page (pcschmidt.github.io) updated with store links and screenshots. | 6-12h (depends on review times) | - | pending - next |

**Total Estimated Hours**: ~156-180h (added v0.18-v0.21 post-beta hardening +20-28h)  
**Timeline at 10-15h/week**: 8-12 weeks (~2-3 months)

Only v1.0 is open. The backend is live at v0.21.11; the remaining work is store submission, and no gate after v0.21.11 has started.

## Rules

- No gate is skipped
- Failing tests = do not advance
- Each gate defines exactly what ships and what does NOT ship
- Gates over 6 hours should be split into sub-gates (e.g. v0.5-A, v0.5-B)
- Scope changes require re-doing SCOPE CONFIRMED; do not silently
  edit this file mid-build
- When variance > 30% at a gate close, a heads-up is printed but
  approved ranges are NOT silently edited - the user decides whether
  to re-approve

## Final gate

The final gate is labeled explicitly as one of:
- `v1.0 Production Live` (Production / GA build type)
- `v1.0 Internal GA` (Internal build type)
- `v0.X Prototype Validated` (Exploratory build type, X depends on scope)

---

## Where to read next

- [README.md](README.md) - overview, live URLs, and how to run the project
- [SPEC.md](SPEC.md) - what ships in v0.21.11 and what is deferred
- [PLANS.md](PLANS.md) - the open work behind the v1.0 row
- [DECISIONS.md](DECISIONS.md) - the decisions that produced the last three gates
