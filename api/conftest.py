"""Pytest configuration for the SITREP backend.

This file exists so pytest adds the ``api`` directory to ``sys.path``: the backend
uses flat imports (``from scheduler import ...``), so tests must run from ``api``
with its own directory importable.
"""
