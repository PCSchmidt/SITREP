"""Second-pass debug: BD dates/content and IISS free URLs."""
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def get_html(url):
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
    return html


async def probe_bd_listing_dates():
    html = await get_html("https://breakingdefense.com/")
    soup = BeautifulSoup(html, 'lxml')
    print("=== BD LISTING - DATE/META ELEMENTS ===")
    for sel in ['time', 'span.date', '.post-date', '.entry-date', '.post-card__date',
                '.post-card__meta', '.post-card__byline', '.byline', '[class*=date]', '[class*=meta]']:
        elems = soup.select(sel)[:2]
        for e in elems:
            print(f"  {sel}: datetime='{e.get('datetime','')}' text='{e.get_text(strip=True)[:60]}'")
    print("\n  Articles with URLs containing /20:")
    for a in soup.find_all('a', href=True):
        if '/2026/' in a['href'] or '/2025/' in a['href']:
            # Look for nearby time element
            parent = a.find_parent(['article', 'div', 'li'])
            date_e = parent.find('time') if parent else None
            date_class = parent.find(class_=lambda c: c and 'date' in c.lower()) if parent else None
            print(f"  href={a['href'][:70]}")
            print(f"    title={a.get_text(strip=True)[:60]}")
            if date_e:
                print(f"    time: {date_e.get('datetime','')} / {date_e.get_text(strip=True)[:30]}")
            if date_class:
                print(f"    date-class: {date_class.get_text(strip=True)[:30]}")
            break  # Just first one


async def probe_bd_article():
    html = await get_html("https://breakingdefense.com/2026/05/romania-deploys-f-16s-against-russian-drone-strikes-on-civilian-infrastructure/")
    soup = BeautifulSoup(html, 'lxml')
    print("\n=== BD ARTICLE PAGE ===")
    for sel in ['.entry-content', '.article-content', '.post-content', '.post__content',
                '.article__body', '.post__body', 'article .content', '.td-post-content']:
        e = soup.select_one(sel)
        if e:
            print(f"  CONTENT FOUND: {sel} ({len(e.get_text())} chars)")
            print(f"    preview: {e.get_text(strip=True)[:100]}")
    print("  Date elements on article page:")
    for sel in ['time', '.date', '.entry-date', '.post-date', '.td-post-date',
                '.article__date', '.post__date', 'span[class*=date]']:
        e = soup.select_one(sel)
        if e:
            print(f"  {sel}: datetime='{e.get('datetime','')}' text='{e.get_text(strip=True)[:40]}'")


async def probe_iiss():
    print("\n=== IISS BLOG ===")
    html = await get_html("https://www.iiss.org/iiss-blogs/")
    soup = BeautifulSoup(html, 'lxml')
    articles_found = 0
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True)
        if '/iiss-blogs/' in href and len(text) > 15 and href != 'https://www.iiss.org/iiss-blogs/':
            print(f"  {href[:80]} | {text[:60]}")
            articles_found += 1
            if articles_found >= 8:
                break
    if articles_found == 0:
        print("  No articles found - checking all links with dates...")
        for a in soup.find_all('a', href=True)[:20]:
            print(f"  {a['href'][:80]} | {a.get_text(strip=True)[:50]}")


async def main():
    await probe_bd_listing_dates()
    await probe_bd_article()
    await probe_iiss()


if __name__ == "__main__":
    asyncio.run(main())
