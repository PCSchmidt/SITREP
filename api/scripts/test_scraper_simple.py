# Simple scraper test - just test ISW
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.scrapers.isw_scraper import ISWScraper


async def test_isw():
    """Test ISW scraper only"""
    print("Testing ISW scraper...")
    print("=" * 50)

    scraper = ISWScraper()

    try:
        # Scrape recent articles (limit to last 7 days)
        articles = await scraper.scrape_recent_articles(days=7)

        print(f"\n[SUCCESS] Scraped {len(articles)} articles from ISW")

        if articles:
            # Show first article as example
            article = articles[0]
            print(f"\nSample Article:")
            print(f"  Title: {article.title}")
            print(f"  URL: {article.url}")
            print(f"  Published: {article.published_date}")
            print(f"  Author: {article.author}")
            print(f"  Regions: {', '.join(article.region_tags)}")
            print(f"  Content length: {len(article.content)} characters")
            print(f"  Content preview: {article.content[:200]}...")

            # Save to JSON
            filepath = scraper.save_to_json(articles, output_dir="../data/scraped")
            print(f"\n[SUCCESS] Saved to: {filepath}")

        else:
            print("\n[WARNING] No articles found (check date range or website structure)")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_isw())
