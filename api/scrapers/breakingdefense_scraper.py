# Breaking Defense scraper - RSS feed based
from .base_rss_scraper import RSSBaseScraper


class BreakingDefenseScraper(RSSBaseScraper):
    """
    Scraper for Breaking Defense (breakingdefense.com).
    Covers emerging defense tech, military procurement, defense industry.
    All content is defense-focused - no topic filter needed.
    """

    FEED_URL = "https://breakingdefense.com/feed/"

    def __init__(self):
        super().__init__("Breaking Defense")
