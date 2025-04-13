from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import time

class GoogleMapsScraper:
    def __init__(self, query, location, max_pages=1):
        self.query = query
        self.location = location
        self.max_pages = max_pages
        self.base_url = "https://www.google.com/maps/search/"

    def get_search_url(self, page_num=1):
        return f"{self.base_url}{self.query}+in+{self.location}&page={page_num}"

    def extract_email_from_website(self, page, website_url):
        try:
            page.goto(website_url, timeout=15000)
            page.wait_for_timeout(3000)  # wait 3s for content to load
            content = page.content()
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", content)
            return emails[0] if emails else None
        except Exception as e:
            print(f"[!] Failed to get email from {website_url}: {str(e)}")
            return None

    def scrape(self):
        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_num in range(1, self.max_pages + 1):
                search_url = self.get_search_url(page_num)
                print(f"Fetching: {search_url}")

                try:
                    page.goto(search_url, timeout=20000)
                    page.wait_for_timeout(5000)  # Wait for content to load
                    html = page.content()
                    soup = BeautifulSoup(html, "html.parser")
                    listings = soup.select("div.place-result-container")  # Adjust selector based on actual structure

                    if not listings:
                        print(f"[!] No listings found on page: {search_url}")
                        continue

                    for listing in listings:
                        name_tag = listing.select_one("h3.place-name")
                        address_tag = listing.select_one("span.place-address")
                        phone_tag = listing.select_one("span.place-phone")
                        website_tag = listing.select_one("a.place-website")

                        name = name_tag.text.strip() if name_tag else "N/A"
                        address = address_tag.text.strip() if address_tag else "N/A"
                        phone = phone_tag.text.strip() if phone_tag else "N/A"
                        website = website_tag["href"] if website_tag else None
                        email = self.extract_email_from_website(page, website) if website else None

                        results.append({
                            "name": name,
                            "address": address,
                            "phone": phone,
                            "website": website,
                            "email": email,
                            "source": "Google Maps"
                        })

                except Exception as e:
                    print(f"[!] Timeout or error on page {search_url}: {str(e)}")

            browser.close()

        return results


if __name__ == "__main__":
    scraper = GoogleMapsScraper(query="restaurants", location="New York", max_pages=1)
    results = scraper.scrape()
    for result in results:
        print(result)
        time.sleep(1)  # Be respectful with delays