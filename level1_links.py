import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://webscraper.io"
url = base_url + "/test-sites/e-commerce/static"

response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

links = []

for a in soup.select("a.title"):
    links.append(urljoin(base_url, a["href"]))

print("Found links:", len(links))
print(links[:5])
