# Debug ISW website structure
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def debug_isw():
    """Fetch ISW page and inspect structure"""
    url = "https://www.understandingwar.org/publications"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            print(f"Fetching: {url}")
            await page.goto(url, wait_until="networkidle", timeout=30000)

            html = await page.content()
            soup = BeautifulSoup(html, 'lxml')

            # Save HTML to file for inspection
            with open("isw_debug.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print("\n[SAVED] HTML saved to isw_debug.html")

            # Try different selectors
            print("\n=== Trying different article selectors ===")

            selectors = [
                'div.views-row',
                'article',
                '.publication',
                '.view-content > div',
                'div[class*="publication"]',
                'div[class*="article"]',
            ]

            for selector in selectors:
                elements = soup.select(selector)
                print(f"{selector}: {len(elements)} matches")

            # Check for h3/h2 links
            print("\n=== Looking for title links ===")
            title_selectors = ['h3 a', 'h2 a', '.title a', 'a.headline']
            for selector in title_selectors:
                elements = soup.select(selector)
                print(f"{selector}: {len(elements)} matches")
                if elements:
                    print(f"  First match: {elements[0].get_text(strip=True)[:80]}")

        except Exception as e:
            print(f"\n[ERROR] {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_isw())
