import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Set up Firefox options
options = Options()
options.add_argument("--headless")  # Remove for debugging

# Specify the path to GeckoDriver
gecko_driver_path = 'C:/WebDriver/geckodriver.exe'

# Initialize the WebDriver
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

# Base UNCF Opportunities Page (single page)
uncf_url = "https://scholarships.uncf.org/s/search-wizard?id=Scholarships%2CInternships%2CFellowships%2CCareer&value="

# File path for output CSV
output_csv_file = "uncf_opportunities.csv"

def parse_current_page(writer):
    """
    Scrapes the current page's rows and writes them to CSV.
    If a row has all fields as N/A, it skips that row.
    """
    wait = WebDriverWait(driver, 10)
    tbody_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    rows = tbody_element.find_elements(By.TAG_NAME, "tr")
    
    for index, row in enumerate(rows):
        # Reset fields for this row
        program_name = "N/A"
        program_type = "N/A"
        award_year = "N/A"
        open_date = "N/A"
        deadline = "N/A"
        application_link = "N/A"
        
        try:
            # Extract Program Name from <th>
            try:
                th_elem = row.find_element(By.TAG_NAME, "th")
                program_name = th_elem.get_attribute("data-cell-value").strip()
            except Exception:
                pass

            # Extract Program Type
            try:
                program_type_elem = row.find_element(By.XPATH, './/td[@data-label="Program Type"]')
                program_type = program_type_elem.get_attribute("data-cell-value").strip()
            except Exception:
                pass

            # Extract Award Year
            try:
                award_year_elem = row.find_element(By.XPATH, './/td[@data-label="Award Year"]')
                award_year = award_year_elem.get_attribute("data-cell-value").strip()
            except Exception:
                pass

            # Extract Open Date
            try:
                open_date_elem = row.find_element(By.XPATH, './/td[@data-label="Open Date"]')
                open_date = open_date_elem.get_attribute("data-cell-value").strip()
            except Exception:
                pass

            # Extract Deadline
            try:
                deadline_elem = row.find_element(By.XPATH, './/td[@data-label="Deadline"]')
                deadline = deadline_elem.get_attribute("data-cell-value").strip()
            except Exception:
                pass

            # Click the button to open detailed application link in a new tab
            try:
                button_elem = th_elem.find_element(By.TAG_NAME, "button")
                main_window = driver.current_window_handle
                driver.execute_script("arguments[0].click();", button_elem)
                time.sleep(2)
                
                # Get all window handles and switch to the new tab
                all_handles = driver.window_handles
                if len(all_handles) > 1:
                    for handle in all_handles:
                        if handle != main_window:
                            driver.switch_to.window(handle)
                            time.sleep(1)
                            application_link = driver.current_url
                            driver.close()
                            time.sleep(1)
                            driver.switch_to.window(main_window)
                            time.sleep(1)
                            break
            except Exception:
                # If clicking the button fails, application_link remains "N/A"
                pass

            # If all non-link fields are N/A, skip this row
            if (program_name == "N/A" and program_type == "N/A" and 
                award_year == "N/A" and open_date == "N/A" and 
                deadline == "N/A"):
                print(f"Skipping row {index+1} as all fields are N/A.")
                break

            writer.writerow([program_name, program_type, award_year, open_date, deadline, application_link])
            print(f"Extracted row {index+1}: {program_name} - {application_link}")

        except Exception as e:
            print(f"Error extracting row {index+1}: {e}")

try:
    driver.get(uncf_url)
    time.sleep(5)  # Allow time for the page to load

    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Program Name", "Program Type", "Award Year", "Open Date", "Deadline", "Application Link"])
        parse_current_page(writer)

finally:
    driver.quit()

print(f"\nUNCF opportunities saved to {output_csv_file}.")
