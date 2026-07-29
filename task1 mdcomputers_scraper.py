import sys
import csv
import requests
from bs4 import BeautifulSoup

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "external harddrive"
    
    url = "https://mdcomputers.in/index.php"
    params = {
        "route": "product/search",
        "search": query
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    print(f"Searching MDComputers for: {query}")
    res = requests.get(url, params=params, headers=headers)
    
    if res.status_code != 200:
        print(f"Failed to load page, status code: {res.status_code}")
        return

    soup = BeautifulSoup(res.text, "html.parser")
    products = soup.find_all("div", class_="product-thumb")

    results = []
    for p in products:
        title_tag = p.find("h4")
        if not title_tag or not title_tag.find("a"):
            continue
            
        name = title_tag.find("a").text.strip()
        link = title_tag.find("a")["href"]

        price_tag = p.find("span", class_="price-new") or p.find("span", class_="price")
        price = price_tag.text.strip() if price_tag else "N/A"

        old_price_tag = p.find("span", class_="price-old")
        old_price = old_price_tag.text.strip() if old_price_tag else ""

        img_tag = p.find("img")
        img_url = img_tag.get("src", "") if img_tag else ""

        results.append({
            "Name": name,
            "Price": price,
            "Original Price": old_price,
            "Link": link,
            "Image URL": img_url
        })

    print(f"Found {len(results)} items. Saving to CSV...")

    with open("md_products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Price", "Original Price", "Link", "Image URL"])
        writer.writeheader()
        writer.writerows(results)

    print("Saved to md_products.csv")

if __name__ == "__main__":
    main()
