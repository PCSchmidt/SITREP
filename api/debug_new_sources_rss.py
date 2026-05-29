"""Probe RSS feeds for the 20 new candidate sources."""
import urllib.request
import xml.etree.ElementTree as ET

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; RSS reader)'}


def probe(label, url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='replace')
        if not ('<rss' in content or '<feed' in content or '<channel' in content):
            print(f"  [NO]   {label}: {url} (not a feed)")
            return
        root = ET.fromstring(content)
        items = root.findall('.//item') or root.findall('.//{http://www.w3.org/2005/Atom}entry') or root.findall('.//entry')
        title0 = ''
        if items:
            t = items[0].findtext('title') or items[0].findtext('{http://www.w3.org/2005/Atom}title') or ''
            title0 = t[:60]
        print(f"  [OK]   {label}: {len(items)} items | {title0}")
    except Exception as e:
        print(f"  [FAIL] {label}: {url} | {e}")


def main():
    print("=== New Source RSS Probes ===\n")

    print("-- Asia-Pacific --")
    probe("The Diplomat",         "https://thediplomat.com/feed/")
    probe("East Asia Forum",      "https://www.eastasiaforum.org/feed/")
    probe("Lowy Institute",       "https://www.lowyinstitute.org/rss.xml")
    probe("Lowy Institute (2)",   "https://www.lowyinstitute.org/publications/rss")
    probe("CSIS Analysis",        "https://www.csis.org/analysis/rss")
    probe("CSIS All",             "https://www.csis.org/rss.xml")

    print("\n-- Africa --")
    probe("ISS Africa",           "https://issafrica.org/rss.xml")
    probe("ISS Africa (2)",       "https://issafrica.org/iss-today/feed")
    probe("The Africa Report",    "https://www.theafricareport.com/feed/")
    probe("Chatham House Africa", "https://www.chathamhouse.org/rss.xml")
    probe("Chatham House (2)",    "https://www.chathamhouse.org/topics/africa/rss")

    print("\n-- Latin America --")
    probe("NACLA",                "https://nacla.org/rss.xml")
    probe("NACLA (2)",            "https://nacla.org/feed/")
    probe("AS-COA",               "https://www.as-coa.org/rss.xml")
    probe("AS-COA (2)",           "https://www.as-coa.org/feed/")

    print("\n-- Multi-Region --")
    probe("CFR All",              "https://www.cfr.org/rss/all")
    probe("CFR (2)",              "https://www.cfr.org/feed")
    probe("Crisis Group",         "https://www.crisisgroup.org/rss.xml")
    probe("Crisis Group (2)",     "https://www.crisisgroup.org/crisiswatch/feed")
    probe("Geopolitical Futures", "https://geopoliticalfutures.com/feed/")
    probe("SIPRI",                "https://www.sipri.org/rss.xml")
    probe("World Bank Blog",      "https://blogs.worldbank.org/rss.xml")
    probe("Foreign Policy",       "https://foreignpolicy.com/feed/")
    probe("Chatham House",        "https://www.chathamhouse.org/rss.xml")

    print("\nDone.")


if __name__ == "__main__":
    main()
