# Scraper orchestrator - runs all scrapers and aggregates results
import asyncio
import logging
from typing import List, Dict
from datetime import datetime

from .isw_scraper import ISWScraper
from .defenseone_scraper import DefenseOneScraper
from .breakingdefense_scraper import BreakingDefenseScraper
from .warontherocks_scraper import WarOnTheRocksScraper
from .thewarzone_scraper import TheWarZoneScraper
from .aljazeera_scraper import AlJazeeraScraper
from .gdelt_scraper import GDELTScraper
from .foreignpolicy_scraper import ForeignPolicyScraper
from .cfr_scraper import CFRScraper
from .americasquarterly_scraper import AmericasQuarterlyScraper
from .rss_scraper import RSSFeedScraper
from .guardian_api_scraper import GuardianAPIScraper
from .gov_scraper import GovernmentScraper
from .base import Article
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScraperOrchestrator:
    """Orchestrates all scrapers and handles errors/retries."""

    # Per-attempt timeout (seconds). Prevents one slow/hung source (e.g. ISW
    # Playwright networkidle, GDELT API) from stalling the entire pipeline in
    # asyncio.gather, which has no timeout of its own.
    SCRAPER_TIMEOUT = 60

    def __init__(self):
        self.scrapers = [
            ISWScraper(),           # Playwright - deep analysis, Ukraine/Iran
            DefenseOneScraper(),    # RSS - Pentagon policy, military tech
            BreakingDefenseScraper(),  # RSS - defense procurement, emerging tech
            WarOnTheRocksScraper(), # RSS - strategic analysis
            TheWarZoneScraper(),    # RSS - military aviation, weapons systems
            AlJazeeraScraper(),     # RSS - non-Western perspective, Middle East/Africa
            GDELTScraper(),         # GDELT DOC 2.0 - LatAm, Africa, SE Asia local sources
            ForeignPolicyScraper(), # RSS - US foreign policy, global affairs
            CFRScraper(),           # RSS - US foreign relations
            AmericasQuarterlyScraper(), # RSS - Latin America dedicated coverage
            RSSFeedScraper(),       # RSS - 20+ feeds (Defense, Reuters, BBC, Guardian, Bloomberg, FT, Economist, etc.)
            GovernmentScraper(),    # RSS - US/UK government press releases
        ]

        # Add Guardian API if key available
        if os.getenv('GUARDIAN_API_KEY'):
            self.scrapers.append(GuardianAPIScraper())
            logger.info("Guardian API scraper enabled")
        else:
            logger.warning("GUARDIAN_API_KEY not set - Guardian API scraper disabled")

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

        tasks = [self._scrape_with_retry(scraper, days, max_retries) for scraper in self.scrapers]
        scraper_results = await asyncio.gather(*tasks, return_exceptions=True)

        for scraper, result in zip(self.scrapers, scraper_results):
            if isinstance(result, Exception):
                logger.error(f"{scraper.source_name} failed after retries: {result}")
                results[scraper.source_name] = []
            else:
                results[scraper.source_name] = result
                logger.info(f"{scraper.source_name}: {len(result)} articles")

        return results

    async def _scrape_with_retry(self, scraper, days: int, max_retries: int) -> List[Article]:
        for attempt in range(max_retries + 1):
            try:
                return await asyncio.wait_for(
                    scraper.scrape_recent_articles(days),
                    timeout=self.SCRAPER_TIMEOUT
                )
            except asyncio.TimeoutError:
                e = f"timed out after {self.SCRAPER_TIMEOUT}s"
                if attempt < max_retries:
                    wait = 2 ** attempt
                    logger.warning(f"{scraper.source_name} attempt {attempt + 1} {e}. Retrying in {wait}s...")
                    await asyncio.sleep(wait)
                else:
                    logger.error(f"{scraper.source_name} failed after {max_retries + 1} attempts: {e}")
                    raise
            except Exception as e:
                if attempt < max_retries:
                    wait = 2 ** attempt
                    logger.warning(f"{scraper.source_name} attempt {attempt + 1} failed: {e}. Retrying in {wait}s...")
                    await asyncio.sleep(wait)
                else:
                    logger.error(f"{scraper.source_name} failed after {max_retries + 1} attempts")
                    raise

    def save_all_results(self, results: Dict[str, List[Article]], output_dir: str = "data/scraped"):
        for source_name, articles in results.items():
            if articles:
                scraper = next((s for s in self.scrapers if s.source_name == source_name), None)
                if scraper:
                    scraper.save_to_json(articles, output_dir)

    def get_summary(self, results: Dict[str, List[Article]]) -> Dict:
        total_articles = sum(len(articles) for articles in results.values())
        by_region: Dict[str, int] = {}

        for articles in results.values():
            for article in articles:
                for region in article.region_tags:
                    by_region[region] = by_region.get(region, 0) + 1

        return {
            "total_articles": total_articles,
            "by_source": {name: len(articles) for name, articles in results.items()},
            "by_region": by_region,
            "timestamp": datetime.utcnow().isoformat()
        }


async def main():
    orchestrator = ScraperOrchestrator()
    logger.info(f"Starting pipeline with {len(orchestrator.scrapers)} sources...")

    results = await orchestrator.scrape_all_sources(days=7)
    orchestrator.save_all_results(results)

    summary = orchestrator.get_summary(results)
    logger.info("=== SCRAPING SUMMARY ===")
    logger.info(f"Total: {summary['total_articles']} articles")
    for source, count in summary['by_source'].items():
        logger.info(f"  {source}: {count}")
    logger.info(f"By region: {summary['by_region']}")

    return results


if __name__ == "__main__":
    asyncio.run(main())
