from selenium import webdriver
from tests.test_login import login
import time

def inicializar_driver():
    driver = webdriver.Chrome()
    return driver

def main():
    driver = inicializar_driver()
    try:
        login(driver)
        time.sleep(2)
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
