import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Firefox options
options = Options()
options.add_argument("--headless")  # Run Firefox in headless mode

# Specify the path to GeckoDriver
gecko_driver_path = '/WebDriver/geckodriver.exe'

# Initialize the WebDriver using the Service class
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

# File path for the output CSV
output_csv_file = "indeed_jobs.csv"

try:
    # Define the search parameters
    job_title = "Software Engineer Intern"
    location = "United States"

    # Build the URL
    base_url = "https://www.indeed.com"
    search_url = f"{base_url}/jobs?q={job_title}&l={location}"

    # Open the search URL
    driver.get(search_url)

    # Wait until the job listings are present
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mosaic-provider-jobcards")))

    # Get the job listings
    job_cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

    # Open the CSV file for writing
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
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

                # Write job details to CSV
                writer.writerow([title, company, location, summary_salary, summary_type, job_url])

            except Exception as e:
                print("Error parsing job:", e)

finally:
    # Close the WebDriver
    driver.quit()

print(f"Jobs have been successfully written to {output_csv_file}")
