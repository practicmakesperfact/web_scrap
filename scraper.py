import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import time

BASE_URL = "https://quotes.toscrape.com"
url = BASE_URL
quotes_data = []

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_author_details(author_url):
    print(f"   ↳ Fetching author page: {author_url}")
    response = requests.get(author_url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    born_date = soup.find("span", class_="author-born-date")
    born_location = soup.find("span", class_="author-born-location")
    description = soup.find("div", class_="author-description")

    return (
        born_date.get_text(strip=True) if born_date else "",
        born_location.get_text(strip=True) if born_location else "",
        description.get_text(strip=True) if description else ""
    )

author_cache = {}

page = 1

while url:
    print(f"\n📄 Scraping page {page}: {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    quotes = soup.find_all("div", class_="quote")

    for q in quotes:
        text = q.find("span", class_="text").get_text(strip=True)
        author = q.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in q.find_all("a", class_="tag")]

        about_link = q.find("a", string="(about)")
        if not about_link:
            continue

        author_url = urljoin(BASE_URL, about_link["href"])

        if author_url not in author_cache:
            author_cache[author_url] = scrape_author_details(author_url)
            time.sleep(0.3)

        born_date, born_location, description = author_cache[author_url]

        quotes_data.append({
            "quote": text,
            "author": author,
            "tags": ", ".join(tags),
            "born_date": born_date,
            "born_location": born_location,
            "author_description": description
        })

        print(f"   ✓ Quote by {author}")

    next_btn = soup.find("li", class_="next")
    url = urljoin(BASE_URL, next_btn.a["href"]) if next_btn else None
    page += 1

# Save CSV
with open("quotes_with_authors.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "quote",
            "author",
            "tags",
            "born_date",
            "born_location",
            "author_description"
        ]
    )
    writer.writeheader()
    writer.writerows(quotes_data)

print("\n✅ DONE! Saved to quotes_with_authors.csv")
print(f"📦 Total quotes scraped: {len(quotes_data)}")
