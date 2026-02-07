from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://quotes.toscrape.com/js/")

time.sleep(3)

data = []

while True:
    soup = BeautifulSoup(driver.page_source, "lxml")

    quotes = soup.find_all("div", class_="quote")
    for q in quotes:
        text = q.find("span", class_="text").get_text(strip=True)
        author = q.find("small", class_="author").get_text(strip=True)

        data.append({
            "quote": text,
            "author": author
        })

    try:
        next_btn = driver.find_element("css selector", "li.next a")
        next_btn.click()
        time.sleep(2)
    except:
        break


print("Scraping finished.")

input("Press ENTER to close browser...")
driver.quit()


with open("selenium_quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["quote", "author"])
    writer.writeheader()
    writer.writerows(data)

print("Saved selenium_quotes.csv")
