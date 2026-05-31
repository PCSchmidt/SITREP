# Guardian API Scraper
# Uses The Guardian's official Open Platform API
# Free tier: 5,000 requests/day

import aiohttp
import logging
import os
from datetime import datetime, timedelta
from typing import List, Dict

from .base import BaseScraper, Article

logger = logging.getLogger(__name__)


class GuardianAPIScraper(BaseScraper):
    """
    Scraper for The Guardian using their official API.

    API Docs: https://open-platform.theguardian.com/documentation/
    Register for free key: https://open-platform.theguardian.com/access/

    Free tier limits:
    - 5,000 calls per day
    - 12 calls per second
    """

    BASE_URL = "https://content.guardianapis.com/search"

    # Region-specific search queries
    REGION_QUERIES = {
        'Middle East': 'iran OR iraq OR syria OR israel OR palestine OR lebanon OR yemen OR saudi',
        'Europe/Africa': 'ukraine OR russia OR nato OR putin OR europe OR africa OR wagner',
        'Indo-Pacific': 'china OR taiwan OR japan OR korea OR india OR south china sea',
        'Western Hemisphere': 'mexico OR venezuela OR colombia OR brazil OR canada OR arctic OR cartel'
    }

    def __init__(self, api_key: str = None):
        """
        Initialize Guardian API scraper.

        Args:
            api_key: Guardian API key (or set GUARDIAN_API_KEY env var)
        """
        super().__init__("The Guardian")
        self.api_key = api_key or os.getenv('GUARDIAN_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Guardian API key required. "
                "Set GUARDIAN_API_KEY environment variable or pass api_key parameter. "
                "Get free key at: https://open-platform.theguardian.com/access/"
            )

    async def scrape_recent_articles(self, days: int = 7) -> List[Article]:
        """Orchestrator entry point: query the Guardian API and return Article objects."""
        raw = await self.scrape_all_regions(articles_per_region=15)
        return [Article.from_dict(d) for d in raw]

    async def scrape_all_regions(self, articles_per_region: int = 15) -> List[Dict]:
        """
        Scrape articles for all regions.

        Args:
            articles_per_region: Number of articles per region

        Returns:
            List of article dictionaries
        """
        all_articles = []

        async with aiohttp.ClientSession() as session:
            for region, query in self.REGION_QUERIES.items():
                try:
                    logger.info(f"Scraping Guardian for region: {region}")
                    articles = await self.scrape_region(session, region, query, articles_per_region)
                    all_articles.extend(articles)
                    logger.info(f"  → Got {len(articles)} Guardian articles for {region}")
                except Exception as e:
                    logger.error(f"Failed to scrape Guardian for {region}: {e}")
                    continue

        logger.info(f"Total Guardian articles: {len(all_articles)}")
        return all_articles

    async def scrape_region(
        self,
        session: aiohttp.ClientSession,
        region: str,
        query: str,
        max_articles: int = 15
    ) -> List[Dict]:
        """
        Scrape articles for a specific region.

        Args:
            session: aiohttp session
            region: Region name
            query: Search query
            max_articles: Maximum articles to fetch

        Returns:
            List of article dictionaries
        """
        # Calculate date range (last 7 days)
        to_date = datetime.now()
        from_date = to_date - timedelta(days=7)

        params = {
            'api-key': self.api_key,
            'q': query,
            'section': 'world|politics|business',  # Relevant sections
            'show-fields': 'bodyText,byline,headline',  # Request full article text
            'from-date': from_date.strftime('%Y-%m-%d'),
            'to-date': to_date.strftime('%Y-%m-%d'),
            'page-size': min(max_articles, 50),  # API max is 50
            'order-by': 'relevance'  # Most relevant articles
        }

        try:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status != 200:
                    logger.error(f"Guardian API error: HTTP {response.status}")
                    return []

                data = await response.json()

                if data['response']['status'] != 'ok':
                    logger.error(f"Guardian API returned error status")
                    return []

                results = data['response']['results']
                articles = []

                for item in results:
                    # Extract article data
                    article = {
                        'source': 'The Guardian',
                        'title': item.get('webTitle', 'Untitled'),
                        'url': item.get('webUrl', ''),
                        'published_date': self._parse_date(item.get('webPublicationDate')),
                        'content': self._extract_content(item),
                        'region_tags': [region]  # Already tagged by our query
                    }

                    articles.append(article)

                return articles

        except Exception as e:
            logger.error(f"Error fetching Guardian articles for {region}: {e}")
            return []

    def _extract_content(self, item: Dict) -> str:
        """Extract article content from API response"""
        fields = item.get('fields', {})

        # Get full body text if available
        content = fields.get('bodyText', '')

        # Fallback to headline if no body
        if not content:
            content = fields.get('headline', item.get('webTitle', ''))

        return content[:3000]  # Limit to 3000 chars

    def _parse_date(self, date_str: str) -> str:
        """Parse Guardian API date format to YYYY-MM-DD"""
        if not date_str:
            return datetime.now().strftime('%Y-%m-%d')

        try:
            # Guardian format: 2026-05-31T12:00:00Z
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d')
        except:
            return datetime.now().strftime('%Y-%m-%d')


# Test function
async def test_guardian_scraper():
    """Test Guardian API scraper"""
    import os

    api_key = os.getenv('GUARDIAN_API_KEY')
    if not api_key:
        print("ERROR: Set GUARDIAN_API_KEY environment variable first")
        print("Get free key at: https://open-platform.theguardian.com/access/")
        return

    scraper = GuardianAPIScraper(api_key)
    articles = await scraper.scrape_all_regions(articles_per_region=5)

    print(f"\n=== GUARDIAN API SCRAPER TEST ===")
    print(f"Total articles: {len(articles)}")
    print(f"\nSample articles:")
    for i, article in enumerate(articles[:3], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Region: {', '.join(article['region_tags'])}")
        print(f"   URL: {article['url']}")
        print(f"   Content preview: {article['content'][:200]}...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_guardian_scraper())
