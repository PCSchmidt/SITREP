# Government Press Release Scraper
# Scrapes official press releases from US and allied government sources
# These are authoritative, free, and publicly available

import aiohttp
import logging
from datetime import datetime
from typing import List, Dict
import re
from bs4 import BeautifulSoup

from .base import BaseScraper, Article

logger = logging.getLogger(__name__)


class GovernmentScraper(BaseScraper):
    """
    Scraper for official government press releases and statements.

    Sources:
    - US State Department
    - US Department of Defense / Pentagon
    - UK Ministry of Defence
    - NATO
    - UN Security Council
    """

    SOURCES = {
        'US State Dept': {
            'rss': 'https://www.state.gov/rss-feed/press-releases/feed/',
            'region_default': ['Global']
        },
        'US Defense Dept': {
            'rss': 'https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=945',
            'region_default': ['Global']
        },
        'UK Ministry of Defence': {
            'rss': 'https://www.gov.uk/government/organisations/ministry-of-defence.atom',
            'region_default': ['Europe/Africa']
        }
    }

    # Region tagging keywords (same as RSS scraper)
    REGION_KEYWORDS = {
        'Middle East': [
            'iran', 'iraq', 'syria', 'israel', 'palestine', 'gaza', 'lebanon', 'hezbollah',
            'saudi', 'yemen', 'gulf', 'egypt', 'jordan', 'hormuz', 'irgc', 'houthi',
            'centcom', 'persian gulf'
        ],
        'Europe/Africa': [
            'ukraine', 'russia', 'nato', 'europe', 'moscow', 'kyiv', 'putin', 'kremlin',
            'baltic', 'poland', 'germany', 'france', 'uk', 'britain', 'eucom',
            'sahel', 'ethiopia', 'sudan', 'nigeria', 'somalia', 'mali', 'africom'
        ],
        'Indo-Pacific': [
            'china', 'taiwan', 'beijing', 'south china sea', 'japan', 'korea', 'north korea',
            'india', 'pakistan', 'philippines', 'vietnam', 'indonesia', 'australia',
            'indo-pacific', 'indopacom'
        ],
        'Western Hemisphere': [
            'mexico', 'cartel', 'latin america', 'venezuela', 'colombia', 'brazil',
            'southcom', 'northcom', 'canada', 'arctic', 'greenland', 'caribbean'
        ]
    }

    def __init__(self):
        super().__init__("Government")

    async def scrape_recent_articles(self, days: int = 7) -> List[Article]:
        """Orchestrator entry point: scrape gov sources and return Article objects."""
        raw = await self.scrape_all(max_per_source=10)
        return [Article.from_dict(d) for d in raw]

    async def scrape_all(self, max_per_source: int = 10) -> List[Dict]:
        """
        Scrape all government sources.

        Args:
            max_per_source: Maximum articles per source

        Returns:
            List of article dictionaries
        """
        all_articles = []

        async with aiohttp.ClientSession() as session:
            for source_name, config in self.SOURCES.items():
                try:
                    logger.info(f"Scraping government source: {source_name}")
                    articles = await self.scrape_rss(
                        session,
                        source_name,
                        config['rss'],
                        config['region_default'],
                        max_per_source
                    )
                    all_articles.extend(articles)
                    logger.info(f"  → Got {len(articles)} from {source_name}")
                except Exception as e:
                    logger.error(f"Failed to scrape {source_name}: {e}")
                    continue

        logger.info(f"Total government articles: {len(all_articles)}")
        return all_articles

    async def scrape_rss(
        self,
        session: aiohttp.ClientSession,
        source_name: str,
        rss_url: str,
        region_default: List[str],
        max_articles: int
    ) -> List[Dict]:
        """Scrape government RSS feed"""
        import feedparser

        try:
            async with session.get(rss_url) as response:
                if response.status != 200:
                    logger.error(f"{source_name}: HTTP {response.status}")
                    return []

                feed_content = await response.text()
                feed = feedparser.parse(feed_content)

                articles = []

                for entry in feed.entries[:max_articles]:
                    # Extract content
                    content = self._extract_content(entry)

                    article = {
                        'source': source_name,
                        'title': entry.get('title', 'Untitled'),
                        'url': entry.get('link', ''),
                        'published_date': self._parse_date(entry),
                        'content': content,
                        'region_tags': self._tag_regions(
                            entry.get('title', '') + ' ' + content,
                            region_default
                        )
                    }

                    articles.append(article)

                return articles

        except Exception as e:
            logger.error(f"Error scraping {source_name}: {e}")
            return []

    def _extract_content(self, entry) -> str:
        """Extract content from RSS entry"""
        if hasattr(entry, 'content'):
            content = entry.content[0].value
        elif hasattr(entry, 'summary'):
            content = entry.summary
        elif hasattr(entry, 'description'):
            content = entry.description
        else:
            content = ""

        # Clean HTML
        content = re.sub(r'<[^>]+>', '', content)
        content = re.sub(r'\s+', ' ', content)

        return content.strip()[:3000]

    def _parse_date(self, entry) -> str:
        """Parse date from RSS entry"""
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            dt = datetime(*entry.published_parsed[:6])
            return dt.strftime('%Y-%m-%d')
        return datetime.now().strftime('%Y-%m-%d')

    def _tag_regions(self, text: str, default: List[str]) -> List[str]:
        """Tag article with regions based on keywords"""
        text_lower = text.lower()
        regions = []

        for region, keywords in self.REGION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    regions.append(region)
                    break

        # Return found regions or default
        return regions if regions else default


# Test function
async def test_gov_scraper():
    """Test government scraper"""
    scraper = GovernmentScraper()
    articles = await scraper.scrape_all(max_per_source=5)

    print(f"\n=== GOVERNMENT SCRAPER TEST ===")
    print(f"Total articles: {len(articles)}")
    print(f"\nSample articles:")
    for i, article in enumerate(articles[:3], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Regions: {', '.join(article['region_tags'])}")
        print(f"   Content preview: {article['content'][:150]}...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_gov_scraper())
