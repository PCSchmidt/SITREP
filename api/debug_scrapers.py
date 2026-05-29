"""Debug script to probe live HTML structure of each broken scraper site."""
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def probe(url, label):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"})
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, 'lxml')
    print(f"\n{'='*60}")
    print(f"=== {label} : {url} ===")
    print(f"{'='*60}")

    # Show article/h2/h3 links
    for tag in ['article', 'h2', 'h3']:
        elems = soup.find_all(tag)[:5]
        for e in elems:
            links = e.find_all('a', href=True)
            if links:
                href = links[0]['href'][:80]
                text = links[0].get_text(strip=True)[:70]
                print(f"  <{tag}> href={href}")
                print(f"         text={text}")
                break

    # Show time elements
    times = soup.find_all('time')[:3]
    for t in times:
        dt = t.get('datetime', '')
        txt = t.get_text(strip=True)[:40]
        print(f"  <time datetime={dt}> text={txt}")

    # Show divs with article-like class names
    seen = set()
    for div in soup.find_all(['div', 'li', 'section'], class_=True)[:60]:
        classes = ' '.join(div.get('class', []))
        key_class = classes.split()[0] if classes else ''
        if key_class in seen:
            continue
        if any(kw in classes.lower() for kw in ['article', 'story', 'post', 'card', 'item', 'entry', 'headline', 'pub', 'resource', 'teaser', 'listing']):
            links = div.find_all('a', href=True)
            if links:
                seen.add(key_class)
                print(f"  <div class='{classes[:70]}'> -> {links[0]['href'][:60]}")
                # Show any child h2/h3
                for h in div.find_all(['h2', 'h3', 'h4'])[:1]:
                    print(f"    child <{h.name}>: {h.get_text(strip=True)[:60]}")

    # Show all anchor hrefs on the page that look like article links
    print(f"\n  Sample article-like hrefs:")
    hrefs_shown = 0
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True)
        if len(text) > 20 and len(text) < 120 and '/' in href and not any(x in href for x in ['#', 'javascript', 'mailto', 'twitter', 'facebook', 'linkedin']):
            print(f"    {href[:80]} | {text[:60]}")
            hrefs_shown += 1
            if hrefs_shown >= 8:
                break


async def main():
    await probe("https://www.defenseone.com/news/", "Defense One")
    await probe("https://breakingdefense.com/", "Breaking Defense")
    await probe("https://www.iiss.org/online-analysis/", "IISS")


if __name__ == "__main__":
    asyncio.run(main())
