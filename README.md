# LinkedIn Job Scraper

This is a Python script that allows you to scrape job listings from LinkedIn. It uses Selenium and BeautifulSoup to interact with the LinkedIn website and extract job data.

## Prerequisites

- Python 3.x
- Selenium library
- BeautifulSoup library
- Chrome browser

## Setup

1. Install the required Python libraries using pip:

`pip install selenium beautifulsoup4`

2. Download the ChromeDriver executable that matches your Chrome browser version and place it in the same directory as the script.

3. Open the script file (linkedin_scraper.py) and modify the following variables:

- session_id: Your LinkedIn session ID. You can obtain this value by logging into LinkedIn in your Chrome browser, opening the developer tools (Ctrl+Shift+I or Cmd+Option+I), and navigating to the Application tab. Under Storage, expand Cookies and copy the value of the li_at cookie.
- jobs_url: The URL of the LinkedIn job search page you want to scrape. You can specify search parameters in the URL.
- search_terms: Optional search terms to narrow down the job search. You can leave this empty if not needed.
- geo_id: Optional geographic ID for location-based job searches. You can leave this empty if not needed.
- chromedriver_path: The path to the ChromeDriver executable if it's not in the same directory.

## Usage

To run the script, execute the following command:

`python linkedin_scraper.py`

The script will start a Chrome browser in headless mode, log in to LinkedIn using your session ID, perform the job search, scrape the job listings, and output the data in the console.

## Output

The script will print a list of dictionaries, where each dictionary represents a job listing. Each job listing contains the following information:

-     title: The job title.
-     url: The URL of the job listing.
-     job_title: The job title (duplicated for convenience).
-     job_company: The company offering the job.
-     job_company_url: The URL of the company's LinkedIn page.
-     salary: The salary information (if available).
-     no_of_applicants: The number of applicants for the job (if available).
-     job_description: The job description.

## Notes

-     This script uses web scraping techniques to extract data from LinkedIn. Make sure to comply with LinkedIn's terms of service and use the script responsibly.
-     The script relies on the Chrome browser and ChromeDriver to interact with the LinkedIn website. Ensure that you have Chrome installed and the ChromeDriver executable compatible with your Chrome version.
-     The script may require adjustments if LinkedIn modifies its website structure.

If you have any questions or encounter any issues, please feel free to ask.
