# SPEC.md
# Blueprint v11 | Project Specification
# Written during SCOPE CONFIRMED phase. Updated at each gate close.

## PROJECT

**App name**: SITREP  
**Current gate**: v0.0  
**Status**: AWAITING SCOPE CONFIRMED  
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

### Infrastructure
- ✅ FastAPI backend on Railway
- ✅ Supabase for briefing caching
- ✅ CloakBrowser for stealth scraping (bypasses paywalls)
- ✅ Multi-model LLM synthesis (Gemini → Llama → Claude fallback via Open Router)
- ✅ Cost-optimized: single cached briefing per week served to all users

### Monitoring & Analytics
- ✅ Mixpanel for user behavior tracking
- ✅ Sentry for crash reporting and error tracking
- ✅ Weekly automation monitoring with failure alerts

### Compliance
- ✅ Privacy Policy
- ✅ Terms of Service
- ✅ App Store and Play Store approval
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

**Tier 1 (v0.1-v0.2):**
- ISW (Institute for the Study of War) - Ukraine/Russia, Iran analysis
- Defense One - Pentagon insider news, military tech
- Breaking Defense - Emerging defense tech, procurement
- IISS (International Institute for Strategic Studies) - Strategic analysis

**Tier 2 (future expansion):**
- CSIS - Policy analysis
- Janes - Equipment specs (may require CloakBrowser)
- Reuters, Al Jazeera, BBC - General geopolitical
- GTAC Intelligence Hub - Aggregated defense data
- PizzINT - Real-time geopolitical intel feed

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
  ↑ CloakBrowser + Open Router
```

**Weekly Pipeline:**
1. Railway Cron triggers scraping (Sunday 06:00 UTC)
2. CloakBrowser scrapes 4 sources → raw articles JSON
3. Multi-model LLM synthesis (Gemini primary, Llama/Claude fallback)
4. Generate BLUF briefing per region
5. Cache in Supabase
6. Mobile apps fetch cached briefing on refresh

---

## COST MODEL

**Operational ceiling**: $20/month  
**Build budget**: < $50 total LLM usage  

**Cost breakdown (estimated):**
- Gemini 2.0 Flash: $0 (free tier 1,500 req/day)
- Railway backend: $5/month (free tier likely sufficient)
- Supabase: $0 (free tier)
- Sentry: $0 (free tier)
- Mixpanel: $0 (free tier)
- Open Router fallback: ~$2-5/month if Gemini limits hit

**Total**: $5-10/month typical, $20/month worst case

---

## v0.0 ACTIVE TASKS

**Goal**: Foundation setup - project scaffolding, dependencies, repo structure

**Tasks**:
1. Initialize React Native + Expo project (TypeScript, Expo Router)
2. Set up FastAPI backend directory structure
3. Install core dependencies:
   - Mobile: `expo-router`, `nativewind`, `@tanstack/react-query`, `zustand`
   - Backend: `fastapi`, `supabase-py`, `playwright` (CloakBrowser)
4. Configure Supabase project (database + connection)
5. Set up Git repository structure (mobile/, api/, docs/)
6. Write basic README with project overview
7. Verify mobile app runs on iOS Simulator and Android Emulator
8. Verify FastAPI server starts on localhost:8000

**Completion criteria**:
- ✅ Mobile app displays "Hello SITREP" on both platforms
- ✅ FastAPI returns `{"status": "ok"}` on GET /health
- ✅ Supabase connection verified (test query succeeds)
- ✅ All dependencies installed without errors
- ✅ Git repo initialized with initial commit

**Estimated hours**: 4h (2h raw × 2.0x calibration)
