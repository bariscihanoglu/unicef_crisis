CrisisWatch Data Scraper
A Python script to scrape and filter crisis data from the CrisisGroup website, with built-in pagination support and date filtering.

Features
Pagination Handling: Automatically navigates through all available pages

Date Filtering: Filters results by specified months and year

Headless Browsing: Uses undetected ChromeDriver to avoid bot detection

Logging: Detailed logging for monitoring and debugging

CSV Export: Saves filtered results in structured CSV format

Prerequisites
Python 3.9+

Chrome browser installed

ChromeDriver compatible with your Chrome version

Installation
Clone the repository

Install required packages:

bash
Copy
pip install -r requirements.txt
Configuration
Create location_codes.py with country-code mappings:

python
Copy
LOCATION_CODES_DICT = {
    'Benin': 'BEN',
    'Rwanda': 'RWA',
    'China': 'CHN',
    'Egypt': 'EGY',
    # Add more countries as needed
}
Modify constants in the script as needed:

python
Copy
COUNTRY_NAMES = ['Benin', 'Rwanda', 'China', 'Egypt']  # Countries to monitor
DESIRED_MONTHS = {10, 11, 12}  # October-December
DESIRED_YEAR = 2024
DATE_RANGE = '-3 months'  # Website's temporal filter
Usage
Run the script:

bash
Copy
python crisis_scraper.py
The script will:

Launch headless Chrome browser

Scrape data from multiple pages

Filter results by specified dates

Save output to crisis_data.csv

Output Example (crisis_data_example.csv)
csv
Copy
Country,MonthYear,Title,Content
Benin,December 2023,Political tensions rise,Opposition parties continue to protest...
Rwanda,November 2023,Border dispute escalates,Rwandan and Congolese forces clashed...
China,October 2023,Taiwan Strait incident,Chinese jets entered Taiwan's ADIZ...
Notes
Website structure changes may require CSS selector updates

Adjust DATE_RANGE for different temporal filters

Modify DESIRED_MONTHS/DESIRED_YEAR for different date filters

Set DESIRED_MONTHS = None to disable month filtering

Troubleshooting
Dependency Issues:

Verify Chrome and ChromeDriver versions match

Run pip freeze to check package versions

Location Codes:

Ensure country names match keys in LOCATION_CODES_DICT

Confirm codes match website's internal codes

Website Changes:

Check CSS selectors if scraping fails

Verify pagination structure remains unchanged

Blocking Issues:

Add random delays between requests

Consider proxy rotation

Disable headless mode for debugging:

python
Copy
options.add_argument("--headless=new")  # Remove this line
License
MIT License - See included LICENSE file

Important: Use this script responsibly and in compliance with the target website's terms of service. Consider adding rate limiting and respecting robots.txt in production use.
