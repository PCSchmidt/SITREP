# IISS (International Institute for Strategic Studies) scraper
from datetime import datetime
from typing import List
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re

from .base import BaseScraper, Article


class IISSScraper(BaseScraper):
    """Scraper for International Institute for Strategic Studies"""

    BASE_URL = "https://www.iiss.org"
    ARTICLES_URL = f"{BASE_URL}/publications"

    def __init__(self):
        super().__init__("IISS")

    async def scrape_recent_articles(self, days: int = 7) -> List[Article]:
        """
        Scrape recent IISS publications.

        Focus areas:
        - Strategic analysis
        - Military balance assessments
        - Armed conflict monitoring
        - Security policy research
        """
        articles = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                self.logger.info(f"Scraping IISS from {self.ARTICLES_URL}")
                await page.goto(self.ARTICLES_URL, wait_until="networkidle")

                html = await page.content()
                soup = BeautifulSoup(html, 'lxml')

                # IISS publications listing
                publication_items = soup.select('.publication-item, article, .resource-item')

                for item in publication_items:
                    try:
                        title_elem = item.select_one('h2 a, h3 a, .title a')
                        if not title_elem:
                            continue

                        title = title_elem.get_text(strip=True)
                        article_url = title_elem.get('href', '')
                        if not article_url.startswith('http'):
                            article_url = self.BASE_URL + article_url

                        date_elem = item.select_one('time, .date, .published')
                        if date_elem:
                            date_text = date_elem.get('datetime') or date_elem.get_text(strip=True)
                            pub_date = self._parse_date(date_text)
                        else:
                            pub_date = datetime.utcnow()

                        if not self.is_recent(pub_date, days):
                            continue

                        author_elem = item.select_one('.author, .byline')
                        author = author_elem.get_text(strip=True) if author_elem else "IISS"

                        content = await self._scrape_article_content(page, article_url)
                        if not content:
                            continue

                        region_tags = self._infer_regions(title + " " + content)

                        article = Article(
                            source="IISS",
                            url=article_url,
                            title=title,
                            published_date=pub_date,
                            content=content,
                            author=author,
                            region_tags=region_tags
                        )
                        articles.append(article)
                        self.logger.info(f"Scraped: {title}")

                        if len(articles) >= 20:
                            break

                    except Exception as e:
                        self.logger.warning(f"Failed to parse publication: {e}")
                        continue

            except Exception as e:
                self.logger.error(f"Failed to scrape IISS: {e}")
            finally:
                await browser.close()

        self.logger.info(f"Scraped {len(articles)} publications from IISS")
        return articles

    async def _scrape_article_content(self, page, url: str) -> str:
        """Extract publication content"""
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            html = await page.content()
            soup = BeautifulSoup(html, 'lxml')

            # IISS content structure
            content_elem = soup.select_one('.publication-content, .article-body, .resource-content')
            if content_elem:
                for tag in content_elem.find_all(['script', 'style', 'nav', 'footer']):
                    tag.decompose()
                return content_elem.get_text(separator='\n', strip=True)
            return ""
        except Exception as e:
            self.logger.warning(f"Failed to scrape content from {url}: {e}")
            return ""

    def _parse_date(self, date_text: str) -> datetime:
        """Parse date formats"""
        try:
            if 'T' in date_text:
                return datetime.fromisoformat(date_text.replace('Z', '+00:00'))

            date_text = re.sub(r'Published:?\s*', '', date_text, flags=re.IGNORECASE).strip()
            for fmt in ["%B %d, %Y", "%Y-%m-%d", "%m/%d/%Y", "%d %B %Y", "%b %d, %Y"]:
                try:
                    return datetime.strptime(date_text, fmt)
                except ValueError:
                    continue
            return datetime.utcnow()
        except Exception:
            return datetime.utcnow()

    def _infer_regions(self, text: str) -> List[str]:
        """Infer geographic regions"""
        regions = []
        text_lower = text.lower()

        if any(kw in text_lower for kw in ['iran', 'iraq', 'syria', 'israel', 'gaza', 'middle east', 'gulf']):
            regions.append("Middle East")
        if any(kw in text_lower for kw in ['china', 'taiwan', 'south china sea', 'pacific', 'asia']):
            regions.append("Indo-Pacific")
        if any(kw in text_lower for kw in ['ukraine', 'russia', 'nato', 'europe', 'africa', 'balkans']):
            regions.append("Europe/Africa")
        if any(kw in text_lower for kw in ['latin america', 'venezuela', 'americas', 'caribbean']):
            regions.append("Western Hemisphere")

        return regions if regions else ["Global"]
