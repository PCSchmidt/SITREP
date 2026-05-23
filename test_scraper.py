# Quick test script for scrapers
import sys
sys.path.insert(0, 'api')

import asyncio
from api.scrapers.orchestrator import ScraperOrchestrator


async def test_scraper():
    """Quick test of scraping pipeline"""
    orchestrator = ScraperOrchestrator()

    print("Testing scraping pipeline (limited to 2 articles per source for speed)...")

    # Run scrapers
    results = await orchestrator.scrape_all_sources(days=7)

    # Print summary
    summary = orchestrator.get_summary(results)
    print("\n=== SCRAPING TEST RESULTS ===")
    print(f"Total articles: {summary['total_articles']}")
    print(f"By source: {summary['by_source']}")
    print(f"By region: {summary['by_region']}")
    print("=============================\n")

    # Show sample article
    for source_name, articles in results.items():
        if articles:
            article = articles[0]
            print(f"\nSample from {source_name}:")
            print(f"  Title: {article.title}")
            print(f"  URL: {article.url}")
            print(f"  Date: {article.published_date}")
            print(f"  Regions: {article.region_tags}")
            print(f"  Content length: {len(article.content)} chars")
            break

    # Save results
    if summary['total_articles'] > 0:
        orchestrator.save_all_results(results)
        print("\n✅ Results saved to data/scraped/")
    else:
        print("\n⚠️  No articles scraped - check logs for errors")


if __name__ == "__main__":
    asyncio.run(test_scraper())
