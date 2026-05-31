# ISW (Institute for the Study of War) scraper
from datetime import datetime
from typing import List
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re

from .base import BaseScraper, Article


class ISWScraper(BaseScraper):
    """Scraper for Institute for the Study of War (ISW)"""

    BASE_URL = "https://www.understandingwar.org"
    ARTICLES_URL = f"{BASE_URL}/publications"

    def __init__(self):
        super().__init__("ISW")

    async def scrape_recent_articles(self, days: int = 7) -> List[Article]:
        """
        Scrape recent ISW articles.

        ISW publishes daily assessments and strategic updates on:
        - Ukraine/Russia war
        - Iran and its proxies
        - Middle East geopolitics
        """
        articles = []

        async with async_playwright() as p:
            # Launch browser in headless mode
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                self.logger.info(f"Scraping ISW articles from {self.ARTICLES_URL}")
                # Use domcontentloaded (not networkidle, which can hang forever on
                # sites with persistent connections) with an explicit timeout.
                await page.goto(self.ARTICLES_URL, wait_until="domcontentloaded", timeout=30000)

                # Get page HTML
                html = await page.content()
                soup = BeautifulSoup(html, 'lxml')

                # ISW uses h3 links for article titles
                article_links = soup.select('h3 a')

                for link_elem in article_links:
                    try:
                        # Extract title and link
                        title = link_elem.get_text(strip=True)
                        article_url = link_elem.get('href', '')

                        # Skip if no URL or if it's a navigation link
                        if not article_url or 'about' in article_url.lower():
                            continue

                        if not article_url.startswith('http'):
                            article_url = self.BASE_URL + article_url

                        # Parse date from title (ISW format: "Title, May 22, 2026")
                        date_match = re.search(r'([A-Z][a-z]+)\s+(\d{1,2}),\s+(\d{4})', title)
                        if date_match:
                            date_text = date_match.group(0)
                            pub_date = self._parse_date(date_text)
                        else:
                            pub_date = datetime.utcnow()

                        # Check if article is recent
                        if not self.is_recent(pub_date, days):
                            continue

                        # Scrape full article content
                        content = await self._scrape_article_content(page, article_url)

                        # Infer region tags based on content
                        region_tags = self._infer_regions(title + " " + content)

                        article = Article(
                            source="ISW",
                            url=article_url,
                            title=title,
                            published_date=pub_date,
                            content=content,
                            author="ISW",
                            region_tags=region_tags
                        )
                        articles.append(article)
                        self.logger.info(f"Scraped: {title}")

                        # Limit to prevent overwhelming the server
                        if len(articles) >= 20:
                            break

                    except Exception as e:
                        self.logger.warning(f"Failed to parse article row: {e}")
                        continue

            except Exception as e:
                self.logger.error(f"Failed to scrape ISW: {e}")
            finally:
                await browser.close()

        self.logger.info(f"Scraped {len(articles)} articles from ISW")
        return articles

    async def _scrape_article_content(self, page, url: str) -> str:
        """Navigate to article page and extract full content"""
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            html = await page.content()
            soup = BeautifulSoup(html, 'lxml')

            # ISW articles are in <article> tag
            content_elem = soup.select_one('article, main')
            if content_elem:
                # Remove script/style/nav/footer tags
                for tag in content_elem.find_all(['script', 'style', 'nav', 'footer', 'header']):
                    tag.decompose()
                return content_elem.get_text(separator='\n', strip=True)
            return ""
        except Exception as e:
            self.logger.warning(f"Failed to scrape article content from {url}: {e}")
            return ""

    def _parse_date(self, date_text: str) -> datetime:
        """Parse various date formats ISW uses"""
        # Try common formats: "May 21, 2026", "2026-05-21", etc.
        try:
            # Remove extra text like "Published: "
            date_text = re.sub(r'Published:?\s*', '', date_text, flags=re.IGNORECASE)
            date_text = date_text.strip()

            # Try parsing
            for fmt in ["%B %d, %Y", "%Y-%m-%d", "%m/%d/%Y", "%d %B %Y"]:
                try:
                    return datetime.strptime(date_text, fmt)
                except ValueError:
                    continue

            # Fallback to current date if parsing fails
            self.logger.warning(f"Could not parse date: {date_text}")
            return datetime.utcnow()
        except Exception as e:
            self.logger.warning(f"Date parsing error: {e}")
            return datetime.utcnow()

    def _infer_regions(self, text: str) -> List[str]:
        """Infer geographic regions from article text"""
        regions = []
        text_lower = text.lower()

        # Middle East keywords
        if any(kw in text_lower for kw in ['iran', 'iraq', 'syria', 'israel', 'gaza', 'lebanon', 'yemen', 'saudi', 'uae', 'middle east']):
            regions.append("Middle East")

        # Indo-Pacific keywords
        if any(kw in text_lower for kw in ['china', 'taiwan', 'south china sea', 'japan', 'korea', 'indo-pacific', 'pacific']):
            regions.append("Indo-Pacific")

        # Europe/Africa keywords
        if any(kw in text_lower for kw in ['ukraine', 'russia', 'europe', 'nato', 'africa', 'balkans', 'poland']):
            regions.append("Europe/Africa")

        # Western Hemisphere keywords
        if any(kw in text_lower for kw in ['latin america', 'venezuela', 'cuba', 'mexico', 'brazil', 'americas']):
            regions.append("Western Hemisphere")

        return regions if regions else ["Global"]
