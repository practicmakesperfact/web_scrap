import requests
from bs4 import BeautifulSoup

base_url = "https://www.example.com?page={}"
for page in range(1, 6):  # Scrape first 5 pages
    url = base_url.format(page)
    print(f"Scraping {url}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    titles = soup.find_all('h2')
    for title in titles:
        print(title.get_text(strip=True))
