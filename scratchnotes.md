CLAUDE_CHAT: "https://claude.ai/chat/c4acd191-899d-46c3-84eb-8cabcb8354ba"

PROMPT: "https://github.com/PCSchmidt/CloakBrowser
I have this document that looks like it is created from an automated template. I want to recreate and enhance this idea, perhaps using the CloakBrowser to access information for the newsletter."
RESPONSE:"Let me check out your CloakBrowser repo to understand what you're working with.Good — got a clear picture of both the document and the tool. Let me think through this before diving in.

**What the Lowdown is:** An AI-generated open-source OSINT newsletter with a clean template — executive summary, regional BLUFs, structured sub-sections, cited sources, embedded maps/charts. Published by a military ops support squadron.

**What CloakBrowser is:** A stealth Playwright/Puppeteer wrapper around a patched Chromium binary — drops bot detection so you can scrape paywalled or protected news sites without getting blocked.

Here's how I'd architect this as a portfolio-worthy project:

---

## The Architecture

**Stack:**
- **CloakBrowser** — stealth scraping of news sources (Reuters, Defense One, ISW, Al Jazeera, etc.)
- **FastAPI backend** — orchestrates scraping jobs, feeds Claude API
- **Claude API** — takes raw scraped articles, synthesizes into the Lowdown format (BLUF, sub-sections, sourcing)
- **Next.js or React frontend** — renders the newsletter with a nice UI, region tabs, download to PDF

**Pipeline:**

```
Scheduler → CloakBrowser scrapes sources → 
  Raw text → Claude synthesizes by region → 
    Structured JSON → Frontend renders → 
      PDF export (optional)
```

---

## Key Design Decisions

**Source list (open, scrapeable):**
- ISW (isw.org) — Ukraine/Iran assessments
- Defense One — military tech
- Reuters/Al Jazeera — geopolitics
- Breaking Defense, Stars and Stripes, The Aviationist
- IISS publications

**Claude prompt structure** — the Lowdown's format is very consistent and actually ideal for structured prompting:
- System prompt defines the BLUF + bullet format, tone, citation style
- Each region gets a separate synthesis call with the scraped articles for that beat
- Final call assembles the executive summary across regions

**What makes this a strong portfolio piece:**
- Agentic scraping pipeline (CloakBrowser orchestration)
- Claude function-calling / structured outputs
- Real-world data, not toy examples
- Touches RAG (retrieval of fresh articles), summarization, and document generation
- Ties directly into your defense aerospace work context

---

## Want me to build this out?

I can start with whichever layer is most useful:

1. **The scraper** — Python FastAPI service using CloakBrowser to pull from the target source list, extracting article text cleanly
2. **The Claude synthesis pipeline** — prompt engineering to replicate the Lowdown format with proper BLUFs, sections, and sourcing
3. **The frontend** — a React/Next.js newsletter viewer with region tabs and the military-aesthetic design from the PDF
4. **End-to-end scaffold** — all three wired together

Which would you like to start with?"
PROMPT: "Naming SITREP for app. Mobile app deplorable on android and ios stores. Enhancements beyond whatever was used to create the original LOWDOWN. Control and minimize costs. Need security, high tech, very high end feel UI, low latency, etc. I set up a repo, SITREP. Will use claude code package in vscode for build. Where to START?"
RESPONSE: "Smart approach — Claude Code in VSCode is the right tool for this. Let me help you think through the starting point strategically before writing a single line of code.

## The Right Starting Order

For a mobile app going to the App Store / Play Store, your stack choice at the start locks in everything else. Here's the decision tree:

---

## Stack Decision First

**React Native + Expo** is the clear call for your requirements:
- Single codebase → iOS + Android
- Expo's managed workflow handles app store submission complexity
- Expo Router for navigation
- Works perfectly with your existing React/Next.js muscle memory
- Large ecosystem, active community

**Alternative:** Flutter — great UI performance but Dart is a context switch and the ecosystem is thinner for your use case.

**Recommendation: React Native + Expo (TypeScript)**

---

## Backend

Since you're already thinking Railway/Render for AeroIntel:
- **FastAPI (Python)** — same backend pattern, Claude API calls, scraping orchestration
- **Railway** for deployment — simple, cost-controlled
- **Supabase** for auth + database — free tier is generous, built-in row-level security, real-time subscriptions

---

## Cost Control Architecture

The Lowdown appears to run on a **scheduled batch job**, not real-time. That's the right model:
- Generate the SITREP once per day (or on-demand with a refresh button)
- Cache the output in Supabase — users read cached content, not live Claude calls
- Claude only fires when a new edition is generated
- This keeps costs to ~1-2 API calls per edition per region, not per user

---

## Where to Actually Start

```
Week 1: Foundation
  └── Expo project scaffolded (TypeScript)
  └── FastAPI backend skeleton
  └── Supabase project + auth configured
  └── Claude synthesis pipeline (core value)
  └── One region working end-to-end

Week 2: Mobile UI
  └── The high-end military aesthetic
  └── Region tabs, BLUF cards, expandable sections
  └── Source citation drawer

Week 3: Scraping + Pipeline
  └── CloakBrowser integration
  └── Source list + scheduling
  └── Cost monitoring

Week 4: Store prep
  └── App signing, icons, splash screens
  └── Store listings
```

---

## TODAY — Literal First Commands

When you open VSCode with Claude Code:

**1. Init the Expo app:**
```bash
npx create-expo-app@latest sitrep --template blank-typescript
cd sitrep
```

**2. Init the backend alongside it:**
```bash
mkdir sitrep-api
cd sitrep-api
uv init  # or pip + venv
```

**3. Set up your repo structure:**
```
SITREP/
├── mobile/          # Expo app
├── api/             # FastAPI
├── docs/            # Architecture notes
└── .github/         # CI/CD later
```

**4. First Claude Code prompt** (paste this in after scaffolding):

> "I'm building SITREP, a military-aesthetic mobile news intelligence app in React Native + Expo TypeScript. The app synthesizes open-source news into structured intelligence reports (BLUF format) using the Claude API. Set up the project structure, install core dependencies (Expo Router, NativeWind for styling, React Query for data fetching), and create a placeholder home screen with a dark military UI theme. The color palette should be near-black backgrounds, amber/gold accents, sharp typography — think AMOLED-ready high-contrast."

---

## One Critical Decision to Make Now

**Authentication model:**
- **Option A:** No auth, free app, editions are public — simplest, fastest to ship
- **Option B:** Supabase auth, users create accounts — enables personalization, notifications, saved editions
- **Option C:** Passkey / magic link only — high security feel, no password friction

Given the "high-end security feel" requirement, Option B or C makes sense and Supabase handles it with minimal code.

What's your call on auth, and do you want me to generate the full project scaffold + first Claude Code session plan?"
PROMPTS: "Describe the app for the repo description"
RESPONSE: "**SITREP** — AI-powered open-source intelligence platform delivering classified-feel daily threat assessments and geopolitical briefings to mobile. Structured like a professional intelligence product: executive summaries, regional BLUFs, cited sourcing, and real-time world event synthesis — built on Claude AI, React Native, and FastAPI."