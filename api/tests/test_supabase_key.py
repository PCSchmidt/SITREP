"""Regression tests for Supabase key selection.

The backend writes briefings, so it must use the service_role key. Installing the
anon key used to fail writes with "new row violates row-level security policy"
while the pipeline reported success, because file storage hid the failure.
"""

import importlib
import sys
import types

import pytest

pytest.importorskip("dotenv")


@pytest.fixture
def client_module(monkeypatch):
    """Import the client module against a stubbed supabase package."""
    created = []

    fake = types.ModuleType("supabase")

    def create_client(url, key):
        created.append((url, key))
        return types.SimpleNamespace()

    fake.create_client = create_client
    fake.Client = object
    monkeypatch.setitem(sys.modules, "supabase", fake)

    import database.supabase_client as module

    # Reload so the module binds this fixture's stub instead of a previous one.
    module = importlib.reload(module)

    return module, created


def test_service_key_is_preferred(client_module, monkeypatch):
    module, created = client_module
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_KEY", "service-key")
    monkeypatch.setenv("SUPABASE_KEY", "anon-key")

    client = module.SupabaseClient()

    assert client.uses_service_role is True
    assert created[-1] == ("https://example.supabase.co", "service-key")


def test_anon_key_is_a_fallback_and_flags_itself(client_module, monkeypatch):
    module, created = client_module
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.delenv("SUPABASE_SERVICE_KEY", raising=False)
    monkeypatch.setenv("SUPABASE_KEY", "anon-key")

    client = module.SupabaseClient()

    assert client.uses_service_role is False
    assert created[-1] == ("https://example.supabase.co", "anon-key")


def test_blank_service_key_falls_back_to_anon(client_module, monkeypatch):
    module, created = client_module
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_KEY", "   ")
    monkeypatch.setenv("SUPABASE_KEY", "anon-key")

    client = module.SupabaseClient()

    assert client.uses_service_role is False
    assert created[-1] == ("https://example.supabase.co", "anon-key")


def test_missing_credentials_raise(client_module, monkeypatch):
    module, _ = client_module
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.delenv("SUPABASE_SERVICE_KEY", raising=False)
    monkeypatch.delenv("SUPABASE_KEY", raising=False)

    with pytest.raises(ValueError):
        module.SupabaseClient()
