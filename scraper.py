import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import time

base_url = "https://quotes.toscrape.com"
url = base_url
quotes_data = []

def scrape_author_details(author_url):
    response = requests.get(author_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "lxml")

    born_date = soup.find("span", class_="author-born-date").get_text(strip=True)
    born_location = soup.find("span", class_="author-born-location").get_text(strip=True)
    description = soup.find("div", class_="author-description").get_text(strip=True)

    return born_date, born_location, description
author_cache = {}

while url:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "lxml")

    quotes = soup.find_all("div", class_="quote")

    for q in quotes:
        text = q.find("span", class_="text").get_text(strip=True)
        author = q.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in q.find_all("a", class_="tag")]

        author_link = q.find("a")["href"]
        author_url = urljoin(base_url, author_link)

        if author_url not in author_cache:
            author_cache[author_url] = scrape_author_details(author_url)
            time.sleep(0.5)

        born_date, born_location, description = author_cache[author_url]

        quotes_data.append({
            "quote": text,
            "author": author,
            "tags": ", ".join(tags),
            "born_date": born_date,
            "born_location": born_location,
            "author_description": description
        })

    next_btn = soup.find("li", class_="next")
    url = urljoin(base_url, next_btn.a["href"]) if next_btn else None

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
