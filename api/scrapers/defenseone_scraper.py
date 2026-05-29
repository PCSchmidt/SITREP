# Defense One scraper - RSS feed based
from .base_rss_scraper import RSSBaseScraper


class DefenseOneScraper(RSSBaseScraper):
    """
    Scraper for Defense One (defenseone.com).
    Covers Pentagon policy, military tech, national security strategy.
    All content is defense-focused - no topic filter needed.
    """

    FEED_URL = "https://www.defenseone.com/rss/all/"

    def __init__(self):
        super().__init__("Defense One")
