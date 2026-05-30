# Foreign Policy scraper - RSS feed based
from .base_rss_scraper import RSSBaseScraper


class ForeignPolicyScraper(RSSBaseScraper):
    """
    Scraper for Foreign Policy (foreignpolicy.com).
    Covers US foreign policy, global affairs, diplomacy, and strategic analysis.
    Strong coverage of Americas, US-China relations, and global governance.
    """

    FEED_URL = "https://foreignpolicy.com/feed/"

    def __init__(self):
        super().__init__("Foreign Policy")
