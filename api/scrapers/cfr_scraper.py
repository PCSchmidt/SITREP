# Council on Foreign Relations scraper - RSS feed based
from .base_rss_scraper import RSSBaseScraper


class CFRScraper(RSSBaseScraper):
    """
    Scraper for Council on Foreign Relations (cfr.org).
    Covers US foreign policy, international relations, security affairs.
    Authoritative analysis on Western Hemisphere issues, particularly
    migration, trade, and regional security.
    """

    FEED_URL = "https://www.cfr.org/rss/all.xml"

    def __init__(self):
        super().__init__("Council on Foreign Relations")
