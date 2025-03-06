import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Firefox options
options = Options()
options.add_argument("--headless")  # Run Firefox in headless mode (remove for debugging)

# Specify the path to GeckoDriver
gecko_driver_path = '/WebDriver/geckodriver.exe'

# Initialize the WebDriver
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

# UNCF Opportunities Page
uncf_url = "https://scholarships.uncf.org/s/search-wizard?id=Scholarships%2CInternships%2CFellowships%2CCareer&value="

# File path for output CSV
output_csv_file = "uncf_opportunities.csv"

try:
    # Open UNCF page
    driver.get(uncf_url)
    time.sleep(5)  # Allow time for the page to load

    # Wait for the table body containing the opportunities
    wait = WebDriverWait(driver, 20)
    tbody_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))

    # Find all scholarship rows inside <tbody>
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")

    # Open CSV file for writing
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Program Name", "Program Type", "Award Year", "Open Date", "Deadline", "Application Link"])

        for index, row in enumerate(rows):
            try:
                # Extract Program Name from <th> (contains a button)
                try:
                    program_name_element = row.find_element(By.TAG_NAME, "th")
                    program_name = program_name_element.get_attribute("data-cell-value").strip()
                except:
                    program_name = "N/A"

                # Extract Program Type
                try:
                    program_type_element = row.find_element(By.XPATH, './/td[@data-label="Program Type"]')
                    program_type = program_type_element.get_attribute("data-cell-value").strip()
                except:
                    program_type = "N/A"

                # Extract Award Year
                try:
                    award_year_element = row.find_element(By.XPATH, './/td[@data-label="Award Year"]')
                    award_year = award_year_element.get_attribute("data-cell-value").strip()
                except:
                    award_year = "N/A"

                # Extract Open Date
                try:
                    open_date_element = row.find_element(By.XPATH, './/td[@data-label="Open Date"]')
                    open_date = open_date_element.get_attribute("data-cell-value").strip()
                except:
                    open_date = "N/A"

                # Extract Deadline
                try:
                    deadline_element = row.find_element(By.XPATH, './/td[@data-label="Deadline"]')
                    deadline = deadline_element.get_attribute("data-cell-value").strip()
                except:
                    deadline = "N/A"

                # Click the button to open the modal/pop-up
                try:
                    button_element = program_name_element.find_element(By.TAG_NAME, "button")
                    driver.execute_script("arguments[0].click();", button_element)  # Use JavaScript click
                    time.sleep(2)  # Wait for modal to open

                    # Extract the actual application link from the modal
                    try:
                        link_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "scholarships.uncf.org/details")]'))
                        )
                        application_link = link_element.get_attribute("href")
                    except:
                        application_link = "N/A"

                    # Close the modal (if applicable)
                    try:
                        close_button = driver.find_element(By.XPATH, '//button[@title="Close"]')
                        close_button.click()
                        time.sleep(2)  # Wait for modal to close
                    except:
                        print("No close button found, continuing...")

                except:
                    application_link = "N/A"

                # Write to CSV
                writer.writerow([program_name, program_type, award_year, open_date, deadline, application_link])

                print(f"Extracted {index + 1}: {program_name} - {application_link}")

            except Exception as e:
                print(f"Error extracting opportunity {index + 1}: {e}")

finally:
    # Close WebDriver
    driver.quit()

print(f"UNCF opportunities saved to {output_csv_file}.")
