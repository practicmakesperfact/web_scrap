import requests
from bs4 import BeautifulSoup
from scraper.base import BaseScraper

class StaticScraper(BaseScraper):
    def scrape(self):
        r = requests.get(self.config["base_url"], timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        data = []
        for card in soup.select(self.config["program_card"]):
            item = {}
            for field, selector in self.config["fields"].items():
                item[field] = self.extract_text(card, selector)
            data.append(item)
        return data
