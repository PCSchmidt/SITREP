# Defense One scraper
from datetime import datetime
from typing import List
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re

from .base import BaseScraper, Article


class DefenseOneScraper(BaseScraper):
    """Scraper for Defense One"""

    BASE_URL = "https://www.defenseone.com"
    ARTICLES_URL = f"{BASE_URL}/latest"

    def __init__(self):
        super().__init__("Defense One")

    async def scrape_recent_articles(self, days: int = 7) -> List[Article]:
        """
        Scrape recent Defense One articles.

        Focus areas:
        - Pentagon news and policy
        - Military technology
        - Defense procurement
        - National security strategy
        """
        articles = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                self.logger.info(f"Scraping Defense One from {self.ARTICLES_URL}")
                await page.goto(self.ARTICLES_URL, wait_until="networkidle")

                html = await page.content()
                soup = BeautifulSoup(html, 'lxml')

                # Defense One uses article cards
                article_cards = soup.select('article, .article-card, .story-card')

                for card in article_cards:
                    try:
                        # Extract title and link
                        title_elem = card.select_one('h2 a, h3 a, .headline a')
                        if not title_elem:
                            continue

                        title = title_elem.get_text(strip=True)
                        article_url = title_elem.get('href', '')
                        if not article_url.startswith('http'):
                            article_url = self.BASE_URL + article_url

                        # Extract date
                        date_elem = card.select_one('time, .date, .published-date')
                        if date_elem:
                            date_text = date_elem.get('datetime') or date_elem.get_text(strip=True)
                            pub_date = self._parse_date(date_text)
                        else:
                            pub_date = datetime.utcnow()

                        if not self.is_recent(pub_date, days):
                            continue

                        # Extract author
                        author_elem = card.select_one('.author, .byline')
                        author = author_elem.get_text(strip=True) if author_elem else "Defense One"

                        # Scrape full content
                        content = await self._scrape_article_content(page, article_url)
                        if not content:
                            continue

                        region_tags = self._infer_regions(title + " " + content)

                        article = Article(
                            source="Defense One",
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
                        self.logger.warning(f"Failed to parse article: {e}")
                        continue

            except Exception as e:
                self.logger.error(f"Failed to scrape Defense One: {e}")
            finally:
                await browser.close()

        self.logger.info(f"Scraped {len(articles)} articles from Defense One")
        return articles

    async def _scrape_article_content(self, page, url: str) -> str:
        """Extract article content from Defense One article page"""
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            html = await page.content()
            soup = BeautifulSoup(html, 'lxml')

            # Defense One article content
            content_elem = soup.select_one('article .article-body, .article-content, .story-content')
            if content_elem:
                for tag in content_elem.find_all(['script', 'style', 'nav', 'footer', 'aside']):
                    tag.decompose()
                return content_elem.get_text(separator='\n', strip=True)
            return ""
        except Exception as e:
            self.logger.warning(f"Failed to scrape content from {url}: {e}")
            return ""

    def _parse_date(self, date_text: str) -> datetime:
        """Parse Defense One date formats"""
        try:
            # Handle ISO format (from datetime attribute)
            if 'T' in date_text:
                return datetime.fromisoformat(date_text.replace('Z', '+00:00'))

            # Handle common formats
            date_text = re.sub(r'Published:?\s*', '', date_text, flags=re.IGNORECASE).strip()
            for fmt in ["%B %d, %Y", "%Y-%m-%d", "%m/%d/%Y", "%b %d, %Y"]:
                try:
                    return datetime.strptime(date_text, fmt)
                except ValueError:
                    continue

            return datetime.utcnow()
        except Exception:
            return datetime.utcnow()

    def _infer_regions(self, text: str) -> List[str]:
        """Infer geographic regions from article text"""
        regions = []
        text_lower = text.lower()

        if any(kw in text_lower for kw in ['iran', 'iraq', 'syria', 'israel', 'gaza', 'middle east', 'persian gulf']):
            regions.append("Middle East")
        if any(kw in text_lower for kw in ['china', 'taiwan', 'pacific', 'korea', 'japan', 'indo-pacific']):
            regions.append("Indo-Pacific")
        if any(kw in text_lower for kw in ['ukraine', 'russia', 'nato', 'europe', 'africa']):
            regions.append("Europe/Africa")
        if any(kw in text_lower for kw in ['venezuela', 'cuba', 'latin america', 'americas']):
            regions.append("Western Hemisphere")

        return regions if regions else ["Global"]
