# Americas Quarterly scraper - RSS feed based
from .base_rss_scraper import RSSBaseScraper


class AmericasQuarterlyScraper(RSSBaseScraper):
    """
    Scraper for Americas Quarterly (americasquarterly.org).
    Dedicated coverage of Latin America and the Caribbean: politics,
    economics, security, migration. Essential for Western Hemisphere
    intelligence that goes beyond US-centric perspectives.
    """

    FEED_URL = "https://americasquarterly.org/feed/"

    def __init__(self):
        super().__init__("Americas Quarterly")
