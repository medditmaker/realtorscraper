import requests
import json
from datetime import datetime
import time

def scrape():
    # 1. Setup a Session (this saves cookies like a real browser)
    session = requests.Session()
    
    # 2. Perfect Headers (Mimicking Chrome on Windows)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.realtor.ca",
        "Referer": "https://www.realtor.ca/",
        "ContentType": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    payload = {
        "ZoomLevel": "11",
        "LatitudeMin": "50.605",
        "LatitudeMax": "50.765",
        "LongitudeMin": "-120.515",
        "LongitudeMax": "-120.195",
        "PriceMin": "650000",
        "BedRange": "4-0",
        "TransactionTypeId": "2",
        "PropertySearchTypeId": "1",
        "Sort": "6-D",
        "RecordsPerPage": "50",
        "CultureId": "1",
        "ApplicationId": "1"
    }

    try:
        # Step A: Visit the home page first to get cookies
        session.get("https://www.realtor.ca", headers=headers, timeout=15)
        time.sleep(2) # Wait a second to seem human
        
        # Step B: Make the search request
        url = "https://api37.realtor.ca/Listing.svc/PropertySearch_Post"
        response = session.post(url, data=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            listings = data.get("Results", [])
            
            cleaned_data = []
            for l in listings:
                cleaned_data.append({
                    "mls": l.get("MlsNumber"),
                    "price": l.get("Property", {}).get("Price"),
                    "address": l.get("Property", {}).get("Address", {}).get("AddressText"),
                    "url": "https://www.realtor.ca" + l.get("RelativeDetailsURL"),
                    "beds": l.get("Building", {}).get("Bedrooms"),
                    "time": l.get("TimeOnRealtor", "New")
                })
            
            with open("data.json", "w") as f:
                json.dump({"last_updated": str(datetime.now()), "listings": cleaned_data}, f, indent=2)
            print(f"Success! Found {len(cleaned_data)} houses.")
        else:
            with open("data.json", "w") as f:
                json.dump({"error": f"Status {response.status_code}", "last_updated": str(datetime.now())}, f)
            print(f"Failed with status: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape()
