# CONTRACT

Locked project fields for SITREP: identity, stack, constraints, and what is banned. Fields change only through a new entry in [DECISIONS.md](DECISIONS.md). Values below were re-checked against the code on 2026-09-12; the four that had drifted are marked "(corrected 2026-09-12)".

| | |
| --- | --- |
| Contract status | SCOPE CONFIRMED |
| Current version | v0.21.10 |
| Live API | **https://sitrep-production-6aac.up.railway.app** |
| Last field change | 2026-09-12 (storage, keys, deployment URLs) |

---

## Project identity

PROJECT_NAME:          SITREP
PROJECT_VERSION:       v0.21.10                     (corrected 2026-09-12; was v0.15.0)
BUILD_TYPE:            PRODUCTION
FINAL_VERSION:         v1.0 Production Live
CLIENT_TYPE:           PERSONAL
CLIENT_CODE:           N/A
TEAM_MODE:             false
START_DATE:            2026-05-21
TARGET_LAUNCH_DATE:    Not fixed. The 2026-08-21 date passed. Google Play closed testing
                       (20 testers, 14 days) is next, then Apple App Store review.

---

## Tech stack (locked after SCOPE CONFIRMED)

MOBILE:                React Native + Expo SDK ~56.0.8 (TypeScript strict, React Native 0.85.3, React 19.2.3)
STYLING:               NativeWind (Tailwind for React Native) + dark theme
NAVIGATION:            Expo Router ~56.2.8
STATE_MANAGEMENT:      TanStack Query 5.x + Zustand
PDF_VIEWING:           react-native-pdf 7.x on device; <iframe> on web
BACKEND:               FastAPI Python 3.11+, uvicorn on Railway (Docker)
DATABASE:              Supabase Postgres for briefings. PDFs are not stored anywhere;
                       they are rebuilt on demand            (corrected 2026-09-12)
SCRAPING:              Playwright + httpx/RSS (CloakBrowser optional for paywalled sources)
PDF_GENERATION:        ReportLab, pdf_generator_v3 (PT Serif + Lato, two-column cover)
AUTH:                  None (v1.0) | Supabase Auth (v1.1+).
                       Write and debug endpoints take an optional X-Admin-Token header; the
                       guard is enforced only while SITREP_ADMIN_TOKEN is set, and that
                       Railway variable is not set yet          (added 2026-09-12)
AI_ROUTING:            Open Router (multi-model waterfall)
AI_PRIMARY_MODEL:      deepseek/deepseek-v4-flash ($0.10/$0.20 per 1M tokens)
AI_FALLBACK_1:         deepseek/deepseek-v3.2 ($0.25/$0.38 per 1M tokens)
AI_FALLBACK_2:         moonshotai/kimi-k2.5 ($0.40/$1.90 per 1M tokens)
AI_COST_TARGET:        ~$0.001/briefing (99% reduction vs GPT-4o Mini)
EMBEDDINGS:            None
OBSERVABILITY:         Mixpanel (analytics) + Sentry (crash tracking)
AUTOMATION:            Internal APScheduler (daily briefing + PDF generation)
BILLING:               None

---

## Deployment (locked after SCOPE CONFIRMED)

MOBILE_PLATFORM:       Google Play Store next, then Apple App Store   (corrected 2026-09-12)
BACKEND_PLATFORM:      Railway (Docker image, uvicorn + FastAPI)
MOBILE_BUNDLE_ID:      com.pcschmidt.sitrep (Android versionCode 7, iOS buildNumber 1)
BACKEND_URL:           https://sitrep-production-6aac.up.railway.app  (corrected 2026-09-12)
WEB_URL:               https://pcschmidt.github.io/sitrep/
BACKEND_PORT_LOCAL:    8000
DATABASE_PORT:         6543 (pooled)
LEGAL_URLS:            https://pcschmidt.github.io/sitrep/privacy-policy | .../sitrep/terms
PORTFOLIO_URL:         https://pcschmidt.github.io

---

## LLM synthesis pipeline

SYNTHESIS_MODEL:       Multi-model waterfall (Open Router), order fixed in
                       api/synthesis/openrouter_client.py:
                       1. deepseek/deepseek-v4-flash  (~$0.001/briefing)
                       2. deepseek/deepseek-v3.2      (~$0.003/briefing)
                       3. moonshotai/kimi-k2.5        (~$0.009/briefing)
SYNTHESIS_PURPOSE:     Scrape → Analyze → Generate BLUF-format intelligence briefings
SYNTHESIS_FREQUENCY:   Daily automated (Internal APScheduler)
SYNTHESIS_REGIONS:     Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere
SYNTHESIS_OUTPUT:      JSON briefing cached in Supabase, served to all users
COST_OPTIMIZATION:     One cached briefing per day served to every user (no per-user generation)

---

## Constraints (hard limits that never change)

OPERATIONAL_COST_CEILING:  $20/month total (not per-user)
BUILD_COST_TARGET:         < $50 total LLM usage during development
FREE_APP:                  No monetization (portfolio piece)
MIN_TEST_COVERAGE:         70% line coverage target. Actual 2026-09-12: 11 pytest tests
                           in api/tests/ (admin-token guard, Supabase key selection). No
                           mobile test suite
ACCESSIBILITY:             WCAG AA minimum
UPDATE_FREQUENCY:          Daily automated briefing generation
CONTENT_DISCLAIMERS:       AI-generated warnings on every screen and on every PDF page

---

## Banned technologies

The following stay out of this project, whichever tool or contributor suggests them:

| Technology | Use Instead | Reason |
| --- | --- | --- |
| Per-user LLM generation | One cached briefing per day | Violates the $20/month ceiling |
| Real-time news streaming | One daily batch run at 06:00 UTC | Cost and complexity |
| Social media scraping | News outlet, API, and RSS scraping | Unreliable, moderation burden |
| Custom LLM fine-tuning | Prompt engineering with a model waterfall | Unnecessary for this task |
| Video/multimedia scraping | Text-only articles | Bandwidth and scope creep |
| User auth in v1.0 | No auth; Supabase Auth stays deferred | Faster v1.0 ship date |
| Anon key for Supabase writes | `SUPABASE_SERVICE_KEY` in the pipeline | Anon writes fail with 42501 (row-level security) |
| Supabase-py 2.9.0 | `supabase==2.31.0` in `api/requirements.txt` | 2.9.0 rejects new-format `sb_secret_` keys |

---

## Hooks status

These are the template's hook labels. The live configuration is `.claude/settings.json`, which registers SessionStart, PreToolUse, PostToolUse, PreCompact, and Stop hooks.

CO_AUTHOR_HOOK:        INSTALLED
ENFORCE_TESTS_HOOK:    INSTALLED
BLOCK_DANGEROUS_HOOK:  INSTALLED
CONTEXT_CHECK_HOOK:    INSTALLED
WRITETHRU_HOOK:        INSTALLED

---

## Visual verification

VISUAL_CHECKS_ENABLED: true
SCREENSHOTS_PATH:      No `/mockups/screenshots/` directory exists in this repo. Store
                       screenshots are still to be produced (5 screenshots plus a
                       1024x500 feature graphic)
MOBILE_DEV_PLATFORM:   Development build and Android preview APK on a physical device
                       (react-native-pdf does not run in Expo Go)
EXPO_DEV_URL:          exp://localhost:8081

---

## Status

Contract status: **SCOPE CONFIRMED**
Last updated: 2026-09-12
Updated by: Chris Schmidt
Superseded fields: version, database, backend URL, and target launch date were corrected on
2026-09-12 to match the shipped v0.21.10 build. See [DECISIONS.md](DECISIONS.md) DEC-010.

---

## Portfolio goals

**Primary Showcase Skills**:
- [x] Mobile development (React Native + Expo for iOS/Android)
- [x] Backend engineering (FastAPI + Python)
- [x] Web scraping (Playwright, RSS, and public APIs; CloakBrowser never needed)
- [x] LLM orchestration (multi-model waterfall with cost control)
- [ ] Production deployment (Google Play submission next, then Apple App Store)
- [x] Monitoring and analytics (Sentry + Mixpanel)

**Target Audience**: Defense and aerospace recruiters, full-stack engineering roles that need AI integration

**Success Criteria** (targets, not results):
- App live on Google Play and the App Store with 100+ downloads
- Demo screenshots on pcschmidt.github.io
- Documented decisions that show cost-conscious engineering
- Tested codebase that survives a code review

---

## Where to read next

- [README.md](README.md) - overview, live URLs, and how to run the project
- [SPEC.md](SPEC.md) - what ships, what is deferred
- [DECISIONS.md](DECISIONS.md) - dated decisions behind these locked fields
- [VERSION_ROADMAP.md](VERSION_ROADMAP.md) - gate history and what v1.0 still needs

