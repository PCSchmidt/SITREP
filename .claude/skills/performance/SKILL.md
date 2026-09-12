---
name: performance
description: "This skill audits frontend load speed, backend response time, and database query performance. Use before production deployments, at gate close, or when the user types /performance."
---

# Performance

Audits page load, API latency, and query time. Invoke: `/performance`; also auto-triggered pre-deploy.

## TARGETS

Frontend (Lighthouse): Performance 90+, Accessibility 95+, Best Practices 95+
Backend: P50 < 200ms (non-AI), P95 < 500ms, AI endpoints < 3s to first token
Database: No query over 100ms, all FKs indexed

Two deliberate exceptions:
- `POST /pipeline/run-weekly` is a ~20-minute job, not a latency target. Trigger it with a short client timeout - the client gives up and the server finishes.
- `GET /briefing/latest/pdf` takes a few seconds after a redeploy, because the PDF is regenerated and cached to `data/pdfs/` on demand.

## LIGHTWEIGHT GATE CLOSE CHECK

Add response time assertions to the test suite for new endpoints.

## FULL PRE-DEPLOY AUDIT

```bash
# Web app Lighthouse (the Expo web export is served from GitHub Pages)
npx lighthouse https://pcschmidt.github.io/sitrep/ --output=json --quiet

# Database slow query check
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC
LIMIT 10;
```

## AUTO-FIXES

CRITICAL (blocks deploy): N+1 queries, missing indexes on FK columns
HIGH: queries over 500ms, Lighthouse below 80
MEDIUM: queries 100-500ms, Lighthouse 80-90
