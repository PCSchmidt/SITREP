# Base RSS scraper - fetches feed metadata, pulls full content via httpx
import xml.etree.ElementTree as ET
import re
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import List, Optional
import logging

import httpx
from bs4 import BeautifulSoup

from .base import BaseScraper, Article

logger = logging.getLogger(__name__)

CONTENT_SELECTORS = [
    '.entry-content',
    '.article-body',
    '.article-content',
    '.story-body',
    '.story-content',
    '.post-content',
    '.post__content',
    '.td-post-content',
    'article',
    'main',
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
}


class RSSBaseScraper(BaseScraper):
    """
    RSS/Atom feed-based scraper. Subclasses set FEED_URL.
    Fetches article list from feed, then pulls full content via httpx.
    """

    FEED_URL: str = ""
    # Articles whose titles don't match any of these keywords are dropped.
    # Empty list = accept all articles (appropriate for defense-only sources).
    TOPIC_FILTER: List[str] = []
    # Max articles to return per run
    MAX_ARTICLES: int = 20

    def __init__(self, source_name: str):
        super().__init__(source_name)

    async def scrape_recent_articles(self, days: int = 7) -> List[Article]:
        feed_items = await self._fetch_feed()
        if not feed_items:
            self.logger.warning(f"No items from {self.FEED_URL}")
            return []

        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        articles = []

        async with httpx.AsyncClient(headers=HEADERS, timeout=20, follow_redirects=True) as client:
            for item in feed_items:
                if len(articles) >= self.MAX_ARTICLES:
                    break

                title = item.get('title', '').strip()
                url = item.get('url', '').strip()
                pub_date = item.get('pub_date')

                if not title or not url:
                    continue

                if pub_date and pub_date < cutoff:
                    continue

                if self.TOPIC_FILTER and not self._matches_topic(title):
                    continue

                content = item.get('content', '')
                if len(content) < 300:
                    content = await self._fetch_content(client, url)

                if not content:
                    self.logger.debug(f"No content for {url}")
                    continue

                region_tags = self._infer_regions(title + ' ' + content)

                article = Article(
                    source=self.source_name,
                    url=url,
                    title=title,
                    published_date=(pub_date or datetime.now(timezone.utc)).replace(tzinfo=None),
                    content=content,
                    author=item.get('author', self.source_name),
                    region_tags=region_tags,
                )
                articles.append(article)
                self.logger.info(f"Scraped: {title[:60]}")

        self.logger.info(f"Scraped {len(articles)} articles from {self.source_name}")
        return articles

    async def _fetch_feed(self) -> List[dict]:
        """Fetch and parse RSS/Atom feed, return list of item dicts."""
        try:
            # Use httpx instead of urllib for better reliability
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(self.FEED_URL, headers=HEADERS, follow_redirects=True)
                resp.raise_for_status()
                raw = resp.content

            # Strip leading/trailing whitespace to handle malformed feeds
            if isinstance(raw, bytes):
                raw = raw.strip()

            root = ET.fromstring(raw)
        except Exception as e:
            self.logger.error(f"Failed to fetch feed {self.FEED_URL}: {e}")
            return []

        items = []
        # RSS 2.0
        for item in root.findall('.//item'):
            items.append(self._parse_rss_item(item))
        # Atom
        if not items:
            atom_ns = 'http://www.w3.org/2005/Atom'
            for entry in root.findall(f'.//{{{atom_ns}}}entry'):
                items.append(self._parse_atom_entry(entry))

        return items

    def _parse_rss_item(self, item: ET.Element) -> dict:
        title = item.findtext('title') or ''
        link = item.findtext('link') or ''
        pub_date_str = item.findtext('pubDate') or ''
        author = item.findtext('author') or item.findtext('{http://purl.org/dc/elements/1.1/}creator') or ''
        # Full content in content:encoded, fall back to description
        content = (
            item.findtext('{http://purl.org/rss/1.0/modules/content/}encoded') or
            item.findtext('description') or ''
        )
        # Strip HTML tags from content
        content = BeautifulSoup(content, 'lxml').get_text(separator=' ', strip=True) if content else ''

        pub_date = None
        if pub_date_str:
            try:
                pub_date = parsedate_to_datetime(pub_date_str)
            except Exception:
                pass

        return {'title': title, 'url': link, 'pub_date': pub_date, 'author': author, 'content': content}

    def _parse_atom_entry(self, entry: ET.Element) -> dict:
        ns = 'http://www.w3.org/2005/Atom'
        title = entry.findtext(f'{{{ns}}}title') or ''
        link_elem = entry.find(f'{{{ns}}}link[@rel="alternate"]') or entry.find(f'{{{ns}}}link')
        link = link_elem.get('href', '') if link_elem is not None else ''
        updated = entry.findtext(f'{{{ns}}}updated') or ''
        author_elem = entry.find(f'{{{ns}}}author/{{{ns}}}name')
        author = author_elem.text if author_elem is not None else ''
        content_elem = entry.find(f'{{{ns}}}content') or entry.find(f'{{{ns}}}summary')
        content = content_elem.text or '' if content_elem is not None else ''
        content = BeautifulSoup(content, 'lxml').get_text(separator=' ', strip=True) if content else ''

        pub_date = None
        if updated:
            try:
                pub_date = datetime.fromisoformat(updated.replace('Z', '+00:00'))
            except Exception:
                pass

        return {'title': title, 'url': link, 'pub_date': pub_date, 'author': author, 'content': content}

    async def _fetch_content(self, client: httpx.AsyncClient, url: str) -> str:
        """Fetch full article content from URL using httpx + BeautifulSoup."""
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'lxml')
            # Remove noise
            for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
                tag.decompose()
            for sel in CONTENT_SELECTORS:
                elem = soup.select_one(sel)
                if elem:
                    text = elem.get_text(separator='\n', strip=True)
                    if len(text) > 200:
                        return text[:8000]
            return ''
        except Exception as e:
            self.logger.debug(f"Content fetch failed for {url}: {e}")
            return ''

    def _matches_topic(self, title: str) -> bool:
        title_lower = title.lower()
        return any(kw in title_lower for kw in self.TOPIC_FILTER)

    def _infer_regions(self, text: str) -> List[str]:
        regions = []
        t = text.lower()
        if any(kw in t for kw in ['iran', 'iraq', 'syria', 'israel', 'gaza', 'lebanon', 'yemen', 'saudi', 'uae', 'middle east', 'persian gulf', 'strait of hormuz']):
            regions.append('Middle East')
        if any(kw in t for kw in ['china', 'taiwan', 'south china sea', 'japan', 'korea', 'indo-pacific', 'pacific', 'philippines', 'australia', 'vietnam']):
            regions.append('Indo-Pacific')
        if any(kw in t for kw in ['ukraine', 'russia', 'nato', 'europe', 'africa', 'balkans', 'poland', 'belarus', 'finland', 'sweden', 'estonia', 'latvia', 'lithuania']):
            regions.append('Europe/Africa')
        # Western Hemisphere: broader keywords including US military activities, regional orgs, country names
        if any(kw in t for kw in [
            'latin america', 'venezuela', 'cuba', 'mexico', 'brazil', 'colombia', 'americas', 'caribbean', 'canada',
            'argentina', 'chile', 'peru', 'ecuador', 'bolivia', 'panama', 'guatemala', 'honduras', 'nicaragua',
            'southcom', 'northcom', 'western hemisphere', 'oas', 'organization of american states',
            'cartel', 'narco', 'drug trafficking', 'migration crisis', 'border', 'us-mexico'
        ]):
            regions.append('Western Hemisphere')
        return regions if regions else ['Global']
