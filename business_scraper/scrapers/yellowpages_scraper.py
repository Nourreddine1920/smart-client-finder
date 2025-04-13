from playwright.sync_api import sync_playwright

def scrape_yellowpages(keyword, city, max_pages=1):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for page_num in range(1, max_pages + 1):
            search_url = f"https://www.yellowpages.com/search?search_terms={keyword.replace(' ', '+')}&geo_location_terms={city.replace(' ', '+')}&page={page_num}"
            print(f"Fetching: {search_url}")
            try:
                page.goto(search_url, timeout=60000)

                listings = page.locator("div.info")
                count = listings.count()

                for i in range(count):
                    block = listings.nth(i)

                    try:
                        name = block.locator("a.business-name").inner_text(timeout=1000) if block.locator("a.business-name").count() > 0 else None
                        phone = block.locator("div.phones").inner_text(timeout=1000) if block.locator("div.phones").count() > 0 else None
                        website = block.locator("a.track-visit-website").get_attribute("href") if block.locator("a.track-visit-website").count() > 0 else None

                        results.append({
                            "name": name,
                            "phone": phone,
                            "website": website,
                            "location": city,
                            "industry": keyword,
                            "source": "YellowPages"
                        })
                    except Exception as e:
                        print(f"[!] Error parsing one listing: {e}")

            except Exception as e:
                print(f"[!] Failed to fetch {search_url}: {e}")

        browser.close()

    return results
