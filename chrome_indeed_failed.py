from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Setup the Chrome WebDriver
os.environ['PATH'] += r';C:\WebDriver'
driver = webdriver.Chrome()  
driver.get('https://www.indeed.com')

try:
    # Locate the job search box (Indeed uses different IDs; 'q' is common)
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys('Internship for computer science')
    
    # Locate the find jobs button and click it
    find_jobs_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    find_jobs_button.click()

    # Wait for the job results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'mosaic-provider-jobcards'))
    )

    # Find job titles within the job cards
    jobs = driver.find_elements(By.CSS_SELECTOR, 'a[data-mobtk]')
    for job in jobs:
        title = job.get_attribute('aria-label')
        if title:  # Check if title is not None
            print(title)

finally:
    driver.quit()
