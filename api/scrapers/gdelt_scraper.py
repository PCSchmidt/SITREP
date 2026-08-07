# GDELT DOC 2.0 scraper - discovers articles from local-language sources worldwide
import asyncio
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Dict

import httpx
from bs4 import BeautifulSoup

from .base import BaseScraper, Article

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; SITREP intelligence aggregator)'
}

# Same fallback chain as RSSBaseScraper
CONTENT_SELECTORS = [
    '.entry-content', '.article-body', '.article-content', '.story-body',
    '.story-content', '.post-content', '.post__content', '.article__body',
    'article', 'main',
]


class GDELTScraper(BaseScraper):
    """
    Discovers geopolitical articles via the free GDELT DOC 2.0 API.

    Fills the coverage gap for regions under-served by RSS scrapers:
      - Western Hemisphere (Latin America)
      - Sub-Saharan Africa
      - Southeast Asia / Oceania

    GDELT monitors hundreds of thousands of sources worldwide including
    local-language outlets machine-translated to English. No API key required.

    Rate-limiting: 3 queries per run with 30-second delays between each.
    On a weekly cron job this adds ~2 minutes to pipeline time.

    Query syntax confirmed working: parenthesized OR for country filters
      e.g. "military security (sourcecountry:BR OR sourcecountry:CO)"
    """

    GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
    DELAY_BETWEEN_QUERIES = 30   # seconds — increased from 10s to avoid 429s
    MAX_RECORDS_PER_QUERY = 15   # reduced from 20 to lower API load
    MAX_ARTICLES_TOTAL = 15      # bounded so best-effort content fetch fits scrape_timeout
    # GDELT's rate-limited multi-query run + per-article content fetches need
    # more than the orchestrator's default per-scraper timeout. Honored by
    # ScraperOrchestrator._scrape_with_retry via getattr(scraper, 'scrape_timeout').
    scrape_timeout = 300  # increased from 150s to 5min for slower retries

    # Three targeted region queries covering our worst coverage gaps.
    #
    # IMPORTANT: GDELT's sourcecountry: filter uses FIPS 10-4 country codes,
    # NOT ISO 3166-1. They diverge for many countries (e.g. Chile FIPS=CI not
    # CL, South Africa=SF not ZA, Philippines=RP not PH, Vietnam=VM, Nigeria=NI,
    # Australia=AS). An unsupported code makes GDELT reject the whole query
    # ("Invalid/Unsupported Country") and return zero articles.
    #
    # Keywords are wrapped in (a OR b OR ...): GDELT ANDs space-separated terms,
    # so a flat keyword list would require every word to appear at once (~0 hits).
    QUERIES = [
        {
            "keywords": "(military OR conflict OR sanctions OR economy OR trade OR protest OR cartel OR migration)",
            "countries": ["BR", "CO", "MX", "AR", "VE", "CU", "PE", "CI"],  # CI = Chile (FIPS)
            "region_tag": "Western Hemisphere",
            "label": "Latin America",
        },
        {
            "keywords": "(military OR conflict OR coup OR insurgency OR humanitarian OR drought OR economy OR sanctions)",
            "countries": ["SF", "KE", "NI", "ET", "GH", "TZ", "IV", "SG", "RW", "UG"],  # SF=S.Africa NI=Nigeria IV=Côte d'Ivoire SG=Senegal
            "region_tag": "Europe/Africa",
            "label": "Sub-Saharan Africa",
        },
        {
            "keywords": "(military OR maritime OR sovereignty OR territorial OR semiconductor OR trade OR economy OR infrastructure)",
            "countries": ["ID", "RP", "VM", "TH", "MY", "BM", "AS", "NZ", "FJ", "PP"],  # RP=Philippines VM=Vietnam BM=Burma AS=Australia PP=PNG
            "region_tag": "Indo-Pacific",
            "label": "Southeast Asia / Oceania",
        },
    ]

    def __init__(self):
        super().__init__("GDELT")

    async def scrape_recent_articles(self, days: int = 7) -> List[Article]:
        articles: List[Article] = []
        seen_urls: set = set()

        end_dt = datetime.now(timezone.utc)
        start_dt = end_dt - timedelta(days=days)
        start_str = start_dt.strftime("%Y%m%d%H%M%S")
        end_str = end_dt.strftime("%Y%m%d%H%M%S")

        # Short per-article timeout: failed/slow fetches fall back to headline
        # quickly so the whole scraper stays within scrape_timeout.
        async with httpx.AsyncClient(headers=HEADERS, timeout=8, follow_redirects=True) as client:
            for i, qcfg in enumerate(self.QUERIES):
                if i > 0:
                    self.logger.info(f"GDELT: {self.DELAY_BETWEEN_QUERIES}s delay before next query...")
                    await asyncio.sleep(self.DELAY_BETWEEN_QUERIES)

                country_filter = " OR ".join(f"sourcecountry:{c}" for c in qcfg["countries"])
                query_str = f"{qcfg['keywords']} ({country_filter})"

                self.logger.info(f"GDELT: Querying [{qcfg['label']}]")
                gdelt_items = await self._fetch_gdelt(query_str, start_str, end_str)
                self.logger.info(f"GDELT [{qcfg['label']}]: {len(gdelt_items)} candidate articles")

                for item in gdelt_items:
                    if len(articles) >= self.MAX_ARTICLES_TOTAL:
                        break

                    url = item.get("url", "")
                    if not url or url in seen_urls:
                        continue
                    seen_urls.add(url)

                    title = item.get("title", "").strip()
                    if not title or len(title) < 10:
                        continue

                    pub_date = self._parse_gdelt_date(item.get("seendate", ""))
                    content = await self._fetch_content(client, url)
                    if not content:
                        # GDELT is a metadata index, not a content archive, and
                        # many of its foreign / local-language sources resist
                        # full-page scraping. Fall back to the headline so the
                        # candidate still contributes discovery-level signal
                        # rather than being dropped (the reason GDELT yielded 0).
                        content = title

                    # Start with GDELT-assigned region, enrich with keyword inference
                    region_tags = [qcfg["region_tag"]]
                    for r in self._infer_regions(title + " " + content):
                        if r not in region_tags:
                            region_tags.append(r)

                    article = Article(
                        source=f"GDELT/{item.get('domain', 'unknown')}",
                        url=url,
                        title=title,
                        published_date=pub_date,
                        content=content,
                        author=None,
                        region_tags=region_tags,
                    )
                    articles.append(article)
                    self.logger.info(f"GDELT scraped: {title[:65]}")

        self.logger.info(f"GDELT total: {len(articles)} articles ({len(seen_urls)} unique URLs)")
        return articles

    async def _fetch_gdelt(self, query: str, start: str, end: str, retries: int = 2) -> List[Dict]:
        """Query GDELT DOC 2.0 API with exponential backoff on rate limit."""
        params = {
            "query": query,
            "mode": "artlist",
            "maxrecords": str(self.MAX_RECORDS_PER_QUERY),
            "startdatetime": start,
            "enddatetime": end,
            "format": "json",
        }

        # Use httpx instead of urllib for better reliability
        async with httpx.AsyncClient(timeout=30.0) as client:
            for attempt in range(retries + 1):
                try:
                    resp = await client.get(self.GDELT_URL, params=params, headers=HEADERS, follow_redirects=True)
                    resp.raise_for_status()

                    # Handle empty responses
                    if not resp.content or len(resp.content) == 0:
                        self.logger.warning(f"GDELT returned empty response")
                        return []

                    data = resp.json()
                    return data.get("articles", [])

                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 429:
                        # Aggressive exponential backoff for rate limits
                        # attempt 0: 45s, attempt 1: 90s, attempt 2: 180s
                        wait = 45 * (2 ** attempt)
                        self.logger.warning(f"GDELT rate limited (attempt {attempt+1}/{retries+1}). Waiting {wait}s...")
                        await asyncio.sleep(wait)
                    else:
                        self.logger.warning(f"GDELT HTTP {e.response.status_code}")
                        return []
                except json.JSONDecodeError as e:
                    self.logger.warning(f"GDELT returned non-JSON response: {e}")
                    return []
                except Exception as e:
                    self.logger.warning(f"GDELT query error: {e}")
                    if attempt < retries:
                        await asyncio.sleep(10)
                    else:
                        return []
        return []

    def _parse_gdelt_date(self, date_str: str) -> datetime:
        """Parse GDELT seendate: 20260522T124500Z or 20260522124500"""
        if not date_str:
            return datetime.now(timezone.utc).replace(tzinfo=None)
        # Strip T and Z to normalize both variants
        clean = date_str.replace('T', '').replace('Z', '')
        for fmt, length in [("%Y%m%d%H%M%S", 14), ("%Y%m%d%H%M", 12), ("%Y%m%d", 8)]:
            try:
                return datetime.strptime(clean[:length], fmt)
            except ValueError:
                continue
        return datetime.now(timezone.utc).replace(tzinfo=None)

    async def _fetch_content(self, client: httpx.AsyncClient, url: str) -> str:
        """Fetch and extract article text from URL."""
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'lxml')
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
            self.logger.debug(f"Content fetch failed {url}: {e}")
            return ''

    def _infer_regions(self, text: str) -> List[str]:
        regions = []
        t = text.lower()
        if any(kw in t for kw in ['iran', 'iraq', 'syria', 'israel', 'gaza', 'lebanon', 'yemen', 'saudi', 'middle east', 'strait of hormuz', 'persian gulf']):
            regions.append('Middle East')
        if any(kw in t for kw in ['china', 'taiwan', 'south china sea', 'japan', 'korea', 'indo-pacific', 'pacific', 'philippines', 'australia', 'vietnam', 'asean']):
            regions.append('Indo-Pacific')
        if any(kw in t for kw in ['ukraine', 'russia', 'nato', 'europe', 'africa', 'balkans', 'poland', 'belarus', 'finland', 'estonia']):
            regions.append('Europe/Africa')
        if any(kw in t for kw in ['latin america', 'venezuela', 'cuba', 'mexico', 'brazil', 'colombia', 'americas', 'caribbean', 'argentina', 'peru']):
            regions.append('Western Hemisphere')
        return regions if regions else ['Global']
