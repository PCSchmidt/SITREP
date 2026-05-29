"""Probe GDELT DOC 2.0 API - validate query syntax and response format."""
import json
import urllib.request
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; SITREP intelligence aggregator)'}
GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def query_gdelt(description, query, days=7, max_records=5):
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
    print(f"Query: {query}")

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
        data = json.loads(raw)
        articles = data.get("articles", [])
        print(f"Results: {len(articles)} articles")
        for a in articles[:3]:
            print(f"  title:   {a.get('title', '')[:70]}")
            print(f"  domain:  {a.get('domain', '')}")
            print(f"  country: {a.get('sourcecountry', '')}")
            print(f"  lang:    {a.get('language', '')}")
            print(f"  date:    {a.get('seendate', '')}")
            print(f"  url:     {a.get('url', '')[:60]}")
            print()
        return articles
    except Exception as e:
        print(f"  ERROR: {e}")
        return []


def main():
    print("=== GDELT DOC 2.0 API Probe ===")

    # Test 1: Latin America with source country filter
    query_gdelt(
        "Latin America - source country filter",
        "military conflict security government "
        "(sourcecountry:BR OR sourcecountry:CO OR sourcecountry:VE OR sourcecountry:AR)"
    )

    # Test 2: Africa - source country filter
    query_gdelt(
        "Africa - source country filter",
        "military conflict security coup peacekeeping "
        "(sourcecountry:KE OR sourcecountry:ZA OR sourcecountry:NG OR sourcecountry:ET)"
    )

    # Test 3: Pacific Islands / Oceania
    query_gdelt(
        "Pacific Islands - source country filter",
        "military security China sovereignty Pacific maritime "
        "(sourcecountry:FJ OR sourcecountry:PG OR sourcecountry:AU OR sourcecountry:NZ)"
    )

    # Test 4: Southeast Asia
    query_gdelt(
        "Southeast Asia - source country filter",
        "military security maritime ASEAN sovereignty "
        "(sourcecountry:PH OR sourcecountry:VN OR sourcecountry:ID OR sourcecountry:TH)"
    )

    # Test 5: Check date field format
    query_gdelt(
        "Date format check - any recent military news",
        "military conflict security",
        days=2,
        max_records=2
    )

    print("\nDone.")


if __name__ == "__main__":
    main()
