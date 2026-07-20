from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
try:
    driver.get("http://smartadoptqa.programacionwebuce.net/#/login")
    wait = WebDriverWait(driver, 10)
    
    input_email = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    input_password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    
    input_email.send_keys("admin@smartadopt.com")
    input_password.send_keys("Admin1234")
    
    loggin_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    loggin_button.click()
    
    time.sleep(3)
    driver.get("http://smartadoptqa.programacionwebuce.net/#/admin/pets/new")
    time.sleep(5)
    
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("Page source saved to page_source.html")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
