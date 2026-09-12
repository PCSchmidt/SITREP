#!/usr/bin/env python3
"""Trigger one clean briefing regeneration on Railway.

The backend pipeline now clears stale scraped snapshots before saving the
current run, so a single manual pipeline trigger is enough to refresh content
after deploying freshness fixes.
"""

import argparse
import json
import os
import sys

import requests


DEFAULT_API = "https://sitrep-production-6aac.up.railway.app"


def main() -> int:
    parser = argparse.ArgumentParser(description="Trigger a clean SITREP briefing refresh on Railway.")
    parser.add_argument("--api", default=DEFAULT_API, help="Base SITREP API URL")
    parser.add_argument("--timeout", type=int, default=1500, help="Request timeout in seconds")
    parser.add_argument(
        "--token",
        default=os.getenv("SITREP_ADMIN_TOKEN", ""),
        help="Admin token sent as the X-Admin-Token header (defaults to $SITREP_ADMIN_TOKEN)",
    )
    args = parser.parse_args()

    url = f"{args.api.rstrip('/')}/pipeline/run-weekly"
    print(f"Triggering clean briefing regeneration via {url}")

    token = (args.token or "").strip()
    headers = {"X-Admin-Token": token} if token else None

    try:
        response = requests.post(url, timeout=args.timeout, headers=headers)
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return 1

    try:
        payload = response.json()
    except ValueError:
        print(f"Non-JSON response ({response.status_code}):")
        print(response.text[:2000])
        return 1

    summary = {
        "http_status": response.status_code,
        "status": payload.get("status"),
        "successful_regions": payload.get("successful_regions"),
        "failed_regions": payload.get("failed_regions"),
        "scraping": payload.get("scraping"),
        "errors": payload.get("errors"),
        "global_briefing": payload.get("global_briefing"),
    }
    print(json.dumps(summary, indent=2))

    return 0 if response.ok and payload.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())