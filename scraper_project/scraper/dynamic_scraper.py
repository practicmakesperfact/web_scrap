from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from scraper.base import BaseScraper

class DynamicScraper(BaseScraper):
    def scrape(self):
        data = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.config["base_url"], timeout=60000)
            page.wait_for_timeout(3000)

            soup = BeautifulSoup(page.content(), "html.parser")

            for card in soup.select(self.config["program_card"]):
                item = {}
                for field, selector in self.config["fields"].items():
                    item[field] = self.extract_text(card, selector)
                data.append(item)

            browser.close()
        return data
