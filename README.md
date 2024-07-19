# Crazing Dealership Scraper

The Crazing Dealership Scraper is a Python application designed to extract information about car dealerships from the Carzing website. It navigates through the dealership listings, collects data on each dealer, and saves the information in a CSV file for further analysis or use. This tool is particularly useful for individuals or businesses looking to aggregate dealership data across different locations.

## Features

- **Scraping Dealership Data:** Collects comprehensive details about dealerships, including name, location, phone number, distance, inventory count, and inventory URL.
- **Pagination Handling:** Automatically navigates through multiple pages of dealership listings to collect data.
- **Asynchronous Support:** Utilizes asynchronous programming to improve the efficiency of web scraping and data collection.
- **Headless Browser Automation:** Employs Playwright with a headless Firefox browser for seamless navigation and data extraction without a GUI.
- **Session Persistence:** Supports session persistence to avoid re-authentication and to maintain session state across multiple scraping sessions.
- **Concurrent Scraping:** Leverages Python's ThreadPool for concurrent scraping, significantly reducing the total scraping time.

## Installation

Before running the Crazing Dealership Scraper, ensure you have Python 3.6+ installed on your system. Then, follow these steps to set up the project environment:

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Abinet508/crazing-dealership-scraper.git
   ```
2. Navigate to the project directory:
   ```bash
   cd crazing-dealership-scraper
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start scraping dealership data, simply run the `crazing.py` script from the command line:

```bash
python crazing.py
```

The script will automatically navigate through the Carzing website, collect dealership data, and save it to a CSV file named `dealers.csv` in the project directory.

## Output

The output CSV file will contain the following columns:

- DEALER NAME
- LOCATION
- PHONE
- DISTANCE
- INVENTORY
- ZIP
- CITY
- INVENTORY URL
