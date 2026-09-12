# DECISIONS

Architecture decision record for SITREP. Newest entry first. A locked entry changes only through a later entry that supersedes it and says so. This is a solo project: Chris Schmidt is owner, proposer, and approver on every entry.

| | |
| --- | --- |
| Entries | DEC-001 to DEC-015 |
| Latest entry | DEC-015, 2026-09-12 |
| Live API for the 2026-09-12 entries | **https://sitrep-production-6aac.up.railway.app** (v0.21.10) |

## How to use

- New entries take the next number, today's date, and go at the top of the log.
- "Significant" means the decision affects three or more future gates, or is hard to reverse.
- Variable names and file layout inside one component do not need an entry.
- A closed entry is not edited. A later entry supersedes it.
- Entries from 2026-09-12 record fixes made after the briefing storage outage; each names the commit that carried it.

---

## Decision template

## DEC-[NNN] -- [Short title]
Date: [date]
Gate: v[X.X.X]
Owner: Chris Schmidt
Proposed by: Chris Schmidt | Claude Code
Approved by: Chris Schmidt
Decision: [What was decided, in one sentence]
Reason: [Why this over the alternative, in one sentence]
Alternatives considered: [What was rejected and why]
Supersedes: DEC-[NNN] | None
Status: LOCKED

---

## Decisions log

## DEC-015 -- Mobile keeps the last good briefing and parses dates defensively
Date: 2026-09-12
Gate: v0.21.10
Owner: Chris Schmidt
Proposed by: Chris Schmidt
Approved by: Chris Schmidt
Decision: The app shows the cached briefing for a region when the backend returns nothing, and parses `generated_at` defensively so a bad date cannot remove a region.
Reason: A missing or unparseable `generated_at` threw in the client and the whole region disappeared ("No briefings available for this region"), which reads to a user as "no news" rather than "backend problem".
Alternatives considered: failing the request and showing an error (loses readable content that is already on the device).
Supersedes: None
Commits: `9f0327a`, `3131027`
Status: LOCKED

---

## DEC-014 -- Serve the web build from /sitrep and forward deep links
Date: 2026-09-12
Gate: v0.21.8
Owner: Chris Schmidt
Proposed by: Chris Schmidt
Approved by: Chris Schmidt
Decision: Publish the Expo web export at https://pcschmidt.github.io/sitrep/ with `baseUrl: /sitrep`, and forward deep links through `public/404.html` to `/sitrep/?redirect=...`, which the app root layout follows.
Reason: GitHub Pages serves the app from a project subpath, where any deep link outside the root 404s. The forward plus the redirect parameter is the smallest fix that keeps links working.
Alternatives considered: a custom 404 app page that renders the route itself (more moving parts), a user subdomain (not available on this account).
Supersedes: None
Commit: `dccaa1e`
Status: LOCKED

---

## DEC-013 -- Opt-in X-Admin-Token guard on write and debug endpoints
Date: 2026-09-12
Gate: v0.21.8
Owner: Chris Schmidt
Proposed by: Chris Schmidt
Approved by: Chris Schmidt
Decision: Guard `/pipeline/run-weekly`, `/synthesize`, `/synthesize/global`, `/briefing/generate-pdf`, and `/debug/*` with an optional `X-Admin-Token` header. Enforcement is active only while `SITREP_ADMIN_TOKEN` is set on the host; while it is unset, each request logs a warning and is allowed.
Reason: An always-on guard would have locked out the in-app scheduler, `refresh_railway_briefings.py`, and the Actions workflow in the same deploy that added it. Opt-in turns the guard on without a flag day.
Alternatives considered: always-enforced token (breaks every caller until all are updated); no guard (leaves the endpoints open).
Supersedes: None
Commit: `ec4be71`
Known gap: `SITREP_ADMIN_TOKEN` is not set on Railway, so the endpoints are still unauthenticated in production.
Status: LOCKED

---

## DEC-012 -- Generate PDFs on demand and serve them inline
Date: 2026-09-12
Gate: v0.21.10
Owner: Chris Schmidt
Proposed by: Chris Schmidt
Approved by: Chris Schmidt
Decision: `GET /briefing/latest/pdf` loads the newest briefing (Supabase first, `data/briefings/*.json` fallback), rebuilds the PDF when the cached file is missing or older than the briefing's `generated_at`, caches it to `data/pdfs/{slug}_{YYYY-MM-DD}.pdf`, and returns it with `Content-Disposition: inline`.
Reason: PDFs existed only on the ephemeral container disk, so a redeploy broke the PDF button while the text briefings still worked from Supabase. `attachment` also made the browser download the file instead of rendering it in the web iframe, which left the UI stuck on "Loading PDF...".
Alternatives considered: archiving PDFs in object storage (not done; there is still no automated PDF archive); keeping attachment disposition (breaks the web viewer).
Supersedes: The disk-only PDF path from v0.6.
Commits: `a2cd4b6`, `59c9600`
Status: LOCKED

---

## DEC-011 -- Pin supabase 2.31.0 for new-format secret keys
Date: 2026-09-12
Gate: v0.21.9
Owner: Chris Schmidt
Proposed by: Chris Schmidt
Approved by: Chris Schmidt
Decision: Keep `supabase==2.31.0` in `api/requirements.txt` and use the new-format secret key (`sb_secret_...`) in `SUPABASE_SERVICE_KEY`.
Reason: supabase-py 2.9.0 rejects `sb_secret_` keys with "Invalid API key"; 2.16.0 is the first release that accepts them. An unpinned or older client silently loses write access to the briefing store.
Alternatives considered: the legacy JWT `service_role` key (works, but the project now issues the new format); pinning at 2.9.0 (cannot see the key at all).
Supersedes: None
Commit: `cc3d5c9`
Status: LOCKED

---

## DEC-010 -- Briefings live in Supabase; the pipeline writes with the service key
Date: 2026-09-12
Gate: v0.21.8
Owner: Chris Schmidt
Proposed by: Chris Schmidt
Approved by: Chris Schmidt
Decision: Store every briefing in Supabase Postgres and write from the pipeline with `SUPABASE_SERVICE_KEY` (new-format secret key), never with the publishable/anon key.
Reason: With the anon key, writes fail with 42501 "new row violates row-level security policy", and briefings written to the container filesystem were lost on every redeploy. Verified 2026-09-12: all five briefings return 200 after a restart.
Alternatives considered: anon key plus permissive row-level security (rejected: opens writes to anyone holding the publishable key); disk-only JSON (rejected: ephemeral filesystem).
Supersedes: File-based caching from v0.6.
Commit: `f82e11f`
Status: LOCKED

---

## DEC-009 -- DeepSeek V4 Flash + Kimi K2.5 waterfall (99% cost reduction)
Date: 2026-05-23
Gate: v0.6
Owner: Chris Schmidt
Proposed by: Chris Schmidt
Approved by: Chris Schmidt
Decision: Use DeepSeek V4 Flash ($0.001/briefing) as primary, DeepSeek V3.2 ($0.003/briefing) as fallback 1, Kimi K2.5 ($0.009/briefing) as fallback 2
Reason: 99.3% cost reduction vs GPT-4o Mini ($0.15 → $0.001 per briefing) while maintaining quality; all models validated with full BLUF synthesis producing 3-5 section briefings with proper citations
Alternatives considered: GPT-4o Mini ($0.15/briefing, 100x more expensive), DeepSeek V3 Chat ($0.003/briefing, good but V4 Flash is cheaper), Claude Haiku ($0.25/briefing, 250x more expensive)
Supersedes: DEC-008 (original DeepSeek/Kimi proposal was correct direction, refined with actual OpenRouter model IDs and V4 Flash discovery)
Status: LOCKED

---

## DEC-008 -- DeepSeek V3 and Kimi K2.5 as cost-optimized fallbacks
Date: 2026-05-23
Gate: v0.2.2
Owner: Chris Schmidt
Proposed by: Chris Schmidt
Approved by: Chris Schmidt
Decision: Use DeepSeek V3 ($0.014/briefing) and Kimi K2.5 ($0.30/briefing) as fallback models instead of Llama 70B ($2/briefing)
Reason: 99% cost reduction while maintaining quality; DeepSeek V3 offers excellent reasoning and citation accuracy at 1.4 cents per briefing vs $2+ for original fallbacks
Alternatives considered: Llama 3.3 70B (50x more expensive), Claude Haiku only (100x more expensive), OpenRouter free tier (insufficient quality for citations)
Supersedes: None (refines original stack choice)
Status: LOCKED

---

## Pre-seeded template decisions (project start)

Seven entries came from the project template before SCOPE CONFIRMED was locked. They are kept because the reasoning still matters, but three of them describe libraries this project never adopted. Each entry says what the code does today.

## DEC-001 -- FastAPI over Next.js API Routes
Date: [project start]
Gate: v0.0.0
Owner: Chris Schmidt
Decision: Use FastAPI for backend, not Next.js API Routes
Reason: LangGraph agents and SSE streaming exceed serverless function time limits
Alternatives considered: Next.js API routes (simpler but incompatible with agents)
Supersedes: None
Applied: `api/main.py` runs FastAPI on Python 3.11+ under uvicorn on Railway. The stated reason mentions LangGraph, which this project does not use; the practical reason here is the long-running pipeline (about 20 minutes per run) and async scraping, which a serverless function limit would cut off.
Status: LOCKED

## DEC-002 -- SQLAlchemy async with Alembic migrations
Date: [project start]
Gate: v0.0.0
Owner: Chris Schmidt
Decision: Use SQLAlchemy async + Alembic for all database operations
Reason: Type-safe ORM prevents SQL injection; named versioned migrations prevent drift
Alternatives considered: Prisma (Python incompatibility), raw SQL (injection risk)
Supersedes: None
Not adopted: this project has no ORM and no migrations. Briefings are written and read through the supabase-py client (`api/database/supabase_client.py`), and the table layout is managed in the Supabase dashboard. Revisit if the schema needs versioned migrations.
Status: NOT ADOPTED (reviewed 2026-09-12)

## DEC-003 -- postgresql+asyncpg:// prefix, connection strategy
Date: [project start]
Gate: v0.0.0
Owner: Chris Schmidt
Decision: DATABASE_URL uses postgresql+asyncpg:// prefix. For MVP, use port 5432 (direct
connection). If pooling is needed at scale, use port 6543 with statement_cache_size=0 in
the SQLAlchemy engine AND append ?pgbouncer=true to the DATABASE_URL.
Reason: SQLAlchemy async requires asyncpg driver. Supabase port 6543 uses PgBouncer in
transaction mode, which breaks asyncpg's default prepared statements
(DuplicatePreparedStatementError at engine init). Port 5432 direct connection works
out of the box. The pooler requires disabling prepared statement caching explicitly.
Alternatives considered: postgres:// prefix (incompatible with asyncpg driver), port 6543
with default asyncpg settings (crashes on startup)
Supersedes: None
Not adopted: no SQLAlchemy engine and no asyncpg in this project. `api/requirements.txt` installs no database driver; supabase-py talks to the REST endpoint over HTTPS.
Status: NOT ADOPTED (reviewed 2026-09-12)

## DEC-004 -- RLS on all user-specific tables from day one
Date: [project start]
Gate: v0.2.0
Owner: Chris Schmidt
Decision: Enable RLS on every table containing user data at migration time
Reason: Data isolation must be at database level, not application level
Alternatives considered: Application-level filtering (error-prone, bypassed by bugs)
Supersedes: None
Applied: row-level security is on. This is why anon-key writes fail with 42501 and the pipeline uses `SUPABASE_SERVICE_KEY` - see DEC-010.
Status: LOCKED

## DEC-005 -- Voyage AI over OpenAI embeddings
Date: [project start]
Gate: v0.4.0+ (when embeddings needed)
Owner: Chris Schmidt
Decision: Use Voyage AI voyage-finance-2 for financial text, voyage-3 for general
Reason: Finance-specific model produces more accurate semantic search for transactions
Alternatives considered: OpenAI text-embedding-3-small (general purpose, less accurate)
Supersedes: None
Not adopted: the project has no embeddings and no vector search. Retrieval is keyword and region tagging over scraped articles.
Status: NOT ADOPTED (reviewed 2026-09-12)

## DEC-006 -- /clear over /compact for context resets
Date: [project start]
Gate: All
Owner: Chris Schmidt
Decision: Always use /clear for context resets, never /compact
Reason: /clear is lossless (save to PLANS.md first); /compact is lossy (retains 20-30%)
Alternatives considered: /compact (convenient but destroys architectural context)
Status: LOCKED

## DEC-007 -- Local development port configuration
Date: [project start]
Gate: v0.0.0
Owner: Chris Schmidt
Decision: Configure BACKEND_PORT_LOCAL in CONTRACT.md to avoid port conflicts
Reason: Port 8000 (or other commonly blocked port) is blocked on the Windows 11 development machine
Alternatives considered: Port 8000 (or other commonly blocked port) (blocked), unblocking via netsh (not persistent)
Status: LOCKED

---

## Where to read next

- [README.md](README.md) - overview, live URLs, and how to run the project
- [CONTRACT.md](CONTRACT.md) - the locked fields these decisions produced
- [SPEC.md](SPEC.md) - what ships in v0.21.10
- [VERSION_ROADMAP.md](VERSION_ROADMAP.md) - which gate carried each entry
