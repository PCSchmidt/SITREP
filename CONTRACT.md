# CONTRACT.md
# Blueprint v11 | Project Contract
# Fill this out during SCOPE CONFIRMED phase. Lock all fields before GO.
# Once LOCKED, fields only change via new DECISIONS.md entry, which
# also triggers re-doing SCOPE CONFIRMED.

---

## PROJECT IDENTITY

PROJECT_NAME:          SITREP
PROJECT_VERSION:       v0.15.0
BUILD_TYPE:            PRODUCTION
FINAL_VERSION:         v1.0 Production Live
CLIENT_TYPE:           PERSONAL
CLIENT_CODE:           N/A
TEAM_MODE:             false
START_DATE:            2026-05-21
TARGET_LAUNCH_DATE:    2026-08-21 (3 months)

---

## TECH STACK (locked after SCOPE CONFIRMED)

MOBILE:                React Native + Expo (TypeScript strict)
STYLING:               NativeWind (Tailwind for React Native) + dark theme
NAVIGATION:            Expo Router
STATE_MANAGEMENT:      TanStack Query + Zustand
PDF_VIEWING:           react-native-pdf
BACKEND:               FastAPI Python 3.11+
DATABASE:              Supabase (PostgreSQL + Blob Storage for PDFs)
SCRAPING:              Playwright (CloakBrowser optional for paywalled sources)
PDF_GENERATION:        ReportLab (programmatic PDF generation)
AUTH:                  None (v1.0) | Supabase Auth (v1.1+)
AI_ROUTING:            Open Router (multi-model waterfall)
AI_PRIMARY_MODEL:      deepseek/deepseek-v4-flash ($0.10/$0.20 per 1M tokens)
AI_FALLBACK_1:         deepseek/deepseek-v3.2 ($0.25/$0.38 per 1M tokens)
AI_FALLBACK_2:         moonshotai/kimi-k2.5 ($0.40/$1.90 per 1M tokens)
AI_COST_TARGET:        ~$0.001/briefing (99% reduction vs GPT-4o Mini)
EMBEDDINGS:            None
OBSERVABILITY:         Mixpanel (analytics) + Sentry (crash tracking)
AUTOMATION:            Railway Cron (weekly briefing + PDF generation)
BILLING:               None

---

## DEPLOYMENT (locked after SCOPE CONFIRMED)

MOBILE_PLATFORM:       App Store + Google Play Store
BACKEND_PLATFORM:      Railway (free tier)
MOBILE_BUNDLE_ID:      com.pcschmidt.sitrep
BACKEND_URL:           TBD (Railway deployment)
BACKEND_PORT_LOCAL:    8000
DATABASE_PORT:         6543 (pooled)
PORTFOLIO_URL:         https://pcschmidt.github.io

---

## LLM SYNTHESIS PIPELINE

SYNTHESIS_MODEL:       Multi-model waterfall (Open Router)
SYNTHESIS_PURPOSE:     Scrape → Analyze → Generate BLUF-format intelligence briefings
SYNTHESIS_FREQUENCY:   Weekly automated (Railway Cron)
SYNTHESIS_REGIONS:     Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere
SYNTHESIS_OUTPUT:      JSON briefing cached in Supabase, served to all users
COST_OPTIMIZATION:     Single cached briefing per week (no per-user generation)

---

## CONSTRAINTS (hard limits that never change)

OPERATIONAL_COST_CEILING:  $20/month total (not per-user)
BUILD_COST_TARGET:         < $50 total LLM usage during development
FREE_APP:                  No monetization (portfolio piece)
MIN_TEST_COVERAGE:         70% line coverage (pytest + vitest)
ACCESSIBILITY:             WCAG AA minimum
UPDATE_FREQUENCY:          Weekly automated briefing generation
CONTENT_DISCLAIMERS:       Heavy AI-generated warnings (like LOWDOWN)

---

## BANNED TECHNOLOGIES

The following are explicitly banned on this project:
(Claude Code must never suggest or use these)

| Technology | Use Instead | Reason |
|-----------|-------------|--------|
| Per-user LLM generation | Cached weekly briefing | Violates cost ceiling |
| Daily briefing updates | Weekly updates | Cost and complexity |
| Social media scraping | News outlet scraping | Unreliable, moderation burden |
| Real-time news streaming | Weekly batch generation | Cost and complexity |
| Custom LLM fine-tuning | Prompt engineering | Unnecessary for synthesis task |
| Video/multimedia scraping | Text-only articles | Bandwidth and scope creep |
| User auth in v1.0 | Auth deferred to v1.1 | Faster v1.0 ship date |

---

## HOOKS STATUS

CO_AUTHOR_HOOK:        INSTALLED
ENFORCE_TESTS_HOOK:    INSTALLED
BLOCK_DANGEROUS_HOOK:  INSTALLED
CONTEXT_CHECK_HOOK:    INSTALLED
WRITETHRU_HOOK:        INSTALLED

---

## VISUAL VERIFICATION

VISUAL_CHECKS_ENABLED: true
SCREENSHOTS_PATH:      /mockups/screenshots/
MOBILE_DEV_PLATFORM:   Expo Go (iOS Simulator + Android Emulator)
EXPO_DEV_URL:          exp://localhost:8081

---

## STATUS

Contract status: **SCOPE CONFIRMED** ✅ (updated with PDF feature)
Last updated: 2026-05-21
Updated by: Chris Schmidt
Locked by: User approval received (re-confirmed after PDF addition)

---

## PORTFOLIO GOALS

**Primary Showcase Skills**:
- ✅ Mobile development (React Native + Expo for iOS/Android)
- ✅ Backend engineering (FastAPI + Python)
- ✅ Web scraping (CloakBrowser stealth scraping)
- ✅ LLM orchestration (multi-model synthesis with cost optimization)
- ✅ Production deployment (App Store + Play Store approval)
- ✅ Monitoring & analytics (Sentry + Mixpanel)

**Target Audience**: Defense/aerospace recruiters, full-stack engineering roles requiring AI integration

**Success Criteria**:
- App live on App Store and Play Store with 100+ downloads
- Professional demo screenshots on pcschmidt.github.io
- Documented architecture decisions showing cost-conscious engineering
- Clean, tested codebase ready for code review
