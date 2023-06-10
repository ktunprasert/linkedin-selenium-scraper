import time
import logging
from selenium import webdriver
from bs4 import BeautifulSoup


class LinkedInScraper:
    def __init__(
        self,
        session_id,
        jobs_url,
        search_terms,
        geo_id,
        chromedriver_path="./chromedriver",
    ):
        self.session_id = session_id
        self.jobs_url = jobs_url
        self.search_terms = search_terms
        self.geo_id = geo_id
        self.driver = None
        self.logger = logging.getLogger(__name__)
        # self.chromedriver_path = chromedriver_path

    def start_driver(self):
        print("Starting driver...")
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--window-size=1080,3840")
        self.driver = webdriver.Chrome(
            # service=Service(executable_path=self.chromedriver_path),
            options=options,
        )

    def login(self):
        print("Logging in...")
        self.driver.get("https://www.linkedin.com/login")
        self.driver.add_cookie({"name": "li_at", "value": self.session_id})
        self.driver.refresh()

    def search_jobs(self):
        print("Searching for jobs...")
        self.driver.get(self.jobs_url)
        time.sleep(3)

    def scrape_jobs(self):
        print("Scraping job listings...")
        with open("page_source.html", "w") as f:
            f.write(self.driver.page_source)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        job_listings = soup.find_all("li", {"class": "jobs-search-results__list-item"})

        print("Found " + len(job_listings) + " jobs")
        jobs = []
        for job in job_listings:
            try:
                job_title = job.find(
                    "a", {"class": "job-card-list__title"}
                ).text.strip()
                job_link = job.find("a", {"class": "job-card-list__title"}).get("href")
                job_link = str(job_link).split("?")[0]
                job_data = self.scrape_job_details(job_link)
            except Exception as e:
                print("Error scraping job details: " + e.__str__())
                continue
            jobs.append(
                {
                    "title": job_title,
                    **job_data
                }
            )
        return jobs

    def scrape_job_details(self, job_url) -> dict:
        print("Scraping job details for " + job_url)
        self.driver.get(f"https://linkedin.com{job_url}")
        time.sleep(1)
        with open("job_source.html", "w") as f:
            f.write(self.driver.page_source)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        job_title = soup.find(
            "h1", {"class": "jobs-unified-top-card__job-title"}
        ).text.strip()

        company_element = soup.find(
            "a", {"class": "jobs-unified-top-card__company-name"}
        )

        job_company = company_element.text.strip() if company_element else ""
        job_company_url = company_element.get("href") if company_element else ""
        salary_element = soup.find(
            "a", {"href": "#SALARY"}
        )
        salary = salary_element.text.strip() if salary_element else ""
        job_level = salary_element.find_next_sibling("span").text.strip()
        job_description = soup.find(
            "div", {"id": "job-details"}
        ).find("span").text.strip()

        job_data = {
            "job_title": job_title,
            "job_company": job_company,
            "job_company_url": job_company_url,
            "salary": salary,
            "job_level": job_level,
            "job_description": job_description,
        }

        return job_data

    def run(self):
        try:
            self.start_driver()
            self.login()
            self.search_jobs()
            jobs = self.scrape_jobs()
            return jobs
        except Exception as e:
            self.logger.error(f"Error scraping LinkedIn job listings: {e}")
        finally:
            if self.driver:
                self.driver.quit()
