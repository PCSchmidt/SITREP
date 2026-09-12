"""Regression tests for the opt-in admin token guard on write endpoints."""

import asyncio
import os
import sys

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("apscheduler")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main  # noqa: E402  (path setup must happen first)


class _FakeRequest:
    class url:  # noqa: N801 - mimic starlette's attribute
        path = "/pipeline/run-weekly"


def _call(header_value, env_value):
    """Run the guard and return "allowed" or "status:<code>"."""
    if env_value is None:
        os.environ.pop(main.ADMIN_TOKEN_ENV, None)
    else:
        os.environ[main.ADMIN_TOKEN_ENV] = env_value

    try:
        asyncio.run(main.require_admin_token(_FakeRequest(), header_value))
    except Exception as exc:  # HTTPException
        return f"status:{getattr(exc, 'status_code', 'error')}"
    finally:
        os.environ.pop(main.ADMIN_TOKEN_ENV, None)

    return "allowed"


@pytest.mark.parametrize(
    "header,env,expected",
    [
        (None, None, "allowed"),            # unconfigured host stays open
        ("anything", None, "allowed"),      # header ignored while unconfigured
        (None, "secret123", "status:401"),  # configured host requires the header
        ("wrong", "secret123", "status:403"),
        ("secret123", "secret123", "allowed"),
        ("secret123", "  secret123  ", "allowed"),  # env value is trimmed
    ],
)
def test_require_admin_token(header, env, expected):
    assert _call(header, env) == expected


def test_guarded_endpoints_are_exactly_the_mutating_ones():
    def guarded(route):
        return any(
            getattr(getattr(dep, "dependency", None), "__name__", "") == "require_admin_token"
            for dep in getattr(route, "dependencies", []) or []
        )

    scanned = {
        route.path: guarded(route)
        for route in main.app.routes
        if getattr(route, "methods", None) and getattr(route, "path", "").startswith("/")
    }

    assert {path for path, is_guarded in scanned.items() if is_guarded} == {
        "/scrape",
        "/synthesize",
        "/synthesize/global",
        "/briefing/generate-pdf",
        "/pipeline/run-weekly",
        "/debug/supabase",
        "/debug/upload-briefing",
    }
    # The mobile app reads these without a token.
    for path in ("/", "/health", "/briefing/latest", "/briefing/global", "/briefing/latest/pdf"):
        assert scanned[path] is False
