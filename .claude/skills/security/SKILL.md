---
name: security
description: "This skill runs security audits at gate close and before production deployments. Use when checking for vulnerabilities, before deploying, or when the user types /security. Covers OWASP Top 10 and AI-specific threats."
---

# Security

OWASP Top 10 plus the SITREP-specific checks. Invoke: `/security`; also auto-triggered pre-deploy.

## WHEN TO RUN

- Lightweight check: every gate close
- Full audit: before every production deploy (mandatory)
- On demand: /security

## LIGHTWEIGHT GATE CLOSE CHECK

```bash
# Check for hardcoded secrets (backend is api/, app code is mobile/)
grep -rn "sk-\|sb_secret" api/ mobile/ --include="*.py" --include="*.ts" --include="*.tsx" | grep -v ".env" | grep -v "test"
grep -rn "password\s*=\s*[\"']" api/ --include="*.py"

# Check for SQL injection patterns
grep -rn "f\"SELECT\|f'SELECT\|format.*SELECT" api/ --include="*.py"
```

## SITREP-specific checks

- **The Supabase service key never leaves the server.** `SUPABASE_SERVICE_KEY` (`sb_secret_...`) bypasses row-level security, so it belongs only in Railway's service variables. Clients may ship the publishable/anon key (`SUPABASE_KEY`) and nothing else; grep a change for `sb_secret` before merging. They are not in the mobile bundle: check `mobile/` and the web export for any embedded key.
- **Writes need the service key.** With the anon key, inserts fail with `42501 new row violates row-level security policy` while the pipeline still reports success. `GET /debug/supabase` reports `key_role` and should read `service_role`; the regression test is `api/tests/test_supabase_key.py`.
- **Write and debug routes are unauthenticated in production today.** `SITREP_ADMIN_TOKEN` is not set on Railway, so the `X-Admin-Token` guard logs a warning and allows the request. Setting the variable is the fix; until then treat `/scrape`, `/synthesize`, `/synthesize/global`, `/briefing/generate-pdf`, `/pipeline/run-weekly`, `/debug/supabase`, and `/debug/upload-briefing` as public and never put a secret behind one.
- **The guard contract is pinned by tests.** `api/tests/test_admin_auth.py` fails if a mutating route is added without `require_admin_token`, or if a route the mobile app reads (`/`, `/health`, `/briefing/latest`, `/briefing/global`, `/briefing/latest/pdf`) gets guarded.
- **Live hosts to include in a review:** https://sitrep-production-6aac.up.railway.app (API) and https://pcschmidt.github.io/sitrep/ (web app).

## FULL PRE-DEPLOY AUDIT (OWASP Top 10)

A01 Broken Access Control:
  - [ ] All routes have auth dependency
  - [ ] RLS enabled on all user-specific tables
  - [ ] No user can access another user's data (RLS isolation test)

A02 Cryptographic Failures:
  - [ ] No secrets in code, git history, or logs
  - [ ] JWT secret is minimum 32 characters
  - [ ] HTTPS enforced

A03 Injection:
  - [ ] All queries use ORM (no raw SQL with f-strings)
  - [ ] All user inputs validated via Pydantic v2
  - [ ] No eval(), exec(), or subprocess with user input

A05 Security Misconfiguration:
  - [ ] DEBUG=false in production
  - [ ] CORS_ORIGINS lists only known domains (no wildcard *)

A07 Auth Failures:
  - [ ] JWT verification on all protected endpoints
  - [ ] Token expiry handled gracefully

AI-Specific:
  - [ ] Cost ceiling enforced per user
  - [ ] Query count tracked and limited
  - [ ] Prompt injection mitigated (user input never directly in system prompt)
  - [ ] Agent log captures all invocations for audit

## AUTO-FIXES

CRITICAL and HIGH: Claude Code fixes autonomously.
MEDIUM: fix before next gate.
LOW: document, address later.
