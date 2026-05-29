# War on the Rocks scraper - RSS feed based (replaces paywalled IISS)
from .base_rss_scraper import RSSBaseScraper


class WarOnTheRocksScraper(RSSBaseScraper):
    """
    Scraper for War on the Rocks (warontherocks.com).
    Peer-reviewed analysis on national security, defense strategy, and
    international relations. High-quality strategic depth - similar tier to IISS.
    """

    FEED_URL = "https://warontherocks.com/feed/"

    def __init__(self):
        super().__init__("War on the Rocks")
