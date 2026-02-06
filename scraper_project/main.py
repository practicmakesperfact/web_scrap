import yaml
import pandas as pd
from scraper.static_scraper import StaticScraper
from scraper.dynamic_scraper import DynamicScraper
from config.mappings import normalize_age

all_data = []

with open("config/sites.yaml") as f:
    sites = yaml.safe_load(f)

for site_name, config in sites.items():
    scraper = (
        DynamicScraper(config)
        if config["type"] == "dynamic"
        else StaticScraper(config)
    )

    records = scraper.scrape()

    for r in records:
        r["age"] = normalize_age(r.get("age"))
        r["source"] = site_name

    all_data.extend(records)

df = pd.DataFrame(all_data)

# Match Google Sheet column order
df = df.rename(columns={
    "program_name": "Program Name",
    "sport": "Sport",
    "age": "Age Group",
    "location": "Location",
    "dates": "Dates",
    "link": "URL"
})

df.to_excel("output/data.xlsx", index=False)
print("✅ Scraping completed")
