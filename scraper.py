#scraper

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup
options = Options()
options.add_argument("user-agent=Mozilla/5.0")
options.add_argument("--headless")

# Automatically manage chromedriver version to match Chrome 141
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.baseball-reference.com/postseason/"
driver.get(url)
time.sleep(2)

data = []
rows = driver.find_elements(By.CSS_SELECTOR, "table#all_ws_series tbody tr")

for row in rows:
    try:
        year = row.find_element(By.XPATH, './th').text.strip()
        winner = row.find_element(By.XPATH, './td[1]').text.strip()
        loser = row.find_element(By.XPATH, './td[2]').text.strip()
        result = row.find_element(By.XPATH, './td[3]').text.strip()

        data.append({
            'Year': year,
            'Winner': winner,
            'Loser': loser,
            'Result': result
        })
    except Exception as e:
        print("Error:", e)
        continue

df = pd.DataFrame(data)
df.to_csv("mlb_world_series_history.csv", index=False)
print("✅ Data saved to mlb_world_series_history.csv")

driver.quit()

