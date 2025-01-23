import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Set up Firefox options
options = Options()
options.add_argument("--headless")  # Run Firefox in headless mode

# Specify the path to GeckoDriver
gecko_driver_path = '/WebDriver/geckodriver.exe'

# Initialize the WebDriver using the Service class
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

# File path for the output CSV
output_csv_file = "jobs.csv"

# Load existing job URLs to prevent duplicates
existing_jobs = set()
if os.path.exists(output_csv_file):
    with open(output_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_jobs.add(row['Job URL'])

try:
    # Define the search parameters
    job_title = "Software Engineer Intern"
    location = "United States"

    # Build the URL
    base_url = "https://www.indeed.com"
    search_url = f"{base_url}/jobs?q={job_title}&l={location}"

    # Open the search URL
    driver.get(search_url)

    # Wait for the job results container
    wait = WebDriverWait(driver, 20)
    job_results_container = wait.until(
        EC.presence_of_element_located((By.ID, "mosaic-jobResults"))
    )

    # Get the job listings within the container
    job_cards = job_results_container.find_elements(By.CLASS_NAME, "job_seen_beacon")

    # Open the CSV file for appending
    with open(output_csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row if the file is new
        if os.stat(output_csv_file).st_size == 0:
            writer.writerow(["Title", "Company", "Location", "Summary Salary", "Summary Type", "Job URL"])

        for job in job_cards:
            try:
                # Job Title
                title_element = job.find_element(By.CSS_SELECTOR, 'h2.jobTitle')
                title = title_element.text.strip()

                # Company Name
                company_element = job.find_element(By.CSS_SELECTOR, 'span[data-testid="company-name"]')
                company = company_element.text.strip()

                # Location
                location_element = job.find_element(By.CSS_SELECTOR, 'div[data-testid="text-location"]')
                location = location_element.text.strip()

                # Salary and Job Type
                summary_elements = job.find_elements(By.CSS_SELECTOR, 'div[data-testid="attribute_snippet_testid"]')
                summary_salary = ''
                summary_type = ''

                for element in summary_elements:
                    text = element.text.strip()
                    if any(word in text for word in ['per hour', 'per year', '$']):
                        summary_salary = text
                    elif any(word in text for word in ['Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary']):
                        summary_type = text

                # Job URL
                job_url = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

                # Skip if job URL already exists
                if job_url in existing_jobs:
                    continue

                # Write job details to CSV
                writer.writerow([title, company, location, summary_salary, summary_type, job_url])
                existing_jobs.add(job_url)  # Add to the set to prevent duplicates in the same run

            except Exception as e:
                print("Error parsing job:", e)

finally:
    # Close the WebDriver
    driver.quit()

print(f"Updated {output_csv_file} with new jobs.")
