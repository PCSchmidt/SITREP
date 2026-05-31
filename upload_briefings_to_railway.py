#!/usr/bin/env python3
"""
Upload local multi-source briefings to Railway/Supabase.
Use this if Railway's pipeline saves are failing.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json
from pathlib import Path

RAILWAY_URL = "https://sitrep-production-6aac.up.railway.app"

def upload_briefing(region: str):
    """Upload a briefing for a specific region"""
    print(f"\nUploading {region}...")

    try:
        response = requests.post(
            f"{RAILWAY_URL}/debug/upload-briefing",
            params={"region": region},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Success: {data.get('article_count')} articles")
            return True
        else:
            print(f"  ✗ Failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("UPLOAD LOCAL BRIEFINGS TO RAILWAY")
    print("=" * 60)

    # Check Supabase status first
    print("\nChecking Supabase status...")
    try:
        response = requests.get(f"{RAILWAY_URL}/debug/supabase", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"  Supabase enabled: {data.get('enabled')}")
            print(f"  Client initialized: {data.get('client_initialized')}")
            print(f"  Current briefings: {data.get('briefings_count')}")
            print(f"  Regions: {data.get('sample_regions', [])}")
        else:
            print(f"  Warning: Status check failed ({response.status_code})")
    except Exception as e:
        print(f"  Error checking status: {e}")

    # Upload all regions
    regions = ["Europe/Africa", "Middle East", "Indo-Pacific", "Western Hemisphere", "Global"]

    print(f"\nUploading {len(regions)} briefings...")

    success_count = 0
    for region in regions:
        if upload_briefing(region):
            success_count += 1

    print(f"\n{'=' * 60}")
    print(f"Upload complete: {success_count}/{len(regions)} successful")
    print(f"{'=' * 60}")

    # Verify
    print("\nVerifying upload...")
    try:
        response = requests.get(f"{RAILWAY_URL}/debug/supabase", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"  Briefings in Supabase: {data.get('briefings_count')}")
            print(f"  Regions: {data.get('sample_regions', [])}")
    except Exception as e:
        print(f"  Error verifying: {e}")

if __name__ == "__main__":
    main()
