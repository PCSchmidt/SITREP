# The War Zone scraper - RSS feed based
from .base_rss_scraper import RSSBaseScraper


class TheWarZoneScraper(RSSBaseScraper):
    """
    Scraper for The War Zone (twz.com).
    Covers military aviation, naval operations, weapons systems, and
    classified/emerging defense technology. Strong visual/equipment coverage.
    """

    FEED_URL = "https://www.twz.com/feed"

    def __init__(self):
        super().__init__("The War Zone")
