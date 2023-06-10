import re
from datetime import datetime

def extract_salary(salary_text):
    """
    Extracts the salary information from the job listing text.
    Returns a tuple containing the minimum and maximum salary values.
    """
    salary_text = salary_text.lower()
    if "salary undisclosed" in salary_text:
        return None, None
    elif "to" in salary_text:
        # Extract range of salaries
        match = re.search(r"\$?(\d{1,3}(?:,\d{3})*)(?:\.\d{2})?\s?to\s?\$?(\d{1,3}(?:,\d{3})*)(?:\.\d{2})?", salary_text)
        if match:
            min_salary = int(match.group(1).replace(",", ""))
            max_salary = int(match.group(2).replace(",", ""))
            return min_salary, max_salary
    else:
        # Extract single salary value
        match = re.search(r"\$?(\d{1,3}(?:,\d{3})*)(?:\.\d{2})?", salary_text)
        if match:
            salary = int(match.group(1).replace(",", ""))
            return salary, salary
    return None, None

def extract_posted_date(posted_text):
    """
    Extracts the date the job listing was posted.
    Returns a datetime object representing the date.
    """
    posted_text = posted_text.lower()
    if "just now" in posted_text:
        return datetime.now()
    elif "today" in posted_text:
        match = re.search(r"today, (\d{1,2}):(\d{2})\s?(am|pm)?", posted_text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            if match.group(3) == "pm" and hour != 12:
                hour += 12
            return datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
    elif "yesterday" in posted_text:
        match = re.search(r"yesterday, (\d{1,2}):(\d{2})\s?(am|pm)?", posted_text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            if match.group(3) == "pm" and hour != 12:
                hour += 12
            return datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0) - timedelta(days=1)
    else:
        match = re.search(r"(\d{1,2})?(\+)?\s?(?:day|week|month|year)s?\s?ago", posted_text)
        if match:
            num = int(match.group(1)) if match.group(1) else 1
            if match.group(2):
                return datetime.now() - timedelta(days=num)
            else:
                return datetime.now() - timedelta(weeks=num)
    return None

def extract_location(location_text):
    """
    Extracts the location information from the job listing text.
    Returns a string representing the location.
    """
    location_text = location_text.lower()
    if "remote" in location_text:
        return "Remote"
    elif "united states" in location_text:
        match = re.search(r"([a-zA-Z\s]+),\s?(us)?", location_text)
        if match:
            return match.group(1)
    else:
        match = re.search(r"([a-zA-Z\s]+),\s?([a-zA-Z]{2})", location_text)
        if match:
            return match.group(1) + ", " + match.group(2).upper()
    return None

def extract_num_applicants(applicants_text):
    """
    Extracts the number of applicants for the job listing.
    Returns an integer representing the number of applicants.
    """
    applicants_text = applicants_text.lower()
    match = re.search(r"(\d+)\+?\s?applicant", applicants_text)
    if match:
        return int(match.group(1).replace(",", ""))
    return None

def extract_job_summary(summary_text):
    """
    Extracts the job summary from the job listing text.
    Returns a string representing the job summary.
    """
    return summary_text.strip()

def extract_job_link(link_element):
    """
    Extracts the link to the job listing from the HTML element.
    Returns a string representing the job link.
    """
