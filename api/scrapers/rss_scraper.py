# RSS Feed Scraper
# Scrapes articles from RSS feeds (faster and more reliable than browser scraping)

import feedparser
import logging
from datetime import datetime
from typing import List, Dict
import re

logger = logging.getLogger(__name__)


class RSSFeedScraper:
    """
    Generic RSS feed scraper for news sources.

    RSS feeds are:
    - Faster than Playwright (no browser needed)
    - More reliable (less prone to breaking)
    - Publisher-approved method
    - Often include full article text
    """

    # RSS Feed URLs for major news sources
    FEEDS = {
        # Defense & Military (specialized)
        'Defense One': 'https://www.defenseone.com/rss/',
        'Breaking Defense': 'https://breakingdefense.com/feed/',
        'The Aviationist': 'https://theaviationist.com/feed/',
        'Military Times': 'https://www.militarytimes.com/arc/outboundfeeds/rss/',
        'Task & Purpose': 'https://taskandpurpose.com/feed/',

        # Mainstream International News
        'Reuters World': 'https://www.reuters.com/rssFeed/worldNews',
        'Reuters Business': 'https://www.reuters.com/rssFeed/businessNews',
        'BBC World': 'http://feeds.bbci.co.uk/news/world/rss.xml',
        'BBC Business': 'http://feeds.bbci.co.uk/news/business/rss.xml',
        'The Guardian World': 'https://www.theguardian.com/world/rss',
        'Al Jazeera': 'https://www.aljazeera.com/xml/rss/all.xml',

        # Economic & Business News
        'Financial Times World': 'https://www.ft.com/world?format=rss',
        'Bloomberg Politics': 'https://www.bloomberg.com/politics/feeds/sitemap_news.xml',
        'The Economist': 'https://www.economist.com/international/rss.xml',
        'Reuters Markets': 'https://www.reuters.com/rssFeed/marketsNews',

        # Think Tanks & Analysis
        'CSIS': 'https://www.csis.org/analysis/feed',
        'CFR Analysis': 'https://www.cfr.org/rss/feed',
        'World Bank News': 'https://www.worldbank.org/en/news/rss',
        'Brookings': 'https://www.brookings.edu/feed/',

        # Regional specialists
        'The Diplomat': 'https://thediplomat.com/feed/',
        'Middle East Eye': 'https://www.middleeasteye.net/rss',
        'Carnegie Endowment': 'https://carnegieendowment.org/feeds/all',
    }

    # Region tagging keywords (including economic terms)
    REGION_KEYWORDS = {
        'Middle East': [
            'iran', 'iraq', 'syria', 'israel', 'palestine', 'gaza', 'lebanon', 'hezbollah',
            'saudi', 'yemen', 'gulf', 'egypt', 'jordan', 'hormuz', 'irgc', 'houthi',
            'bahrain', 'kuwait', 'qatar', 'uae', 'oman',
            'opec', 'oil price', 'strait of hormuz', 'persian gulf', 'gcc'
        ],
        'Europe/Africa': [
            'ukraine', 'russia', 'nato', 'europe', 'moscow', 'kyiv', 'putin', 'kremlin',
            'baltic', 'poland', 'germany', 'france', 'uk', 'britain', 'european union',
            'sahel', 'ethiopia', 'sudan', 'nigeria', 'somalia', 'mali', 'wagner',
            'africa', 'african union', 'libya', 'tunisia', 'algeria', 'morocco',
            'sanctions russia', 'nord stream', 'european economy', 'refugees', 'grain deal'
        ],
        'Indo-Pacific': [
            'china', 'taiwan', 'beijing', 'south china sea', 'japan', 'korea', 'north korea',
            'india', 'pakistan', 'philippines', 'vietnam', 'indonesia', 'australia',
            'singapore', 'thailand', 'myanmar', 'quad', 'aukus', 'asean', 'indo-pacific',
            'belt and road', 'rare earth', 'semiconductor', 'supply chain', 'trade war'
        ],
        'Western Hemisphere': [
            'mexico', 'cartel', 'latin america', 'venezuela', 'colombia', 'brazil',
            'argentina', 'chile', 'peru', 'cuba', 'canada', 'arctic', 'greenland',
            'caribbean', 'central america', 'south america',
            'lithium', 'migration', 'trade bloc', 'nearshoring', 'remittances'
        ]
    }

    def __init__(self):
        self.feeds = self.FEEDS

    async def scrape_all(self, max_articles_per_feed: int = 20) -> List[Dict]:
        """
        Scrape all RSS feeds.

        Args:
            max_articles_per_feed: Maximum articles to take from each feed

        Returns:
            List of article dictionaries
        """
        all_articles = []

        for source_name, feed_url in self.feeds.items():
            try:
                logger.info(f"Scraping RSS feed: {source_name}")
                articles = await self.scrape_feed(source_name, feed_url, max_articles_per_feed)
                all_articles.extend(articles)
                logger.info(f"  → Got {len(articles)} articles from {source_name}")
            except Exception as e:
                logger.error(f"Failed to scrape {source_name}: {e}")
                continue

        logger.info(f"Total RSS articles scraped: {len(all_articles)}")
        return all_articles

    async def scrape_feed(self, source_name: str, feed_url: str, max_articles: int = 20) -> List[Dict]:
        """
        Scrape a single RSS feed.

        Args:
            source_name: Display name of the source
            feed_url: URL of the RSS feed
            max_articles: Maximum articles to extract

        Returns:
            List of article dictionaries
        """
        try:
            # Parse RSS feed
            feed = feedparser.parse(feed_url)

            if feed.bozo:  # RSS parsing error
                logger.warning(f"RSS parse warning for {source_name}: {feed.bozo_exception}")

            articles = []

            for entry in feed.entries[:max_articles]:
                # Extract article data
                article = {
                    'source': source_name,
                    'title': self._clean_text(entry.get('title', 'Untitled')),
                    'url': entry.get('link', ''),
                    'published_date': self._parse_date(entry),
                    'content': self._extract_content(entry),
                    'region_tags': []
                }

                # Tag regions based on content
                article['region_tags'] = self._tag_regions(
                    article['title'] + ' ' + article['content']
                )

                # Only include if we found region tags
                if article['region_tags']:
                    articles.append(article)

            return articles

        except Exception as e:
            logger.error(f"Error scraping {source_name}: {e}")
            return []

    def _extract_content(self, entry) -> str:
        """Extract article content from RSS entry"""
        # Try different content fields (RSS feeds vary)
        if hasattr(entry, 'content'):
            content = entry.content[0].value
        elif hasattr(entry, 'summary'):
            content = entry.summary
        elif hasattr(entry, 'description'):
            content = entry.description
        else:
            content = ""

        # Clean HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        content = self._clean_text(content)

        return content[:3000]  # Limit length

    def _parse_date(self, entry) -> str:
        """Parse publication date from RSS entry"""
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            dt = datetime(*entry.published_parsed[:6])
            return dt.strftime('%Y-%m-%d')
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            dt = datetime(*entry.updated_parsed[:6])
            return dt.strftime('%Y-%m-%d')
        else:
            return datetime.now().strftime('%Y-%m-%d')

    def _tag_regions(self, text: str) -> List[str]:
        """Tag article with relevant regions based on keyword matching"""
        text_lower = text.lower()
        regions = []

        for region, keywords in self.REGION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    regions.append(region)
                    break  # Found match for this region, move to next

        return regions if regions else ['Global']

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")

        return text.strip()


# Test function
async def test_rss_scraper():
    """Test RSS scraper with a few feeds"""
    scraper = RSSFeedScraper()

    # Test just a couple feeds
    test_feeds = {
        'Defense One': scraper.feeds['Defense One'],
        'Reuters World': scraper.feeds['Reuters World']
    }
    scraper.feeds = test_feeds

    articles = await scraper.scrape_all(max_articles_per_feed=10)

    print(f"\n=== RSS SCRAPER TEST ===")
    print(f"Total articles: {len(articles)}")
    print(f"\nSample articles:")
    for i, article in enumerate(articles[:3], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Regions: {', '.join(article['region_tags'])}")
        print(f"   Content preview: {article['content'][:200]}...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_rss_scraper())
