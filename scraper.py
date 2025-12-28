import requests
import json
from datetime import datetime

def scrape():
    url = "https://api37.realtor.ca/Listing.svc/PropertySearch_Post"
    
    # This payload is more specific to what Realtor.ca expects
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

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.realtor.ca/",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    # Use a session to keep cookies
    session = requests.Session()
    
    try:
        # First, visit the homepage to get a session cookie
        session.get("https://www.realtor.ca", headers=headers, timeout=10)
        
        # Now make the actual POST request
        response = session.post(url, data=payload, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            listings = data.get("Results", [])
            print(f"Found {len(listings)} listings.")
            
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
        else:
            print(f"Error: Received status {response.status_code}")
            # If it fails, save the error so we can see it in data.json
            with open("data.json", "w") as f:
                json.dump({"error": f"Status {response.status_code}", "last_updated": str(datetime.now())}, f)

    except Exception as e:
        print(f"Script crashed: {e}")

if __name__ == "__main__":
    scrape()
