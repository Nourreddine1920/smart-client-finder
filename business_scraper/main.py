from utils.csv_exporter import save_to_csv
from scrapers.yellowpages_scraper import scrape_yellowpages
from utils.csv_exporter import save_to_csv
from scrapers.yellowpages_scraper import scrape_yellowpages
from utils.csv_exporter import save_to_csv

# Fake data just for testing
# dummy_data = [
#     {"name": "Test Company", "website": "https://example.com", "phone": "+123456", "location": "Dubai", "source": "TestSource"}
# ]

# save_to_csv(dummy_data)


# Let's run the yellow pages scraper and save the results to a CSV file

keywords = ["Electric Companies", "marketing agency"]
cities = ["New York", "Los Angeles, CA"]

all_data = []

for keyword in keywords:
    for city in cities:
        print(f"Scraping {keyword} in {city}...")
        data = scrape_yellowpages(keyword, city, max_pages=2)
        all_data.extend(data)

save_to_csv(all_data)
