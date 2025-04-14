from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


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

def scrape_kompass(keyword, max_pages=1):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for production
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()

        for page_num in range(1, max_pages + 1):
            search_url = f"https://tn.kompass.com/en/searchCompanies?text={keyword.replace(' ', '+')}&searchType=COMPANYNAME&pageNumber={page_num}"
            print(f"Fetching: {search_url}")

            try:
                page.goto(search_url, timeout=20000)
                page.wait_for_selector(".company-search-result", timeout=10000)  # Wait for the company cards to load
                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                listings = soup.select(".company-search-result")  # Update selector for company cards

                if not listings:
                    print(f"[!] No listings found on page: {search_url}")
                    continue

                for listing in listings:
                    name_tag = listing.select_one(".company-name a")
                    website_tag = listing.select_one(".website a")
                    phone_tag = listing.select_one(".phone")
                    location_tag = listing.select_one(".address")

                    name = name_tag.text.strip() if name_tag else "N/A"
                    website = website_tag["href"] if website_tag else "N/A"
                    phone = phone_tag.text.strip() if phone_tag else "N/A"
                    location = location_tag.text.strip() if location_tag else "N/A"

                    email = extract_email_from_website(page, website) if website != "N/A" else "N/A"

                    results.append({
                        "name": name,
                        "website": website,
                        "email": email,
                        "phone": phone,
                        "location": location,
                        "source": "Kompass"
                    })

            except Exception as e:
                print(f"[!] Timeout or error on page {search_url}: {str(e)}")

        browser.close()

    return results


def scrape_kompass_with_selenium(keyword):
    results = []
    driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed and in PATH
    driver.get(f"https://tn.kompass.com/en/searchCompanies?text={keyword.replace(' ', '+')}&searchType=COMPANYNAME")

    page_num = 1
    while True:
        print(f"Fetching page {page_num}...")
        time.sleep(5)  # Wait for the page to load

        try:
            # Find all company cards on the page
            listings = driver.find_elements(By.CSS_SELECTOR, ".titleSpan")  # Update selector for company cards
            if not listings:
                print(f"[!] No more listings found on page {page_num}. Stopping pagination.")
                break

            for listing in listings:
                try:
                    name = listing.find_element(By.CSS_SELECTOR, ".company-name a").text
                except:
                    name = "N/A"

                try:
                    website = listing.find_element(By.CSS_SELECTOR, ".company-website a").get_attribute("href")
                except:
                    website = "N/A"

                try:
                    phone = listing.find_element(By.CSS_SELECTOR, ".company-phone").text
                except:
                    phone = "N/A"

                try:
                    location = listing.find_element(By.CSS_SELECTOR, ".company-address").text
                except:
                    location = "N/A"

                results.append({
                    "name": name,
                    "website": website,
                    "phone": phone,
                    "location": location,
                    "source": "Kompass"
                })

            print(f"[OK] Scraped {len(listings)} companies from page {page_num}.")
            page_num += 1

            # Click the "Next" button to go to the next page
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, ".pagination-next a")  # Update selector for the "Next" button
                next_button.click()
            except:
                print("[!] No next button found. Stopping pagination.")
                break

        except Exception as e:
            print(f"[!] Error on page {page_num}: {str(e)}")
            break

    driver.quit()
    return results

# # Example usage
# if __name__ == "__main__":
#     keyword = "electrical companies"
#     data = scrape_kompass_with_selenium(keyword)
#     for company in data:
#         print(company)