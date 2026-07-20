from selenium import webdriver
from tests.test_login import login
from tests.test_add_pet import add_pet
import time

def inicializar_driver():
    driver = webdriver.Chrome()
    return driver

def main():
    driver = inicializar_driver()
    try:
        login(driver)
        time.sleep(2)
        add_pet(driver)
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        with open("error_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
