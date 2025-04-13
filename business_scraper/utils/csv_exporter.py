import csv
import os

def save_to_csv(data, filename="data/leads.csv"):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"[OK] Saved {len(data)} records to {filename}")

def save_google_maps_data(data, filename="data/google_maps_leads.csv"):
    if not data:
        print("No Google Maps data to save.")
        return

    keys = data[0].keys()

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"[OK] Saved {len(data)} Google Maps records to {filename}")

def kompass_save_to_csv(data, filename="data/kompass_datas.csv"):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"[OK] Saved {len(data)} Kompass datas records to {filename}")