from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Setting up options
options = Options()
options.add_argument("--headless")

gecko_driver_path = "C:/WebDriver/geckodriver.exe"

service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

# Scholarship Page URL
base_url = "https://whosnext.tmcf.org/jobs?limit=100&page=1"
driver.get(base_url)
time.sleep(5)

# Scroll down to load all content (if dynamic)
# last_height = driver.execute_script("return document.body.scrollHeight")
# for _ in range(3):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(3)
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height

# Store Data in CSV
output_csv_file = "tmcf_jobs.csv"

try:
    wait = WebDriverWait(driver, 10)

    # Find all scholarship listings
    job_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search-result-item")))

    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Location", "Type", "URL"])

        for job in job_list:
            try:
                # Extract scholarship name (Update this if necessary)
                title_element = job.find_element(By.CSS_SELECTOR, ".job-title")
                title = title_element.text.strip()
            except:
                title = "N/A"

            try:
                # Extract location text (May need further checking)
                location_element = job.find_element(By.CSS_SELECTOR, "span.label-value.location")
                location = location_element.text.strip()
            except:
                location = "N/A"

            try:
                # Extract type (May need to refine)
                type_element = job.find_element(By.CSS_SELECTOR, "span.label-value.tags1")
                type = type_element.text.strip()
            except:
                type = "N/A"

            try:
                # Extract job URL
                link_element = job.find_element(By.CSS_SELECTOR, ".job-title-link")
                url = link_element.get_attribute("href")
            except:
                url = "N/A"

            writer.writerow([title, location, type, url])

finally:
    driver.quit()

print(f"Scholarship data saved to {output_csv_file}.")
