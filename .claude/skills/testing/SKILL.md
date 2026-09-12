---
name: testing
description: "Test strategy and test commands for SITREP. Use when writing tests, checking coverage, or working a gate close. Invoke: /testing."
---

# Testing

Backend tests live in `api/tests/` and run with pytest. There is no automated test suite for the web or mobile app.

## The command

```bash
cd api && python -m pytest tests -q      # 11 passed, verified 2026-09-12
```

Run it from `api/` and pass `tests` explicitly. A bare `python -m pytest` from `api/` also collects `api/scripts/test_*.py`, which are ad-hoc scraper and synthesis scripts - six of them fail collection and abort the run.

`api/conftest.py` puts `api/` on `sys.path` because the backend uses flat imports (`from scheduler import ...`). The tests call `pytest.importorskip` for `fastapi`, `apscheduler`, and `dotenv`, so a bare interpreter skips instead of crashing.

## What is covered

| File | Tests | Covers |
| --- | --- | --- |
| `api/tests/test_admin_auth.py` | 7 | `require_admin_token`: an unset host stays open, a configured host returns 401/403, the env value is trimmed, and the guarded set is exactly the seven mutating routes |
| `api/tests/test_supabase_key.py` | 4 | `SUPABASE_SERVICE_KEY` is preferred over `SUPABASE_KEY`; an anon-only install flags `uses_service_role = False` |

Not covered: scrapers, synthesis, PDF generation, the mobile app, and the web export. Treat those as manual checks.

## Conventions

- Test naming: `test_[action]_[condition]_[expected_result]`.
- Write the test from the requirement, not from the implementation, so it can fail for the right reason.
- A fixed bug gets a test that fails without the fix. The Supabase key test exists because an anon-key install failed writes with `42501` while the pipeline still reported success.
- Adding a write route means adding it to the guarded-route set in `test_admin_auth.py`; that test fails if a mutating route lacks `require_admin_token`, or if a route the mobile app reads gets guarded.
- Never commit a virtualenv. Local scratch venvs (`.venv-verify`, `.venv-reqtest`) are git-ignored - use one when you need to test a specific package version, then keep it out of the change.

## Gate close checklist

1. `cd api && python -m pytest tests -q` is green: 11 tests, zero failures, no unexplained skips.
2. No test was deleted or skipped to make the suite pass.
3. Coverage target is 70% line coverage (CONTRACT.md). `pytest-cov==6.0.0` is pinned in `api/requirements.txt` but is not installed in the scratch venvs, so coverage is currently unmeasured - install it in the venv you test with if you need the number.
4. Any endpoint the change touches still returns 200 on the live API (see the deployment skill's check list).

## Related

- Repo README: ../../../README.md
- `../deployment/SKILL.md` for the production checks, `../debug/SKILL.md` when a failing test needs root-cause work.
