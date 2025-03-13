import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set!")

client = MongoClient(MONGO_URI)
db = client.paintball
collection = db.prices

# URLs to track (example placeholders)
URLS = {
    "CTRL 2": "https://www.bunkerkings.com/products/bunkerkings-ctrl2-loader-black",
    "Spire V": "https://virtuepb.com/products/virtue-spire-v-loader-black",
    "Sprie V": "https://www.lonewolfpaintball.com/products/virtue-spire-v?variant=41869081509941"
}

def scrape_price(url):
    """Scrapes the price from a given URL, handling variant-specific pricing."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching {url}: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Attempt to find price for specific variant from embedded JSON
    script_tag = soup.find("script", string=lambda s: s and "var meta" in s)
    if script_tag:
        try:
            script_content = script_tag.string
            json_text = script_content.split("var meta = ", 1)[1].split(";", 1)[0].strip()
            product_data = json.loads(json_text)
            variant_id = url.split("variant=")[-1]  # Extract variant ID from URL
            
            for variant in product_data.get("product", {}).get("variants", []):
                if str(variant.get("id")) == variant_id:
                    return str(variant.get("price", 0) / 100)  # Convert cents to dollars
        except (IndexError, KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing variant data: {e}")

    # Fallback search using meta tag
    price_tag = soup.find("meta", {"property": "og:price:amount"})
    if price_tag:
        return price_tag.get("content", "").strip()

    # Debug output if price is not found
    snippet = soup.prettify()[:200]
    print(f"Price not found on {url}. HTML snippet: {snippet}")
    return None

def store_price(product_name, price, url):
    """Stores scraped prices in MongoDB, ensuring only one entry per product per day per URL."""
    if price:
        today = datetime.datetime.utcnow().date()
        start_of_day = datetime.datetime(today.year, today.month, today.day)
        end_of_day = start_of_day + datetime.timedelta(days=1)

        existing_entry = collection.find_one({
            "product": product_name,
            "url": url,
            "date": {"$gte": start_of_day, "$lt": end_of_day}
        })

        if existing_entry:
            if existing_entry["price"] == price:
                print(f"Price for {product_name} from {url} remains the same. Skipping update.")
                return
            else:
                collection.update_one(
                    {"_id": existing_entry["_id"]},
                    {"$set": {"price": price, "date": datetime.datetime.utcnow()}}
                )
                print(f"Updated: {product_name} - {price} from {url}")
                return
        
        collection.insert_one({
            "product": product_name,
            "price": price,
            "url": url,
            "date": datetime.datetime.utcnow()
        })
        print(f"Stored: {product_name} - {price} from {url}")

def main():
    for product, url in URLS.items():
        price = scrape_price(url)
        if price:
            store_price(product, price, url)

def lambda_handler(event, context):
    """AWS Lambda entry point."""
    main()
    return {"statusCode": 200, "body": "Price check complete"}

if __name__ == "__main__":
    main()
