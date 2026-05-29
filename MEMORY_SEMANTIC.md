# MEMORY_SEMANTIC.md
# Blueprint v11 | Persistent Patterns Across Projects
# Updated at gate close when a pattern is validated or invalidated.

## PATTERNS
# Format:
# ### PAT-[NNN]: [title]
# Confidence: LOW | MEDIUM | HIGH
# Source: [project where first observed]
# Description: [pattern]
# Last validated: [date]

### PAT-001: RSS-first scraping strategy
Confidence: HIGH
Source: SITREP v0.11
Description: Always probe for RSS/Atom feeds before writing HTML selector scrapers. Most
quality publications have feeds. RSS is faster, more stable, and zero maintenance versus
HTML scraping which breaks whenever a site redesigns. If a source has no RSS and is
paywalled, check for a free equivalent before attempting CloakBrowser.
Last validated: 2026-05-29

### PAT-002: Docker + Playwright deployment on Railway
Confidence: HIGH
Source: SITREP v0.10
Description: Deploying FastAPI + Playwright to Railway: use Dockerfile not nixpacks.
nixpacks fails with non-standard system deps (Chromium). Dockerfile must include
`RUN playwright install chromium` explicitly after `pip install playwright`. Paths
must be relative to the container working directory, not the script location.
Build takes ~3 minutes; budget for 2-3 deploy iterations to get it right.
Last validated: 2026-05-26

### PAT-003: Analytics service wrapper pattern (React Native)
Confidence: HIGH
Source: SITREP v0.13
Description: Create a single `services/analytics.ts` wrapper that abstracts SDK calls
rather than calling SDKs directly in screens. Wrap with graceful no-ops when tokens
are missing (use `EXPO_PUBLIC_` prefix env vars). Dynamic import for Mixpanel prevents
startup crashes. `Sentry.wrap()` on the root layout component captures native crashes.
Rebuild required to activate native modules — code is ready before rebuild.
Last validated: 2026-05-29

### PAT-004: ReactNode for mixed JSX children
Confidence: HIGH
Source: SITREP v0.14
Description: React component props typed as `children: string` will fail TypeScript
when JSX children contain expressions like `{'\n\n'}` — JSX creates a string array,
not a string. Always type children-accepting components as `children: ReactNode`
(import from 'react'). `import type { ReactNode } from 'react'` is the clean pattern.
Last validated: 2026-05-29

### PAT-005: Free intelligence APIs before scrapers
Confidence: MEDIUM
Source: SITREP v0.15
Description: Before building a scraper for a new domain (geopolitical intelligence,
financial data, scientific literature), probe for free structured APIs first. GDELT
covers global news with zero auth. World Bank, CEPAL, AfDB have REST APIs for
economic data. These are faster to integrate, more stable, and often richer than
scraped HTML. Rate limits on free APIs are IP-based and usually reset daily.
Last validated: 2026-05-29

### PAT-006: LLM region/category field preservation
Confidence: HIGH
Source: SITREP (region name bug, fixed v0.11)
Description: When an LLM is asked to produce JSON with a field that mirrors an input
parameter (e.g. `"region": "Europe/Africa"`), it will sometimes shorten or rephrase
the value. Never trust the LLM to preserve exact string values — always override the
field after JSON parsing: `briefing['region'] = region`. Apply this pattern to any
field that must exactly match an input parameter.
Last validated: 2026-05-29
