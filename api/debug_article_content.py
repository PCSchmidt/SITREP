# Debug article content extraction
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def debug_article():
    """Check structure of ISW article page"""
    url = "https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-may-22-2026/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            print(f"Fetching: {url}")
            await page.goto(url, wait_until="networkidle", timeout=30000)

            html = await page.content()
            soup = BeautifulSoup(html, 'lxml')

            # Try different content selectors
            print("\n=== Trying content selectors ===")
            selectors = [
                '.field-name-body',
                'article .content',
                '.node-content',
                '.entry-content',
                'article',
                '.post-content',
                'main',
                '.article-body',
            ]

            for selector in selectors:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text(separator=' ', strip=True)
                    print(f"{selector}: {len(text)} chars")
                    if len(text) > 0:
                        print(f"  Preview: {text[:150]}...")
                else:
                    print(f"{selector}: NOT FOUND")

        except Exception as e:
            print(f"\n[ERROR] {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_article())
