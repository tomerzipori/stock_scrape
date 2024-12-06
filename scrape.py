import os
import csv
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
log_file_path = os.path.expanduser("~/scrape_errors.log")  # Save in the home directory
logging.basicConfig(
    filename=log_file_path,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set up EdgeDriver
edge_options = Options()
edge_options.add_argument('--headless')  # Optional: Run in headless mode
edge_options.add_argument('--disable-gpu')
edge_options.add_argument('--no-sandbox')

# Path to your EdgeDriver executable
edge_driver_path = "C:/Users/Tomer/Documents/GitHub/stock_scrape/msedgedriver.exe"

service = Service(edge_driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

dict_urls = {
    "1159250": ("https://market.tase.co.il/he/market_data/security/1159250/major_data", '//*[@id="mainContent"]/security-lobby/security-major/section[1]/div/div[1]/div/div[1]/div/ul/li[2]/div[1]/div[2]/b'),
    "1159094": ("https://market.tase.co.il/he/market_data/security/1159094/major_data", '//*[@id="mainContent"]/security-lobby/security-major/section[1]/div/div[1]/div/div[1]/div/ul/li[2]/div[1]/div[2]/b'),
    "1159169": ("https://market.tase.co.il/he/market_data/security/1159169/major_data", '//*[@id="mainContent"]/security-lobby/security-major/section[1]/div/div[1]/div/div[1]/div/ul/li[2]/div[1]/div[2]/b'),
    "1143783": ("https://market.tase.co.il/he/market_data/security/1143783/major_data", '//*[@id="mainContent"]/security-lobby/security-major/section[1]/div/div[1]/div/div[1]/div/ul/li[2]/div[1]/div[2]/b'),
    "5117379": ("https://maya.tase.co.il/fund/5117379", '//*[@id="wrapper"]/div[3]/div/div[2]/div/div/div/div[2]/div[1]/div/div[4]'),
    "5113444": ("https://maya.tase.co.il/fund/5113444", '//*[@id="wrapper"]/div[3]/div/div[2]/div/div/div/div[2]/div[1]/div/div[4]')
}

prices = {}

try:
    for key, url in dict_urls.items():
        try:
            # Navigate to the webpage
            driver.get(url[0])

            # Use explicit wait to locate the element
            xpath = url[1]
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )

            # Extract the text
            data = element.text
            prices[key] = data
            print(f"{key} Price:", data)

        except Exception as e:
            error_message = f"Error scraping {key}: {e}"
            print(error_message)
            logging.error(error_message)

finally:
    # Close the WebDriver
    driver.quit()

# Save prices to a CSV file
output_file = "prices.csv"
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
    logging.error(error_message)
