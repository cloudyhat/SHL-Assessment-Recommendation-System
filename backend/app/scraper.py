import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_catalog():
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    cards = soup.select(".product-card")

    data = []
    for card in cards:
        try:
            url = card.find("a")["href"]
            name = card.select_one(".product-card__title").text.strip()
            desc = card.select_one(".product-card__description").text.strip()
            meta = card.select(".product-card__tag")
            test_type = [m.text for m in meta]
            duration = int([m for m in meta if "min" in m.text.lower()][0].text.split()[0])
            remote = "Yes" if any("remote" in m.text.lower() for m in meta) else "No"
            adaptive = "Yes" if any("adaptive" in m.text.lower() for m in meta) else "No"

            data.append({
                "url": url,
                "assessment_name": name,
                "description": desc,
                "test_type": test_type,
                "duration": duration,
                "remote_support": remote,
                "adaptive_support": adaptive
            })
        except Exception as e:
            print(f"Error parsing card: {e}")
            continue

    with open("backend/data/shl_catalog.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    scrape_catalog()

# scrape_shl_catalog.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_shl_catalog(url="https://www.shl.com/solutions/products/product-catalog/"):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    cards = soup.select(".product-tile__wrapper")
    data = []

    for card in cards:
        name_tag = card.select_one(".product-tile__heading")
        desc = card.select_one(".product-tile__description")
        link = card.find("a")["href"]

        meta = card.select(".product-tile__meta .product-tile__meta-item")

        remote = "Yes" if "Remote" in str(meta) else "No"
        adaptive = "Yes" if "Adaptive" in str(meta) or "IRT" in str(meta) else "No"
        duration = next((m.text for m in meta if "min" in m.text), "Unknown")
        test_type = next((m.text for m in meta if "Test" in m.text), "Unknown")

        data.append({
            "name": name_tag.text.strip() if name_tag else "Unnamed",
            "description": desc.text.strip() if desc else "",
            "url": "https://www.shl.com" + link,
            "remote": remote,
            "adaptive": adaptive,
            "duration": duration,
            "test_type": test_type,
        })

    return pd.DataFrame(data)

# Save to CSV or JSON for later
df = scrape_shl_catalog()
df.to_csv("shl_assessments.csv", index=False)