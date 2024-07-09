import pandas as pd
# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
# from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time
from dateparser import parse
import math
import re

BASE_URL = "https://hk.jobsdb.com"
job = ""
job_combined = ""
job_ids = []
total_jobs_count = ""
last_avail_page = 0

driver = webdriver.Chrome()
page = None
html = None

def load_DOM():
    global html
    page = driver.page_source
    html = bs(page, "html.parser")

def get_page_contents(cur_page):
    pagination = "?page=" + str(cur_page)
    url = BASE_URL + "/" + job_combined + "-jobs/full-time" + (pagination if cur_page > 1 else "")

    # Get HTML Content
    # page = requests.get(url)
    driver.get(url)
    load_DOM()
    # html = list(soup.children)[2]
    # print(html.prettify())

    # Get job postings and their details
    search_results = html.select_one('div[data-automation="searchResults"]')
    split_view = list(search_results.select_one('div[data-automation="splitViewParentWrapper"] > div').children)
    # print(split_view)
    job_listings_wrapper = split_view[0]
    # job_details_wrapper = split_view[1]
    # print(job_details_wrapper.select_one('div[data-automation="jobDetailsPage"]'))
    return job_listings_wrapper

def get_total_jobs_count():
    # Get total number of jobs found on the website
    job_count = get_page_contents(0).select_one('span[data-automation="totalJobsCount"]').get_text()
    return job_count.replace(",", "")

def retrieve_jobs(job_listings_wrapper):
    job_listings = []

    # Get indivdual job listings from its main divs
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-card-type="JobCard"]')))
    job_cards = job_listings_wrapper.select('article[data-card-type="JobCard"]')
    job_cards_click = driver.find_elements(By.CSS_SELECTOR, 'article[data-card-type="JobCard"]')

    for i, card in enumerate(job_cards_click):
        job_experience = None
        job_fresh_grad = False

        card.find_element(By.CSS_SELECTOR, 'a[data-automation="jobTitle"]').click()
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-automation="jobAdDetails"]')))
            load_DOM()
            requirements_list = [li.get_text() for li in html.select_one('div[data-automation="jobAdDetails"]').select("li")]
            # requirments_tag = html.select_one(':-soup-contains("Requirements:")')
            # requirments_list = requirments_tag.findParent().next_sibling()
            for req in requirements_list:
                req_lowered = req.lower()
                # if keywords in req:
                if "year" in req_lowered:
                    # job_experience = req[:req_lowered.index("year")].replace("–", "to")
                    years_of_exp_idx = re.search(r"\d", req)
                    job_experience = req[years_of_exp_idx.start()] if years_of_exp_idx is not None else None
                    # print(years_of_exp_idx, job_experience)
                elif any(keyword in req_lowered for keyword in ["fresh", "less"]):
                    job_fresh_grad = True
                    # print(req, job_fresh_grad)
        except Exception as e:

            print("ERROR: ", e)

        job_card_details = list(job_cards[i].children)[-1]
        job_company_tag = job_card_details.select_one('a[data-automation="jobCompany"]')
        job_salary_tag = job_card_details.select_one('span[data-automation="jobSalary"] > span')
        job_title = job_card_details.select_one('a[data-automation="jobTitle"]').get_text()
        job_location = [location_description.get_text() for location_description in job_card_details.select('a[data-automation="jobLocation"]')]
        job_salary = job_salary_tag.get_text().replace("–", "-") if job_salary_tag is not None else ""
        job_classification = job_card_details.select_one('a[data-automation="jobClassification"]').get_text()
        job_listing_date = job_card_details.select_one('span[data-automation="jobListingDate"]').get_text()
        job_company = job_company_tag.get_text() if job_company_tag is not None else "**Private"
        job_id = job_cards[i]["data-job-id"]

        if job_id not in job_ids:
            job_listings.append(
                {
                    "Title": job_title,
                    "Company": job_company,
                    "Min. Years of Exp. Required": job_experience,
                    "Fresh Grad/Less Exp.": job_fresh_grad if job_fresh_grad else "",
                    "Location": ", ".join(job_location),
                    "Classification": job_classification.replace("(", "").replace(")",""),
                    "Salary": job_salary,
                    "Posted Date": str(parse(job_listing_date)).split(":")[0] + ":00:00",
                    "Job ID": job_id,
                    "URL": "{0}/job/{1}".format(BASE_URL, job_id)
                }
            )
            job_ids.append(job_id)

    export_job_listings(job_listings)

    # print(job_listings)

def export_job_listings(job_listings):
    df = pd.DataFrame(job_listings)
    df.to_csv(job_combined + ".csv", mode="a", index=False, header=False)

while not job:
    job = input("Type in the key word that you want to search for: ")
job_combined = job.replace(" ", "-")

# Create blank csv file (and overwrite old one if already exists)
pd.DataFrame({}, columns=["Title", "Company", "Min. Years of Exp. Required", "Fresh Grad", "Location", "Classification", "Salary", "Posted Date", "Job ID", "URL"]).to_csv(job_combined + ".csv", index=False, date_format="%Y%m%d %h%m")

search_extent = ""
total_jobs_count = get_total_jobs_count()
max_page_count = math.ceil(int(total_jobs_count) / 26)

search_extent = input("\nThe total number of jobs found was: {0}\nType 'all' to search all jobs OR type in the number of page you want to search (MAX is {1}): ".format(total_jobs_count, str(max_page_count)))

try:
    while int(search_extent) > max_page_count or int(search_extent) <= 0:
        search_extent = input("\nThe total number of jobs found was: {0}\nType 'all' to search all jobs OR type in the number of page you want to search (MAX is {1}): ".format(total_jobs_count, str(max_page_count)))
    search_extent = int(search_extent)
except(ValueError):
    # all
    while search_extent.lower() != "all":
        search_extent = input("\nThe total number of jobs found was: {0}\nType 'all' to search all jobs OR type in the number of page you want to search (MAX is {1}): ".format(total_jobs_count, str(max_page_count)))
    search_extent = max_page_count

# while search_extent != "all" or int(search_extent) > max_page_count or int(search_extent) <= 0:
#     search_extent = input("\nThe total number of jobs found was: {0}\nType 'all' to search all jobs OR type in the number of page you want to search (MAX is {1}): ".format(total_jobs_count, str(max_page_count)))

# keywords = input("Please type in the keywords (seperated by commas) that you want to search in the experience section: ")

for i in range(1, search_extent+1):
    # try:
        print("Now Processing PAGE {0} / {1}".format(i, search_extent))
        job_listings_wrapper = get_page_contents(cur_page = i)
        retrieve_jobs(job_listings_wrapper)
        time.sleep(0.5)
    # except Exception as e:
    #     print("ERROR at: ", i, e)
    #     last_avail_page = i
    #     # error_pages.append(i)
    #     break
# print(job_listings)
print("DONE!! -> " + job + ("\n--Cut short to page: " + str(last_avail_page) if last_avail_page > 0 else ""))
driver.quit()