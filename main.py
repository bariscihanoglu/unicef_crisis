import logging
from datetime import datetime
from typing import List, Dict
from urllib.parse import urlencode
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import csv


from location_codes import LOCATION_CODES_DICT

# Configuration constants
BASE_URL = 'https://www.crisisgroup.org/crisiswatch/database'
COUNTRY_NAMES = ['Benin', 'Rwanda', 'China', 'Egypt']
LOCATION_CODES = [LOCATION_CODES_DICT[country] for country in COUNTRY_NAMES]
DATE_RANGE = '-3 months'  # Website's temporal filter
DESIRED_MONTHS = {10, 11, 12}  # October, November, December - Optional
DESIRED_YEAR = 2024
OUTPUT_FILE = 'crisis_data.csv'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def configure_driver() -> uc.Chrome:
    """Configure headless Chrome driver with anti-detection measures."""
    options = uc.ChromeOptions()
    options.add_argument(f"--user-agent={USER_AGENT}")
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return uc.Chrome(options=options)

def construct_url(page: int) -> str:
    """Construct URL with query parameters including pagination."""
    params = {
        'location[]': LOCATION_CODES,
        'created': DATE_RANGE,
        'page': page
    }
    return f"{BASE_URL}?{urlencode(params, doseq=True)}"

def extract_entry_data(entry) -> Dict[str, str]:
    """Extract and clean data from a single entry element."""
    country = entry.find('h3').get_text(strip=True) if entry.find('h3') else 'N/A'
    
    time_element = entry.find('time')
    month_year = time_element.get_text(strip=True) if time_element else 'N/A'
    
    details = entry.find('div', class_='o-crisis-states__detail')
    title = details.find('strong').get_text(strip=True) if details.find('strong') else 'N/A'
    content = ' '.join(details.get_text(separator=' ', strip=True).replace(title, '').split())
    
    return {
        'Country': country,
        'MonthYear': month_year,
        'Title': title,
        'Content': content
    }

def filter_by_date(entries: List[Dict]) -> List[Dict]:
    """Filter entries to include only specified months and year."""
    filtered = []
    for entry in entries:
        try:
            dt = datetime.strptime(entry['MonthYear'], '%B %Y')
            if dt.year == DESIRED_YEAR and dt.month in DESIRED_MONTHS:
                filtered.append(entry)
        except (ValueError, KeyError):
            logging.warning(f"Invalid date format for entry: {entry.get('MonthYear')}")
    return filtered

def main():
    """Main execution flow with pagination support."""
    driver = configure_driver()
    extracted_data = []
    
    try:
        page = 0
        while True:
            url = construct_url(page)
            logging.info(f"Fetching page {page}: {url}")
            
            driver.get(url)
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "c-crisiswatch-entry"))
                )
            except TimeoutException:
                logging.info(f"No entries found on page {page}, stopping pagination.")
                break
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            entries = soup.find_all('div', class_='c-crisiswatch-entry')
            
            if not entries:
                logging.info(f"No entries found on page {page}, stopping pagination.")
                break
            
            page_data = [extract_entry_data(entry) for entry in entries]
            extracted_data.extend(page_data)
            logging.info(f"Extracted {len(page_data)} entries from page {page}")
            page += 1

        # Apply date filtering
        filtered_data = filter_by_date(extracted_data)
        logging.info(f"Total {len(filtered_data)} valid entries after filtering")

        # Save results
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            if filtered_data:
                writer = csv.DictWriter(f, fieldnames=filtered_data[0].keys())
                writer.writeheader()
                writer.writerows(filtered_data)
            else:
                logging.warning("No data to write to CSV")
            logging.info(f"Data successfully saved to {OUTPUT_FILE}")

    except Exception as e:
        logging.error(f"Execution failed: {str(e)}")
    finally:
        driver.quit()
        logging.info("Driver has been quit.")

if __name__ == "__main__":
    main()
