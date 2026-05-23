# SITREP

**AI-Powered Intelligence Briefing Platform**

SITREP delivers military-grade geopolitical intelligence briefings to mobile devices. It scrapes open-source defense publications (ISW, Defense One, IISS, Breaking Defense), synthesizes them using multi-model LLM pipelines, and presents weekly threat assessments in professional BLUF (Bottom Line Up Front) format—the same structure used by military intelligence products.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Platform](https://img.shields.io/badge/platform-iOS%20%7C%20Android-lightgrey)
![Status](https://img.shields.io/badge/status-v0.6.0%20Backend%20API-green)

---

## 🎯 Project Overview

**Build Type**: Production / GA (App Store + Play Store deployment)  
**Timeline**: 3 months (~114-124 hours total)  
**Current Gate**: v0.6 Backend API ✅ COMPLETE  
**Portfolio**: [pcschmidt.github.io](https://pcschmidt.github.io)

### What is SITREP?

SITREP is a mobile intelligence briefing platform that replicates and enhances "The LOWDOWN" - an AI-generated OSINT newsletter format. It automates the collection, synthesis, and presentation of defense and geopolitical intelligence from dozens of premier open-source publications.

**The Problem**: Keeping up with global defense developments requires monitoring 40+ disparate sources, from think tanks (ISW, CSIS, IISS) to trade publications (Defense One, Breaking Defense) to mainstream news. This is time-consuming and overwhelming.

**The Solution**: SITREP automatically scrapes, synthesizes, and summarizes these sources weekly using AI, presenting a single coherent intelligence briefing organized by region (Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere) in professional military BLUF format.

**Why This Project**: Portfolio showcase demonstrating full-stack mobile development, AI/LLM integration, web scraping, backend architecture, and production deployment to public app stores.

---

## ✨ Key Features (v1.0)

### Intelligence Briefing

- ✅ **Weekly automated generation** - Railway Cron triggers Sunday 06:00 UTC
- ✅ **BLUF format** - Bottom Line Up Front military intelligence structure
- ✅ **4 geographic regions** - Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere
- ✅ **Cited sources** - All claims linked to original Tier 1 publications
- ✅ **80+ OSINT sources** - ISW, Defense One, IISS, CSIS, Breaking Defense, Reuters, Al Jazeera, and more
- ✅ **AI-generated content disclaimers** - Heavy compliance focus for App Store approval

### PDF Features

- ✅ **PDF auto-generation** - Professional 15-20 page reports during weekly pipeline
- ✅ **In-app PDF viewer** - Full-screen viewing with pinch-to-zoom
- ✅ **PDF sharing** - iOS/Android share sheet (email, messages, AirDrop)
- ✅ **PDF save/open** - Save to Files app or open in external apps (Adobe, Apple Books)

### Mobile Experience

- ✅ **Dark military aesthetic** - AMOLED-optimized UI (near-black + amber accents)
- ✅ **Regional filtering** - Tab navigation between geographic regions
- ✅ **Offline reading** - Briefings cached locally for offline access
- ✅ **Smooth UX** - Loading states, optimistic updates, error boundaries

### Infrastructure & Cost Optimization

- ✅ **Cost ceiling: $20/month** (target: $5-10/month typical)
- ✅ **Single cached briefing** - One briefing per week served to all users (no per-user generation)
- ✅ **Multi-model LLM waterfall** - GPT-4o Mini (primary) → Claude Haiku → Llama 3.1 70B
- ✅ **Playwright scraping** - Open-source news scraping (CloakBrowser optional for paywalls)
- ✅ **Full analytics & monitoring** - Mixpanel (user behavior) + Sentry (crash tracking)

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Git**
- **Expo CLI** (`npm install -g expo-cli`)
- **iOS Simulator** (Mac) or **Android Emulator**
- **Supabase** account (free tier)

### Installation

```bash
# Clone the repository
git clone https://github.com/PCSchmidt/SITREP.git
cd SITREP

# Install mobile dependencies
cd mobile
npm install

# Install backend dependencies
cd ../api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Supabase and Open Router credentials
```

### Running Locally

**Mobile App:**
```bash
cd mobile
npm start

# Then choose your platform:
# - Press 'i' for iOS Simulator
# - Press 'a' for Android Emulator
# - Scan QR code with Expo Go app
```

**Backend API:**
```bash
cd api
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload --port 8000

# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

---

## 📁 Project Structure

```
SITREP/
├── mobile/              # React Native + Expo mobile app
│   ├── App.tsx          # Main app entry point
│   ├── app.json         # Expo configuration
│   ├── assets/          # Images, fonts, icons
│   └── package.json     # Mobile dependencies
│
├── api/                 # FastAPI backend
│   ├── main.py          # FastAPI app and routes
│   ├── requirements.txt # Python dependencies
│   ├── .env.example     # Environment template
│   └── venv/            # Python virtual environment (gitignored)
│
├── docs/                # Documentation
│
├── .claude/             # Blueprint v11 framework
│   ├── skills/          # Development workflow skills
│   ├── hooks/           # Pre/post tool execution hooks
│   └── agents/          # Specialized subagents
│
├── CONTRACT.md          # Project scope and identity
├── SPEC.md              # Technical specification
├── VERSION_ROADMAP.md   # 16-gate development roadmap
├── DESIGN_SYSTEM.md     # UI/UX design specifications
├── DECISIONS.md         # Architecture decision records
└── README.md            # This file
```

---

## 🛠️ Tech Stack

### Mobile

- **Framework**: React Native + Expo SDK 56
- **Language**: TypeScript (strict mode)
- **Navigation**: Expo Router (file-based routing)
- **Styling**: NativeWind (Tailwind CSS for React Native)
- **State Management**: 
  - TanStack Query v5 (server state, caching, offline-first)
  - Zustand (client state)
- **PDF Viewing**: react-native-pdf
- **Analytics**: Mixpanel SDK
- **Monitoring**: Sentry React Native SDK

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: Supabase (PostgreSQL + Blob Storage for PDFs)
- **Scraping**: Playwright (CloakBrowser optional for paywalled sources)
- **PDF Generation**: ReportLab (programmatic PDF generation)
- **LLM Integration**: Multi-model via Open Router
  - Primary: GPT-4o Mini ($0.15/briefing typical)
  - Fallback 1: Claude 3 Haiku ($0.25/$1.25 per 1M tokens)
  - Fallback 2: Llama 3.1 70B ($0.52/$0.75 per 1M tokens)
- **HTTP**: httpx (async), aiohttp (concurrent scraping)
- **Testing**: pytest, pytest-asyncio, pytest-cov

### DevOps & Infrastructure
- **Backend Hosting**: Railway (Hobby plan, $5/month)
- **Mobile Deployment**: App Store (iOS) + Play Store (Android)
- **Database**: Supabase Free Tier (500MB database, 1GB storage)
- **Analytics**: Mixpanel Free Tier (100k events/month)
- **Monitoring**: Sentry Free Tier (5k errors/month)
- **Automation**: Railway Cron (weekly briefing generation)
- **CI/CD**: GitHub Actions (planned for v0.13+)

---

## 📋 Development Roadmap

**Current Gate**: v0.1 Mobile Foundation ✅

Built using **Blueprint v11** methodology with 16-gate phased development:

| Version | Gate | Description | Hours | Status |
|---------|------|-------------|-------|--------|
| v0.0 | Foundation | Project scaffold, dependencies, documentation | 4h (4h actual) | ✅ COMPLETE |
| v0.1 | Mobile Foundation | App config, design system, component library, screens | 8h (3h actual) | ✅ COMPLETE |
| v0.2 | Scraping Pipeline | Playwright scraping, ISW working (16 articles) | 8h (4h actual) | ✅ COMPLETE |
| v0.2 | LLM Synthesis | GPT-4o Mini via Open Router, BLUF generation | 12h (3h actual) | ✅ COMPLETE |
| v0.3 | PDF Generation Backend | ReportLab PDF generation, 3-page output | 8h (2h actual) | ✅ COMPLETE |
| v0.4 | Mobile Scaffold | (Skipped - completed in v0.1) | - | ⏭️ SKIPPED |
| v0.5 | UI Design System | (Skipped - completed in v0.1) | - | ⏭️ SKIPPED |
| v0.6 | Backend API | FastAPI endpoints, file-based caching | 8h (4h actual) | ✅ COMPLETE |
| v0.7 | Mobile-Backend Integration | TanStack Query, API client, error handling | 6h | 📅 Next |
| v0.8 | PDF Mobile Integration | react-native-pdf, share sheet, save/open | 6h | 📅 Planned |
| v0.9 | Regional Filtering | Tab state, filter logic, empty states | 6h | 📅 Planned |
| v0.10 | Weekly Automation | Railway Cron setup, failure alerts, monitoring | 10h | 📅 Planned |
| v0.11 | Analytics Integration | Mixpanel events, Sentry crash tracking | 6h | 📅 Planned |
| v0.12 | Legal & Disclaimers | Privacy Policy, ToS, AI content warnings | 4h | 📅 Planned |
| v0.13 | App Store Prep | Icons, screenshots, metadata, build signing | 6h | 📅 Planned |
| v0.14 | Beta Testing | TestFlight, internal testing, bug fixes | 8-16h | 📅 Planned |
| v1.0 | Production Live | App Store + Play Store deployment, launch | 6-12h | 📅 Planned |

**Total Estimated**: 114-124 hours over 3 months  
**Target Launch**: 2026-08-21

See [VERSION_ROADMAP.md](VERSION_ROADMAP.md) for detailed gate descriptions and hour breakdowns.

---

## 🏗️ Technical Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Mobile App (React Native)                 │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Region    │  │   Briefing   │  │   PDF Viewer     │   │
│  │   Tabs      │  │   Cards      │  │   (Full Screen)  │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
│          │                 │                    │             │
│          └─────────────────┴────────────────────┘             │
│                         │                                     │
│                  TanStack Query                               │
│                    (Caching Layer)                            │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST API
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Railway)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  GET /briefing/latest → {regions, pdf_url, metadata} │   │
│  │  GET /briefing/latest/pdf → PDF binary               │   │
│  │  POST /scrape (internal cron trigger)                │   │
│  │  POST /synthesize (internal cron trigger)            │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                     │
│                         ↓                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           Supabase (PostgreSQL + Storage)            │    │
│  │  • briefings table (JSON, metadata, timestamp)       │    │
│  │  • Blob storage for generated PDFs                   │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────┬───────────────────────────────────┘
                          │ Railway Cron
                          │ (Sunday 06:00 UTC)
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              Weekly Scraping Pipeline                        │
│  1. Playwright scrapes OSINT sources (ISW, Defense One...)  │
│  2. Extract articles → JSON storage                          │
│  3. Multi-model LLM synthesis (GPT-4o Mini → Claude → Llama)│
│  4. Generate BLUF per region                                 │
│  5. ReportLab generates PDF                                  │
│  6. Cache briefing + PDF in Supabase                         │
└─────────────────────────────────────────────────────────────┘
```

### Weekly Pipeline Flow

```
Sunday 06:00 UTC
    │
    ↓
┌───────────────────────────────────────────────┐
│  Railway Cron triggers POST /scrape           │
└────────────────┬──────────────────────────────┘
                 │
                 ↓
┌───────────────────────────────────────────────┐
│  Playwright Scraping (async, parallel)        │
│  • ISW: Russia/Ukraine analysis               │
│  • Defense One: Pentagon insider news         │
│  • IISS: Strategic assessments                │
│  • Breaking Defense: Tech/procurement         │
│  • CSIS, Reuters, Al Jazeera (40+ total)     │
└────────────────┬──────────────────────────────┘
                 │
                 ↓ Raw articles JSON
┌───────────────────────────────────────────────┐
│  Multi-Model LLM Synthesis                    │
│  Primary: GPT-4o Mini (~$0.15/briefing)       │
│  Fallback: Claude 3 Haiku → Llama 3.1 70B     │
│                                                │
│  Prompt: "Synthesize into 4 regional BLUF     │
│  briefings (Middle East, Indo-Pacific,        │
│  Europe/Africa, Western Hemisphere)"          │
└────────────────┬──────────────────────────────┘
                 │
                 ↓ Structured BLUF JSON
┌───────────────────────────────────────────────┐
│  ReportLab PDF Generation                     │
│  • Programmatic layout with Python API        │
│  • 3-5 pages per region, military aesthetic   │
│  • Source citations, disclaimers              │
└────────────────┬──────────────────────────────┘
                 │
                 ↓ PDF binary
┌───────────────────────────────────────────────┐
│  Supabase Storage                             │
│  • briefings table: JSON + metadata           │
│  • Blob storage: PDF file                     │
│  • Single cached briefing for all users       │
└───────────────────────────────────────────────┘
```

### Data Model

**Supabase `briefings` table:**

```sql
CREATE TABLE briefings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  created_at TIMESTAMP DEFAULT NOW(),
  week_start DATE NOT NULL,
  regions JSONB NOT NULL,  -- {middle_east: {...}, indo_pacific: {...}, ...}
  pdf_url TEXT,            -- Blob storage URL
  source_count INTEGER,    -- Number of articles scraped
  model_used TEXT          -- "gpt-4o-mini" | "claude-3-haiku" | "llama-3.1-70b"
);
```

**Mobile cache (TanStack Query):**

```typescript
{
  queryKey: ['briefing', 'latest'],
  data: {
    id: string,
    created_at: string,
    week_start: string,
    regions: {
      middle_east: {
        bluf: string,
        sections: Array<{title: string, content: string, sources: string[]}>
      },
      // ... other regions
    },
    pdf_url: string,
    source_count: number
  },
  staleTime: 1000 * 60 * 60 * 24 * 7  // 1 week
}
```

---

## 💰 Cost Breakdown & Optimization

**Operational Ceiling**: $20/month  
**Typical Monthly Cost**: $5-10  
**One-Time Build Cost**: <$50 LLM usage

### Monthly Operating Costs

| Service | Tier | Monthly Cost | Notes |
|---------|------|--------------|-------|
| Railway | Hobby | $5 | Backend hosting, cron jobs |
| Supabase | Free | $0 | 500MB DB, 1GB storage, 2GB bandwidth |
| Open Router (GPT-4o Mini) | Pay-as-you-go | $1-2 | ~$0.15/briefing, 4 briefings/month |
| Open Router (Fallbacks) | Pay-as-you-go | $0-1 | Claude/Llama only if GPT fails (rare) |
| Mixpanel | Free | $0 | 100k events/month |
| Sentry | Free | $0 | 5k errors/month |
| **Total** | | **$5-10** | **Worst case: $20 if heavy fallback usage** |

### Cost Optimization Strategies

1. **Single Cached Briefing**: One briefing generated per week, served to ALL users (no per-user generation)
2. **Cost-Optimized LLM**: GPT-4o Mini at ~$0.15/briefing (4 briefings/month = $0.60/month typical)
3. **Waterfall Fallback**: Only pay for Claude/Llama if GPT-4o Mini fails (rare, adds $0-1/month)
4. **Supabase Free Tier**: 500MB database + 1GB blob storage sufficient for 52 briefings/year + PDFs
5. **No User Auth in v1.0**: Deferred to v1.1 to reduce complexity and backend load
6. **Railway Free Trial**: First $5/month free credits reduce effective cost

---

## 🔒 Security & Compliance

### App Store Approval Strategy

- **Heavy AI disclaimers** - Throughout UI and in About screen
- **Source citations** - All claims linked to original publications
- **No medical/legal advice** - Geopolitical analysis only
- **Privacy Policy** - No user data collection in v1.0 (no auth)
- **Terms of Service** - Standard usage terms

### Data Privacy

- **v1.0**: No user authentication → no personal data collected
- **Analytics**: Anonymous device IDs only (Mixpanel)
- **Crash reporting**: Stack traces only, no PII (Sentry)
- **Supabase**: Single cached briefing, no user-specific data

### Scraping Ethics

- **Playwright scraping**: Respectful scraping of open-source news (1 req/second per source)
- **CloakBrowser**: Optional for paywalled sources, not used in current implementation
- **robots.txt**: Honored where present
- **Source attribution**: All scraped content properly cited in briefings

---

## 🧪 Testing Strategy

- **Unit Tests**: pytest for backend (v0.1+)
- **Integration Tests**: FastAPI test client for API endpoints (v0.6+)
- **E2E Tests**: Playwright for scraping pipeline (v0.1+)
- **Mobile Tests**: Jest + React Native Testing Library (v0.7+)
- **TestFlight Beta**: Internal testing before production (v0.14)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 👤 Author

**Chris Schmidt**
- Portfolio: [pcschmidt.github.io](https://pcschmidt.github.io)
- Email: p.christopher.schmidt@gmail.com
- GitHub: [@PCSchmidt](https://github.com/PCSchmidt)

---

## 🙏 Acknowledgments

- **The LOWDOWN** - Original inspiration for BLUF intelligence format
- **Blueprint v11** - Development methodology framework
- **ISW, Defense One, IISS, Breaking Defense** - Premier OSINT sources
- **Anthropic Claude** - Development assistant and fallback LLM

---

**Status**: v0.6.0 Backend API Complete (2026-05-23)  
**Next**: v0.7 Mobile-Backend Integration (TanStack Query + API client)  
**Target Launch**: 2026-08-21 (App Store + Play Store)
