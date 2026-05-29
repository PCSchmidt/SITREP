"""Probe RSS/Atom feeds for all target sources."""
import asyncio
import urllib.request
import xml.etree.ElementTree as ET


def try_feed(url, label):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; RSS reader)'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='replace')
        # Quick check it's actually a feed
        if '<rss' in content or '<feed' in content or '<channel' in content:
            root = ET.fromstring(content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            items = root.findall('.//item')
            if not items:
                items = root.findall('.//atom:entry', ns) or root.findall('.//entry')
            print(f"  [OK] {label}: {url}")
            print(f"     {len(items)} items found")
            for item in items[:2]:
                title = (item.findtext('title') or
                         item.findtext('{http://www.w3.org/2005/Atom}title') or '')
                link = (item.findtext('link') or
                        item.findtext('{http://www.w3.org/2005/Atom}link') or '')
                pubdate = (item.findtext('pubDate') or
                           item.findtext('{http://www.w3.org/2005/Atom}updated') or
                           item.findtext('updated') or '')
                print(f"     - {title[:70]}")
                print(f"       link={link[:70]}")
                print(f"       date={pubdate[:40]}")
            return True
        else:
            print(f"  [NO] {label}: {url} (not a feed)")
            return False
    except Exception as e:
        print(f"  [FAIL] {label}: {url} ({e})")
        return False


def main():
    print("=== RSS FEED DISCOVERY ===\n")

    candidates = [
        # Defense One
        ("Defense One - all", "https://www.defenseone.com/rss/all/"),
        ("Defense One - topics", "https://www.defenseone.com/rss/topics/"),
        # Breaking Defense
        ("Breaking Defense - feed", "https://breakingdefense.com/feed/"),
        ("Breaking Defense - feed2", "https://breakingdefense.com/feed/rss/"),
        # IISS (long shot)
        ("IISS - feed", "https://www.iiss.org/rss/"),
        ("IISS - analysis feed", "https://www.iiss.org/online-analysis/rss/"),
        # War on the Rocks (replace IISS)
        ("War on the Rocks", "https://warontherocks.com/feed/"),
        # CSIS
        ("CSIS - all", "https://www.csis.org/rss.xml"),
        ("CSIS - analysis", "https://www.csis.org/analysis/feed"),
        ("CSIS - feed", "https://www.csis.org/feed"),
        # Reuters
        ("Reuters - world", "https://feeds.reuters.com/reuters/worldnews"),
        ("Reuters - top news", "https://feeds.reuters.com/Reuters/worldNews"),
        # Al Jazeera
        ("Al Jazeera - news", "https://www.aljazeera.com/xml/rss/all.xml"),
        ("Al Jazeera - feed", "https://www.aljazeera.com/rss2.0.html"),
        # The War Zone / TWZ
        ("The War Zone - feed", "https://www.twz.com/feed"),
        ("The War Zone - feed2", "https://www.thedrive.com/the-war-zone/rss"),
        # Defense News
        ("Defense News - feed", "https://www.defensenews.com/rss/"),
        ("Defense News - feed2", "https://www.defensenews.com/feed/"),
        # Bellingcat
        ("Bellingcat - feed", "https://www.bellingcat.com/feed/"),
        # ISW (verify still working)
        ("ISW - verify", "https://www.understandingwar.org/rss.xml"),
    ]

    for label, url in candidates:
        try_feed(url, label)

    print("\nDone.")


if __name__ == "__main__":
    main()
