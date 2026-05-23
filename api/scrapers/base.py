# Base scraper class with shared functionality
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Article:
    """Data class for scraped articles"""

    def __init__(
        self,
        source: str,
        url: str,
        title: str,
        published_date: datetime,
        content: str,
        author: Optional[str] = None,
        region_tags: Optional[List[str]] = None
    ):
        self.source = source
        self.url = url
        self.title = title
        self.published_date = published_date
        self.content = content
        self.author = author
        self.region_tags = region_tags or []

    def to_dict(self) -> Dict:
        """Convert to JSON-serializable dict"""
        return {
            "source": self.source,
            "url": self.url,
            "title": self.title,
            "published_date": self.published_date.isoformat(),
            "author": self.author,
            "content": self.content,
            "region_tags": self.region_tags,
            "scraped_at": datetime.utcnow().isoformat()
        }


class BaseScraper(ABC):
    """Abstract base class for all source scrapers"""

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.logger = logging.getLogger(f"scraper.{source_name}")

    @abstractmethod
    async def scrape_recent_articles(self, days: int = 7) -> List[Article]:
        """
        Scrape articles from the last N days.

        Args:
            days: Number of days to look back (default: 7 for weekly briefing)

        Returns:
            List of Article objects
        """
        pass

    def save_to_json(self, articles: List[Article], output_dir: str = "data/scraped"):
        """
        Save scraped articles to JSON file.

        Args:
            articles: List of Article objects
            output_dir: Directory to save JSON files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.utcnow().strftime("%Y-%m-%d")
        filename = f"{self.source_name.lower().replace(' ', '_')}_{timestamp}.json"
        filepath = output_path / filename

        data = {
            "source": self.source_name,
            "scraped_at": datetime.utcnow().isoformat(),
            "article_count": len(articles),
            "articles": [article.to_dict() for article in articles]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        self.logger.info(f"Saved {len(articles)} articles to {filepath}")
        return str(filepath)

    def is_recent(self, date: datetime, days: int = 7) -> bool:
        """Check if a date is within the last N days"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        return date >= cutoff
