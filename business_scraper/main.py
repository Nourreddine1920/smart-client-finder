from utils.csv_exporter import save_to_csv
from utils.csv_exporter import save_google_maps_data
from utils.csv_exporter import kompass_save_to_csv
from scrapers.yellowpages_scraper import scrape_yellowpages
from scrapers.googlemaps_scraper import GoogleMapsScraper
from scrapers.kompass_scraper import scrape_kompass
import os

# Keywords and cities for scraping
keywords = ["Electric Companies", "Marketing Agency"]
cities = ["New York", "Los Angeles, CA"]

all_data = []

# Scraping each keyword for each city
for keyword in keywords:
    for city in cities:
        print(f"Scraping {keyword} in {city}...")
        data = scrape_yellowpages(keyword, city, max_pages=2)  # You can change the number of pages to scrape
        all_data.extend(data)

# Save the data to CSV
save_to_csv(all_data)
print("[OK] Scraping completed.")

# # Your Google Maps API key
# API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
# if not API_KEY:
#     raise ValueError("Google Maps API key not found. Please set the 'GOOGLE_MAPS_API_KEY' environment variable.")

# List to store all scraped data
all_data = []

for keyword in keywords:
    for city in cities:
        # Initialize the scraper with the API key
        google_scraper = GoogleMapsScraper(query=keyword, location=city, max_pages=2)
        print(f"Scraping Google Maps for '{keyword}' in '{city}'...")

        # Scrape data using the API
        google_data = google_scraper.scrape()
        if google_data:
            all_data.extend(google_data)
            print(f"[OK] Scraped {len(google_data)} results for '{keyword}' in '{city}'.")
        else:
            print(f"[WARNING] No data found for '{keyword}' in '{city}'.")

        # Save the combined data to a CSV file after each city
        save_google_maps_data(all_data, filename="combined_scraped_data.csv")
        print("[OK] Combined data saved to 'combined_scraped_data.csv'.")

print("[DONE] Scraping completed.")

# Scraping from the kompass website
for keyword in keywords:
    for city in cities:
        print(f"Scraping {keyword} in {city}...")
        data = scrape_kompass(keyword, city, max_pages=2)  # You can change the number of pages to scrape
        all_data.extend(data)

# Save the data to CSV
kompass_save_to_csv(all_data)
print("[OK] Kompass datas scraping completed.")