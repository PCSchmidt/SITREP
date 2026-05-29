"""GDELT probe v2 - with proper rate limiting and encoding fixes."""
import json
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; SITREP intelligence aggregator)'}
GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
DELAY = 4  # seconds between requests (conservative)


def safe_str(s):
    """ASCII-safe string for Windows console output."""
    return s.encode('ascii', errors='replace').decode('ascii') if s else ''


def query_gdelt(description, query, days=7, max_records=5, retries=2):
    end_dt = datetime.now(timezone.utc)
    start_dt = end_dt - timedelta(days=days)

    params = {
        "query": query,
        "mode": "artlist",
        "maxrecords": str(max_records),
        "startdatetime": start_dt.strftime("%Y%m%d%H%M%S"),
        "enddatetime": end_dt.strftime("%Y%m%d%H%M%S"),
        "format": "json",
    }

    url = f"{GDELT_URL}?{urlencode(params)}"
    print(f"\n=== {description} ===")
    print(f"Query: {safe_str(query)}")

    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = resp.read().decode('utf-8', errors='replace')
            data = json.loads(raw)
            articles = data.get("articles", [])
            print(f"Results: {len(articles)} articles")
            for a in articles[:3]:
                print(f"  title:   {safe_str(a.get('title', ''))[:70]}")
                print(f"  domain:  {safe_str(a.get('domain', ''))}")
                print(f"  country: {safe_str(a.get('sourcecountry', ''))}")
                print(f"  lang:    {safe_str(a.get('language', ''))}")
                print(f"  date:    {safe_str(a.get('seendate', ''))}")
                print()
            return articles
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = (attempt + 1) * 6
                print(f"  Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  HTTP {e.code}: {e}")
                return []
        except Exception as e:
            print(f"  ERROR: {e}")
            if attempt < retries:
                time.sleep(3)
            else:
                return []
    return []


def main():
    print("=== GDELT DOC 2.0 Probe v2 (with rate limiting) ===")

    # Test 1: Broad query first (no country filter) to confirm API works
    r1 = query_gdelt(
        "Test 1: No country filter - broad geopolitics",
        "military conflict security government",
        days=3, max_records=3
    )
    time.sleep(DELAY)

    # Test 2: Single country filter - Brazil (large, active news source)
    r2 = query_gdelt(
        "Test 2: Single country - Brazil",
        "military security government sourcecountry:BR",
        days=7, max_records=5
    )
    time.sleep(DELAY)

    # Test 3: Multiple countries OR syntax
    r3 = query_gdelt(
        "Test 3: LatAm multi-country OR",
        "military conflict security sourcecountry:CO OR sourcecountry:VE OR sourcecountry:AR",
        days=7, max_records=5
    )
    time.sleep(DELAY)

    # Test 4: Africa - Kenya + Nigeria
    r4 = query_gdelt(
        "Test 4: Africa - Kenya + Nigeria",
        "military conflict security coup sourcecountry:KE OR sourcecountry:NG",
        days=7, max_records=5
    )
    time.sleep(DELAY)

    # Test 5: Southeast Asia
    r5 = query_gdelt(
        "Test 5: Southeast Asia",
        "military security maritime sourcecountry:PH OR sourcecountry:VN OR sourcecountry:ID",
        days=7, max_records=5
    )
    time.sleep(DELAY)

    # Test 6: Try FIPS country codes (GDELT sometimes uses these)
    r6 = query_gdelt(
        "Test 6: Pacific (AU + NZ only, simpler)",
        "military security China sovereignty Pacific",
        days=7, max_records=5
    )

    print(f"\nSummary: {sum(len(r) for r in [r1,r2,r3,r4,r5,r6])} total results")


if __name__ == "__main__":
    main()
