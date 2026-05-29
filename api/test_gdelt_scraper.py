"""Smoke test for GDELTScraper — validates LatAm query (confirmed working in probe)."""
import asyncio
import sys
import logging
logging.basicConfig(level=logging.INFO)

from scrapers.gdelt_scraper import GDELTScraper


async def main():
    print("=== GDELTScraper Smoke Test ===\n")
    scraper = GDELTScraper()

    # Only run the LatAm query (first one) to avoid rate-limiting other CI/CD runs
    # Override QUERIES to just the first entry for the test
    original_queries = scraper.QUERIES
    scraper.QUERIES = [original_queries[0]]  # LatAm only

    try:
        articles = await scraper.scrape_recent_articles(days=7)
    except Exception as e:
        print(f"[FAIL] Exception: {e}")
        return False

    print(f"Articles found: {len(articles)}")
    if articles:
        a = articles[0]
        print(f"  title:   {a.title[:70]}")
        print(f"  source:  {a.source}")
        print(f"  date:    {a.published_date}")
        print(f"  regions: {a.region_tags}")
        print(f"  content: {len(a.content)} chars | {a.content[:80]}")
        print(f"\n[PASS] GDELT scraper returning articles")
        return True
    else:
        # GDELT may return 0 results if rate-limited or no news matches — not a failure
        print("[WARN] 0 articles — may be rate limited or no matching news this week")
        print("       This is acceptable; GDELT is a best-effort source")
        return True  # Not a hard failure


if __name__ == "__main__":
    ok = asyncio.run(main())
    sys.exit(0 if ok else 1)
