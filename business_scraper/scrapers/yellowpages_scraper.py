from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

def extract_email_from_website(page, website_url):
    try:
        page.goto(website_url, timeout=15000)
        page.wait_for_timeout(3000)  # wait 3s for content to load
        content = page.content()
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", content)
        return emails[0] if emails else None
    except Exception as e:
        print(f"[!] Failed to get email from {website_url}: {str(e)}")
        return None

def scrape_yellowpages(keyword, city, max_pages=1):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Try headless=False to debug
        page = browser.new_page()

        for page_num in range(1, max_pages + 1):
            search_url = f"https://www.yellowpages.com/search?search_terms={keyword.replace(' ', '+')}&geo_location_terms={city.replace(' ', '+')}&page={page_num}"
            print(f"Fetching: {search_url}")

            try:
                page.goto(search_url, timeout=20000)
                page.wait_for_selector("div.result", timeout=10000)
                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                listings = soup.select("div.result")

                if not listings:
                    print(f"[!] No listings found on page: {search_url}")
                    continue

                for listing in listings:
                    name_tag = listing.select_one(".business-name span")
                    website_tag = listing.select_one(".links a[href^='http']")
                    phone_tag = listing.select_one(".phones")
                    location_tag = listing.select_one(".adr")

                    name = name_tag.text.strip() if name_tag else ""
                    website = website_tag["href"] if website_tag else ""
                    phone = phone_tag.text.strip() if phone_tag else ""
                    location = location_tag.text.strip() if location_tag else ""

                    email = extract_email_from_website(page, website) if website else None

                    results.append({
                        "name": name,
                        "website": website,
                        "email": email,
                        "phone": phone,
                        "location": location,
                        "source": "YellowPages"
                    })

            except Exception as e:
                print(f"[!] Timeout or error on page {search_url}: {str(e)}")

        browser.close()

    return results
