#scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time

def scrape_mlb_world_series():
    # Setup Selenium WebDriver with options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://www.baseball-reference.com/postseason/"
    driver.get(url)

    # Wait for the table or page content to load
    try:
        # Adjust wait selector to actual table or container present on the page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )
    except Exception as e:
        print(f"❌ Timeout or error waiting for page content: {e}")
        driver.quit()
        return

    # Grab page source after content load
    html = driver.page_source
    driver.quit()

    # Parse tables from the loaded HTML
    try:
        tables = pd.read_html(html)
    except Exception as e:
        print(f"❌ Failed to parse tables: {e}")
        return

    # Inspect tables to find the one with World Series data
    # Print summary to identify correct table
    for i, table in enumerate(tables):
        print(f"Table {i}: shape={table.shape}")
        print(table.head(3))
        print()

    # For example, pick the right table by inspecting output manually
    # Here, assuming table 0 is World Series history
    ws_df = tables[0]

    if ws_df.empty:
        print("⚠️ No World Series data found.")
        return

    # Clean columns: strip spaces, replace spaces with underscores
    ws_df.columns = [col.strip().replace(' ', '_') for col in ws_df.columns]

    # Save to CSV
    ws_df.to_csv("mlb_world_series_history.csv", index=False)
    print("✅ Saved World Series history to mlb_world_series_history.csv")

if __name__ == "__main__":
    scrape_mlb_world_series()
