# Scraper orchestrator - runs all scrapers and aggregates results
import asyncio
import logging
from typing import List, Dict
from datetime import datetime

from .isw_scraper import ISWScraper
from .defenseone_scraper import DefenseOneScraper
from .breakingdefense_scraper import BreakingDefenseScraper
from .iiss_scraper import IISSScraper
from .base import Article

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScraperOrchestrator:
    """Orchestrates all scrapers and handles errors/retries"""

    def __init__(self):
        self.scrapers = [
            ISWScraper(),
            DefenseOneScraper(),
            BreakingDefenseScraper(),
            IISSScraper()
        ]

    async def scrape_all_sources(self, days: int = 7, max_retries: int = 2) -> Dict[str, List[Article]]:
        """
        Run all scrapers in parallel with error handling.

        Args:
            days: Number of days to look back
            max_retries: Number of retry attempts per source

        Returns:
            Dictionary mapping source name to list of articles
        """
        results = {}

        # Run scrapers in parallel
        tasks = []
        for scraper in self.scrapers:
            task = self._scrape_with_retry(scraper, days, max_retries)
            tasks.append(task)

        # Gather results (continues even if some fail)
        scraper_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for scraper, result in zip(self.scrapers, scraper_results):
            if isinstance(result, Exception):
                logger.error(f"{scraper.source_name} failed after retries: {result}")
                results[scraper.source_name] = []
            else:
                results[scraper.source_name] = result
                logger.info(f"{scraper.source_name}: {len(result)} articles")

        return results

    async def _scrape_with_retry(self, scraper, days: int, max_retries: int) -> List[Article]:
        """Scrape with retry logic"""
        for attempt in range(max_retries + 1):
            try:
                articles = await scraper.scrape_recent_articles(days)
                return articles
            except Exception as e:
                if attempt < max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"{scraper.source_name} attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"{scraper.source_name} failed after {max_retries + 1} attempts")
                    raise

    def save_all_results(self, results: Dict[str, List[Article]], output_dir: str = "data/scraped"):
        """Save all scraper results to JSON files"""
        for source_name, articles in results.items():
            if articles:
                scraper = next((s for s in self.scrapers if s.source_name == source_name), None)
                if scraper:
                    scraper.save_to_json(articles, output_dir)

    def get_summary(self, results: Dict[str, List[Article]]) -> Dict:
        """Generate summary statistics"""
        total_articles = sum(len(articles) for articles in results.values())
        by_region = {}

        for articles in results.values():
            for article in articles:
                for region in article.region_tags:
                    by_region[region] = by_region.get(region, 0) + 1

        return {
            "total_articles": total_articles,
            "by_source": {name: len(articles) for name, articles in results.items()},
            "by_region": by_region,
            "scraped_at": datetime.utcnow().isoformat()
        }


async def main():
    """Main entry point for testing"""
    orchestrator = ScraperOrchestrator()

    logger.info("Starting scraping pipeline...")
    logger.info(f"Scraping from {len(orchestrator.scrapers)} sources")

    # Scrape all sources
    results = await orchestrator.scrape_all_sources(days=7)

    # Save results
    orchestrator.save_all_results(results)

    # Print summary
    summary = orchestrator.get_summary(results)
    logger.info("\n=== SCRAPING SUMMARY ===")
    logger.info(f"Total articles: {summary['total_articles']}")
    logger.info(f"By source: {summary['by_source']}")
    logger.info(f"By region: {summary['by_region']}")
    logger.info("========================\n")

    return results


if __name__ == "__main__":
    asyncio.run(main())
