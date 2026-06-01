"""Smoke test for all v0.11 scrapers - validates each source returns articles."""
import asyncio
import sys
import logging
logging.basicConfig(level=logging.WARNING)  # Suppress debug noise

from scrapers.defenseone_scraper import DefenseOneScraper
from scrapers.breakingdefense_scraper import BreakingDefenseScraper
from scrapers.warontherocks_scraper import WarOnTheRocksScraper
from scrapers.thewarzone_scraper import TheWarZoneScraper
from scrapers.aljazeera_scraper import AlJazeeraScraper


async def test_scraper(scraper, days=7):
    name = scraper.source_name
    try:
        articles = await scraper.scrape_recent_articles(days=days)
        print(f"  [{'PASS' if articles else 'WARN'}] {name}: {len(articles)} articles")
        if articles:
            a = articles[0]
            print(f"         title: {a.title[:70]}")
            print(f"         date:  {a.published_date}")
            print(f"         regions: {a.region_tags}")
            print(f"         content: {len(a.content)} chars | {a.content[:80]}")
        return len(articles)
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
        return 0


async def main():
    print("=== v0.11 Scraper Smoke Test ===\n")
    scrapers = [
        DefenseOneScraper(),
        BreakingDefenseScraper(),
        WarOnTheRocksScraper(),
        TheWarZoneScraper(),
        AlJazeeraScraper(),
    ]

    total = 0
    for scraper in scrapers:
        count = await test_scraper(scraper)
        total += count
        print()

    print(f"Total articles across RSS sources: {total}")
    if total > 0:
        print("RESULT: RSS scrapers working")
    else:
        print("RESULT: No articles found - check feeds")
    return total


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result > 0 else 1)
