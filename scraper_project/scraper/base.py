class BaseScraper:
    def __init__(self, config):
        self.config = config

    def extract_text(self, element, selector):
        if "@href" in selector:
            return element.select_one(selector.replace("@href", "")).get("href", "")
        el = element.select_one(selector)
        return el.get_text(strip=True) if el else ""
