from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Set up Firefox options
options = Options()
options.add_argument("--headless")  # Run Firefox in headless mode

# Specify the path to GeckoDriver
gecko_driver_path = '/WebDriver/geckodriver.exe'

# Initialize the WebDriver
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

# File path for the output CSV
output_csv_file = "linkedin_test.csv"

# LinkedIn job search URL
job_title = "Software Engineer Intern"
location = "United States"
base_url = "https://www.linkedin.com/jobs/search/"
search_url = f"{base_url}?keywords={job_title.replace(' ', '%20')}&location={location.replace(' ', '%20')}"

try:
    # Open the LinkedIn job search URL
    driver.get(search_url)
    time.sleep(5)  # Wait for the page to load completely

    # Handle the popover if it appears
    try:
        popover = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "artdeco-dismiss"))
        )
        popover.click()
        print("Dismissed the sign-in popover.")
    except Exception:
        print("No sign-in popover detected.")

    # Scroll to load all job cards
    print("Scrolling to load all job postings...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Wait for new content to load

        # Calculate new scroll height and compare with the last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # Break the loop if no new content is loaded
            break
        last_height = new_height

    print("All job postings loaded.")

    # Wait for the job list container to load
    wait = WebDriverWait(driver, 20)
    job_list_container = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
    )

    # Locate individual job cards within the container
    job_cards = job_list_container.find_elements(By.TAG_NAME, "li")

    # Open the CSV file for writing
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["Job Title", "Company", "Location", "Posted Time", "Job URL"])

        for job in job_cards:
                # Extract job title
            try:
                title_element = job.find_element(By.CSS_SELECTOR, 'h3')
                job_title = title_element.text.strip()
            except Exception:
                job_title = "N/A"

            # Extract company name
            try:
                company_element = job.find_element(By.CSS_SELECTOR, 'h4')
                company = company_element.text.strip()
            except Exception:
                company = "N/A"

            # Extract location
            try:
                location_element = job.find_element(By.CLASS_NAME, 'job-search-card__location')
                location = location_element.text.strip()
            except Exception:
                location = "N/A"

            # Extract posted time
            try:
                time_element = job.find_element(By.CLASS_NAME, 'job-search-card__listdate')
                posted_time = time_element.text.strip()
            except Exception:
                posted_time = "N/A"

            # Extract job URL
            try:
                job_url = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            except Exception:
                job_url = "N/A"

            # Write job details to CSV
            writer.writerow([job_title, company, location, posted_time, job_url])

            # except Exception as e:
            #     print(f"Error parsing job {index + 1}: {e}")

finally:
    # Close the WebDriver
    driver.quit()

print(f"LinkedIn jobs have been successfully written to {output_csv_file}.")
