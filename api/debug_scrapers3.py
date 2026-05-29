"""Probe BD article content + new source structures."""
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re


async def get_html(url, wait="networkidle"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        })
        try:
            await page.goto(url, wait_until=wait, timeout=30000)
        except Exception:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        html = await page.content()
        await browser.close()
    return html


def show_links(soup, label, min_text=20, url_filter=None):
    print(f"\n  --- {label} article links ---")
    count = 0
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True)
        if len(text) < min_text or len(text) > 150:
            continue
        if url_filter and not url_filter(href):
            continue
        if any(x in href for x in ['#', 'javascript:', 'mailto:', 'twitter.', 'facebook.', 'linkedin.']):
            continue
        # Find nearby time
        parent = a.find_parent(['article', 'div', 'li', 'section'])
        t = parent.find('time') if parent else None
        date_str = t.get('datetime', t.get_text(strip=True)[:20] if t else '') if t else ''
        print(f"    href={href[:70]}")
        print(f"    text={text[:70]}")
        if date_str:
            print(f"    date={date_str}")
        count += 1
        if count >= 5:
            break


def show_content_selectors(soup, label):
    print(f"\n  --- {label} content selectors ---")
    for sel in ['.entry-content', '.post-content', '.article-content', '.article-body',
                '.post__content', '.post__body', '.td-post-content', '.article__body',
                '.story-body', '.story-content', 'article', 'main']:
        e = soup.select_one(sel)
        if e:
            text = e.get_text(strip=True)
            if len(text) > 100:
                print(f"    FOUND {sel}: {len(text)} chars | {text[:80]}")


async def probe_bd_article():
    print("\n=== Breaking Defense ARTICLE PAGE ===")
    html = await get_html("https://breakingdefense.com/2026/05/romania-deploys-f-16s-against-russian-drone-strikes-on-civilian-infrastructure/")
    soup = BeautifulSoup(html, 'lxml')
    show_content_selectors(soup, "Breaking Defense article")
    # Also find date
    for sel in ['time', '.entry-date', '.post-date', 'span[class*=date]', '[class*=pubdate]']:
        e = soup.select_one(sel)
        if e:
            print(f"    DATE {sel}: datetime={e.get('datetime','')} text={e.get_text(strip=True)[:30]}")
            break


async def probe_d1_article():
    print("\n=== Defense One ARTICLE PAGE ===")
    html = await get_html("https://www.defenseone.com/policy/2026/05/house-draft-defense-policy-bill-leaves-some-trump-admins-top-priorities-out/413774/")
    soup = BeautifulSoup(html, 'lxml')
    show_content_selectors(soup, "Defense One article")
    for sel in ['time', '.article-date', '.pub-date', 'span[class*=date]']:
        e = soup.select_one(sel)
        if e:
            print(f"    DATE {sel}: datetime={e.get('datetime','')} text={e.get_text(strip=True)[:30]}")
            break


async def probe_warontherocks():
    print("\n=== War on the Rocks ===")
    html = await get_html("https://warontherocks.com/")
    soup = BeautifulSoup(html, 'lxml')
    show_links(soup, "WOTR listing", url_filter=lambda h: 'warontherocks.com/20' in h)
    # Also check date elements
    for t in soup.find_all('time')[:2]:
        print(f"  time: datetime={t.get('datetime','')} text={t.get_text(strip=True)[:30]}")


async def probe_csis():
    print("\n=== CSIS ===")
    html = await get_html("https://www.csis.org/analysis")
    soup = BeautifulSoup(html, 'lxml')
    show_links(soup, "CSIS listing", url_filter=lambda h: 'csis.org/analysis' in h or 'csis.org/blogs' in h)
    for t in soup.find_all('time')[:2]:
        print(f"  time: datetime={t.get('datetime','')} text={t.get_text(strip=True)[:30]}")


async def probe_thewarzone():
    print("\n=== The War Zone ===")
    html = await get_html("https://www.twz.com/")
    soup = BeautifulSoup(html, 'lxml')
    show_links(soup, "TWZ listing", url_filter=lambda h: 'twz.com/20' in h or '/war/' in h or '/news/' in h)


async def main():
    await probe_d1_article()
    await probe_bd_article()
    await probe_warontherocks()
    await probe_csis()
    await probe_thewarzone()


if __name__ == "__main__":
    asyncio.run(main())
