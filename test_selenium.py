from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://quotes.toscrape.com/js/")
time.sleep(3)

while True:
    soup = BeautifulSoup(driver.page_source, "lxml")

    quotes = soup.find_all("div", class_="quote")
    for q in quotes:
        print(q.find("small", class_="author").text)

    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "li.next a")
        next_btn.click()
        time.sleep(2)
    except:
        print("No more pages")
        break

input("Press ENTER to close browser...")
driver.quit()
