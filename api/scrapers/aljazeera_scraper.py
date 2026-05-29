# Al Jazeera scraper - RSS feed based with topic filtering
from .base_rss_scraper import RSSBaseScraper


class AlJazeeraScraper(RSSBaseScraper):
    """
    Scraper for Al Jazeera (aljazeera.com).
    Covers global news - topic filter applied to keep only defense/geopolitical content.
    Provides non-Western perspective on Middle East, Africa, Asia conflicts.
    """

    FEED_URL = "https://www.aljazeera.com/xml/rss/all.xml"

    # Only keep articles relevant to defense, conflict, and geopolitics
    TOPIC_FILTER = [
        'war', 'military', 'troops', 'attack', 'strike', 'conflict', 'battle',
        'missile', 'weapons', 'nuclear', 'sanctions', 'nato', 'army', 'navy',
        'air force', 'invasion', 'ceasefire', 'drone', 'hostage', 'terrorist',
        'airstrike', 'bombardment', 'blockade', 'siege', 'offensive', 'defense',
        'security', 'intel', 'espionage', 'coup', 'rebel', 'insurgent',
        'israel', 'gaza', 'ukraine', 'russia', 'iran', 'hamas', 'hezbollah',
        'china', 'taiwan', 'north korea', 'pentagon', 'armed forces',
    ]

    def __init__(self):
        super().__init__("Al Jazeera")
