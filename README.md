# CrisisWatch Data Scraper
A Python script to scrape and filter crisis data from the CrisisGroup website, with built-in pagination support and date filtering.

## Features
Pagination Handling: Automatically navigates through all available pages

Date Filtering: Filters results by specified months and year

Headless Browsing: Uses undetected ChromeDriver to avoid bot detection

Logging: Detailed logging for monitoring and debugging

CSV Export: Saves filtered results in structured CSV format

## Prerequisites
Python 3.9+

Chrome browser installed

ChromeDriver compatible with your Chrome version

## Installation
1.Clone the repository

2.Install required packages:

`pip install -r requirements.txt`

## Configuration
Modify constants in the script as needed:
```
COUNTRY_NAMES = ['Benin', 'Rwanda', 'China', 'Egypt']  # Countries to monitor
DESIRED_MONTHS = {10, 11, 12}  # October-December
DESIRED_YEAR = 2024
DATE_RANGE = '-3 months'  # Website's temporal filter
```

Usage
Run the script:

`python crisis_scraper.py`

The script will:

1. Launch headless Chrome browser

2. Scrape data from multiple pages

3. Filter results by specified dates

4. Save output to crisis_data.csv

## Output Example (crisis_data_example.csv)
Country,MonthYear,Title,Content
Benin,December 2023,Political tensions rise,Opposition parties continue to protest...
Rwanda,November 2023,Border dispute escalates,Rwandan and Congolese forces clashed...
China,October 2023,Taiwan Strait incident,Chinese jets entered Taiwan's ADIZ...

## Notes
Website structure changes may require CSS selector updates

Adjust DATE_RANGE for different temporal filters

Modify DESIRED_MONTHS/DESIRED_YEAR for different date filters

## Troubleshooting
Dependency Issues:

Verify Chrome and ChromeDriver versions match

Run pip freeze to check package versions

Website Changes:

Check CSS selectors if scraping fails

Verify pagination structure remains unchanged

Blocking Issues:

Add random delays between requests

Consider proxy rotation
