import requests
import json
from datetime import datetime

def scrape():
    url = "https://api37.realtor.ca/Listing.svc/PropertySearch_Post"
    
    # Kamloops bounding box and criteria
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
        "Sort": "6-D", # Newest first
        "RecordsPerPage": "50",
        "CultureId": "1",
        "ApplicationId": "1"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.realtor.ca/"
    }

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        listings = response.json().get("Results", [])
        
        # We only save the essential info to keep the file small
        cleaned_data = []
        for l in listings:
            cleaned_data.append({
                "mls": l.get("MlsNumber"),
                "price": l.get("Property", {}).get("Price"),
                "address": l.get("Property", {}).get("Address", {}).get("AddressText"),
                "url": "https://www.realtor.ca" + l.get("RelativeDetailsURL"),
                "beds": l.get("Building", {}).get("Bedrooms"),
                "time": l.get("TimeOnRealtor", "New") # Realtor provides a relative string like "2 hours ago"
            })
        
        # Save to data.json
        with open("data.json", "w") as f:
            json.dump({"last_updated": str(datetime.now()), "listings": cleaned_data}, f)

if __name__ == "__main__":
    scrape()
