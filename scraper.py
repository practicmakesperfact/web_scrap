# import requests
# from bs4 import BeautifulSoup

# base_url = "https://www.example.com?page={}"
# for page in range(1, 6):  # Scrape first 5 pages
#     url = base_url.format(page)
#     print(f"Scraping {url}...")
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'lxml')

#     titles = soup.find_all('h2')
#     for title in titles:
#         print(title.get_text(strip=True))

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://quotes.toscrape.com"

while url:
    print("Scraping:", url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    quotes = soup.find_all("span", class_="text")
    for q in quotes:
        print(q.get_text())

    next_btn = soup.find("li", class_="next")

    if next_btn:
        next_link = next_btn.find("a")["href"]
        url = urljoin(url, next_link)
    else:
        url = None
