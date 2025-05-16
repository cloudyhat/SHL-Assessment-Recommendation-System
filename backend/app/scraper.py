import requests
from bs4 import BeautifulSoup
import json
## I tried to scrape the SHL product catalog page to get the list of assessments and their details.
## But the page is not structured in a way that allows for easy scraping. The data is loaded dynamically via JavaScript, which makes it difficult to extract using traditional scraping methods. 
## However, I can provide you with a sample code that demonstrates how to scrape a static page. You may need to use a headless browser or an API if available for dynamic content.
def scrape_shl_catalog():
    url = "https://www.shl.com/solutions/products/product-catalog/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    catalog_data = []

    for card in soup.find_all("div", class_="c-card"):
        title = card.find("h3")
        link = card.find("a", href=True)
        description = card.find("p")
        
        if title and link:
            catalog_data.append({
                "title": title.get_text(strip=True),
                "url": "https://www.shl.com" + link["href"],
                "description": description.get_text(strip=True) if description else ""
            })

    with open("shl_catalog.json", "w") as f:
        json.dump(catalog_data, f, indent=2)

if __name__ == "__main__":
    scrape_shl_catalog()