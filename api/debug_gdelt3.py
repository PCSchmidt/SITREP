"""GDELT probe v3 - test parenthesized OR syntax with long delays."""
import json, time, urllib.request
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; SITREP intelligence aggregator)'}
GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def safe(s): return (s or '').encode('ascii', 'replace').decode('ascii')


def query(label, q, days=7, n=4, delay_before=0):
    if delay_before:
        print(f"  Waiting {delay_before}s before next query...")
        time.sleep(delay_before)
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    params = {"query": q, "mode": "artlist", "maxrecords": str(n),
              "startdatetime": start.strftime("%Y%m%d%H%M%S"),
              "enddatetime": end.strftime("%Y%m%d%H%M%S"), "format": "json"}
    url = f"{GDELT_URL}?{urlencode(params)}"
    print(f"\n[{label}]")
    print(f"  Q: {safe(q)}")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as r:
                raw = r.read().decode('utf-8', errors='replace')
            data = json.loads(raw)
            arts = data.get("articles", [])
            print(f"  => {len(arts)} articles")
            for a in arts[:2]:
                print(f"     [{safe(a.get('sourcecountry','?'))} | {safe(a.get('language','?'))}] "
                      f"{safe(a.get('title',''))[:65]}")
            return len(arts)
        except urllib.error.HTTPError as e:
            wait = 30 * (attempt + 1)
            print(f"  HTTP {e.code} on attempt {attempt+1}. Wait {wait}s...")
            time.sleep(wait)
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < 2: time.sleep(10)
    return 0


print("=== GDELT syntax test (long delays) ===")
# Start with a long wait to let any rate limit reset
print("Initial 30s wait...")
time.sleep(30)

# Test 1: Parenthesized multi-country LatAm
n1 = query("LatAm parenthesized OR",
    "military security conflict (sourcecountry:BR OR sourcecountry:CO OR sourcecountry:MX OR sourcecountry:AR)")

# Test 2: Africa parenthesized OR
n2 = query("Africa parenthesized OR",
    "military conflict coup security (sourcecountry:ZA OR sourcecountry:KE OR sourcecountry:NG)",
    delay_before=20)

# Test 3: SE Asia parenthesized OR
n3 = query("SE Asia parenthesized OR",
    "military maritime security sovereignty (sourcecountry:ID OR sourcecountry:PH OR sourcecountry:VN)",
    delay_before=20)

print(f"\nTotal: {n1+n2+n3} articles. "
      f"{'Parenthesized OR works!' if n1+n2+n3 > 0 else 'Still failing - use individual queries.'}")
