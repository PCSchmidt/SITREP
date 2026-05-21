# SITREP

**AI-Powered Intelligence Briefing Platform**

SITREP delivers military-grade geopolitical intelligence briefings to mobile devices. It scrapes open-source defense publications (ISW, Defense One, IISS, Breaking Defense), synthesizes them using multi-model LLM pipelines, and presents weekly threat assessments in professional BLUF (Bottom Line Up Front) format—the same structure used by military intelligence products.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Platform](https://img.shields.io/badge/platform-iOS%20%7C%20Android-lightgrey)
![Status](https://img.shields.io/badge/status-v0.0.0%20Foundation-orange)

---

## 🎯 Project Overview

**Build Type**: Production / GA (App Store + Play Store deployment)  
**Timeline**: 3 months (~114-124 hours)  
**Current Gate**: v0.0 Foundation  
**Portfolio**: [pcschmidt.github.io](https://pcschmidt.github.io)

### Key Features (v1.0)

- ✅ Weekly automated intelligence briefing generation
- ✅ BLUF format with cited sources from Tier 1 defense publications
- ✅ Regional filtering (Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere)
- ✅ **PDF export** - Auto-generated professional 15-20 page reports
- ✅ **PDF viewing** - In-app viewer with share/save functionality
- ✅ Dark military aesthetic UI (AMOLED-optimized, near-black + amber accents)
- ✅ Full analytics and crash monitoring (Mixpanel + Sentry)
- ✅ Heavy AI-generated content disclaimers (compliance)

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Git**
- **Expo CLI** (`npm install -g expo-cli`)
- **iOS Simulator** (Mac) or **Android Emulator**
- **Supabase** account

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
│   └── .env.example     # Environment template
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
- **Framework**: React Native + Expo
- **Language**: TypeScript (strict mode)
- **Navigation**: Expo Router
- **Styling**: NativeWind (Tailwind for React Native)
- **State**: TanStack Query + Zustand
- **PDF Viewing**: react-native-pdf

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: Supabase (PostgreSQL + Blob Storage)
- **Scraping**: CloakBrowser (Playwright wrapper)
- **PDF Generation**: WeasyPrint
- **LLM**: Multi-model via Open Router
  - Primary: Gemini 2.0 Flash (free tier)
  - Fallback 1: Llama 3.3 70B
  - Fallback 2: Claude Haiku (BYOK)

### DevOps
- **Hosting**: Railway (backend), App Store/Play Store (mobile)
- **Analytics**: Mixpanel (user behavior)
- **Monitoring**: Sentry (crash tracking)
- **Automation**: Railway Cron (weekly briefings)

---

## 📋 Development Roadmap

**Current Gate**: v0.0 Foundation ✅

| Version | Gate | Status |
|---------|------|--------|
| v0.0 | Foundation | ⏳ In Progress |
| v0.1 | Scraping Pipeline | 📅 Planned |
| v0.2 | LLM Synthesis | 📅 Planned |
| v0.3 | PDF Generation Backend | 📅 Planned |
| v0.4-v0.14 | ... | 📅 Planned |
| v1.0 | Production Live | 📅 Planned |

See [VERSION_ROADMAP.md](VERSION_ROADMAP.md) for detailed gate descriptions.

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

**Status**: v0.0.0 Foundation (2026-05-21)  
**Next**: v0.1 Scraping Pipeline  
**Target Launch**: 2026-08-21
