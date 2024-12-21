import os
import sys
import csv
import logging
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Configure logging
log_file_path = "/app/process_log.txt"  # Adjusted for container
logging.basicConfig(
    filename=log_file_path,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set up ChromeDriver
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Path to the ChromeDriver executable in the container
chrome_driver_path = "/usr/bin/chromedriver"

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Dictionary of stock URLs and their price XPaths
dict_urls = {
    "1159250": ("https://market.tase.co.il/he/market_data/security/1159250/major_data",
                '//*[@id="mainContent"]/security-lobby/security-major/section[1]/div/div[1]/div/div[1]/div/ul/li[2]/div[1]/div[2]/b'),
    "1159094": ("https://market.tase.co.il/he/market_data/security/1159094/major_data",
                '//*[@id="mainContent"]/security-lobby/security-major/section[1]/div/div[1]/div/div[1]/div/ul/li[2]/div[1]/div[2]/b'),
    "1159169": ("https://market.tase.co.il/he/market_data/security/1159169/major_data",
                '//*[@id="mainContent"]/security-lobby/security-major/section[1]/div/div[1]/div/div[1]/div/ul/li[2]/div[1]/div[2]/b'),
    "1143783": ("https://market.tase.co.il/he/market_data/security/1143783/major_data",
                '//*[@id="mainContent"]/security-lobby/security-major/section[1]/div/div[1]/div/div[1]/div/ul/li[2]/div[1]/div[2]/b'),
    "5117379": ("https://maya.tase.co.il/fund/5117379",
                '//*[@id="wrapper"]/div[3]/div/div[2]/div/div/div/div[2]/div[1]/div/div[4]'),
    "5113444": (
        "https://maya.tase.co.il/fund/5113444", '//*[@id="wrapper"]/div[3]/div/div[2]/div/div/div/div[2]/div[1]/div/div[4]')
}

# Output dictionary in {stock_number: stock_price} format
prices = {}

try:
    for key, url in dict_urls.items():
        try:
            # Navigate to the webpage
            driver.get(url[0])

            # Use explicit wait to locate the element
            xpath = url[1]
            element = WebDriverWait(driver, 120).until(
                ec.presence_of_element_located((By.XPATH, xpath))
            )

            # Extract the text
            prices[key] = element.text
            print(f"{key} Price:", element.text)

        except Exception as e:
            error_message = f"Error scraping {key}: {e}"
            print(error_message)
            logging.error(error_message, exc_info=True)

finally:
    # Close the WebDriver
    driver.quit()

prices = {
    key: (match.group(0) if isinstance(value, str) and (match := re.search(r'[\d.,]+', value)) else None)
    for key, value in prices.items()
}

# Save prices to a CSV file
output_file = "/app/prices.csv"  # Adjusted for container
try:
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["Index", "Price"])
        # Write the data
        for key, value in prices.items():
            writer.writerow([key, value])
    print(f"Prices saved to {output_file}.")
except Exception as e:
    error_message = f"Error saving prices to CSV file: {e}"
    print(error_message)
    logging.error(error_message, exc_info=True)

sys.exit(0)
