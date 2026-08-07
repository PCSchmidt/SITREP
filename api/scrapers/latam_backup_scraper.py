# Backup Latin America/Western Hemisphere RSS sources
from .base import BaseScraper, Article
from datetime import datetime, timedelta, timezone
from typing import List
import feedparser
import httpx
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; SITREP intelligence aggregator)'
}


class LatAmBackupScraper(BaseScraper):
    """
    Backup scraper for Western Hemisphere intelligence.
    Uses multiple LatAm-focused RSS feeds as fallback when Americas Quarterly fails.

    NOTE: This scraper is disabled because reliable free LatAm RSS feeds are hard to find.
    Instead, we rely on keyword-based tagging from general news RSS feeds (BBC, Reuters,
    Guardian, Al Jazeera) which already cover Western Hemisphere news.
    """

    # Disabled - no reliable free LatAm RSS feeds found
    # Reuters LatAm returns 401, Wilson Center/InSight Crime have connectivity issues
    FEEDS = []

    def __init__(self):
        super().__init__("LatAm Backup Sources (DISABLED)")

    async def scrape_recent_articles(self, days: int = 7) -> List[Article]:
        """Disabled - returns empty list"""
        logger.info("LatAm Backup scraper is disabled (no reliable free RSS feeds)")
        return []

        # Original implementation (disabled):
        all_articles = []
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            for feed_config in self.FEEDS:
                try:
                    logger.info(f"Fetching {feed_config['name']}")
                    resp = await client.get(feed_config['url'], headers=HEADERS)
                    resp.raise_for_status()

                    feed = feedparser.parse(resp.text)
                    articles = self._parse_feed(feed, feed_config['name'], cutoff)
                    all_articles.extend(articles)
                    logger.info(f"  → Got {len(articles)} articles from {feed_config['name']}")

                except Exception as e:
                    logger.warning(f"Failed to fetch {feed_config['name']}: {e}")
                    continue

        logger.info(f"LatAm Backup total: {len(all_articles)} articles")
        return all_articles

    def _parse_feed(self, feed, source_name: str, cutoff: datetime) -> List[Article]:
        """Parse RSS feed entries into Article objects"""
        articles = []

        for entry in feed.entries[:20]:  # Limit per feed
            try:
                # Parse publish date
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

                if not pub_date or pub_date < cutoff:
                    continue

                # Get content
                content = ""
                if hasattr(entry, 'summary'):
                    content = entry.summary
                elif hasattr(entry, 'description'):
                    content = entry.description

                title = entry.get('title', '').strip()
                url = entry.get('link', '').strip()

                if not title or not url or len(title) < 10:
                    continue

                # All articles from these feeds are Western Hemisphere
                article = Article(
                    source=source_name,
                    url=url,
                    title=title,
                    published_date=pub_date.replace(tzinfo=None),
                    content=content or title,
                    region_tags=['Western Hemisphere']
                )
                articles.append(article)

            except Exception as e:
                logger.debug(f"Failed to parse entry from {source_name}: {e}")
                continue

        return articles
