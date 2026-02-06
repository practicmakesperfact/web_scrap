import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import time

base_url = "https://quotes.toscrape.com"
url = base_url

quotes_data = []

while url:
    print("Scraping:", url)

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "lxml")

    quotes = soup.find_all("div", class_="quote")

    for q in quotes:
        text = q.find("span", class_="text").get_text(strip=True)
        author = q.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in q.find_all("a", class_="tag")]

        quotes_data.append({
            "quote": text,
            "author": author,
            "tags": ", ".join(tags)
        })

    next_btn = soup.find("li", class_="next")
    url = urljoin(base_url, next_btn.a["href"]) if next_btn else None

    time.sleep(1)  # be polite

print("Total quotes scraped:", len(quotes_data))
with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["quote", "author", "tags"]
    )
    writer.writeheader()
    writer.writerows(quotes_data)

print("Saved to quotes.csv")

