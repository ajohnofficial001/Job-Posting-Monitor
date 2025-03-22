import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Firefox options
options = Options()
options.add_argument("--headless")  # Run in headless mode; remove for debugging
# Optionally, set a custom user agent to mimic a real browser
#options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0")

# Specify the path to GeckoDriver
gecko_driver_path = 'C:/WebDriver/geckodriver.exe'

# Initialize the WebDriver using the Service class
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

# Input CSV (the one with basic job details and job URL)
input_csv = "linkedin_jobs.csv"
# Output CSV with detailed job description
output_csv = "linkedin_job_details.csv"

# Read the input CSV into a list of dictionaries
jobs = []
with open(input_csv, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        jobs.append(row)

# Open the output CSV for writing
with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = ["Job Title", "Company", "Location", "Posted Time", "Job URL", "Job Description"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for job in jobs:
        job_url = job["Job URL"]
        print(f"Processing: {job_url}")
        # Open the job URL in a new tab
        main_window = driver.current_window_handle
        driver.execute_script("window.open(arguments[0]);", job_url)
        time.sleep(2)
        # Switch to the new tab
        new_window = [handle for handle in driver.window_handles if handle != main_window][0]
        driver.switch_to.window(new_window)
        # Wait for the job description element to load
        wait = WebDriverWait(driver, 20)
        job_description = "N/A"
        try:
            # Try the first common selector
            desc_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.description__text")))
            job_description = desc_elem.text.strip()
        except Exception as e1:
            try:
                # Fallback: try another common selector
                desc_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobs-box__html-content")))
                job_description = desc_elem.text.strip()
            except Exception as e2:
                print(f"Error extracting description for {job_url}: {e1}, {e2}")
                job_description = "N/A"

        # Write job details to the output CSV
        writer.writerow({
            "Job Title": job["Job Title"],
            "Company": job["Company"],
            "Location": job["Location"],
            "Posted Time": job["Posted Time"],
            "Job URL": job_url,
            "Job Description": job_description
        })

        # Close the new tab and switch back to main window
        driver.close()
        driver.switch_to.window(main_window)
        time.sleep(1)

driver.quit()
print("Job details saved to", output_csv)
