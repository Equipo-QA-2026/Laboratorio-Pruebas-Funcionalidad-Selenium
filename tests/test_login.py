from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import BASE_URL, USER_VALIDO, PASS_VALIDO, USER_INVALIDO, PASS_INVALIDO


credenciales = [
    {"email": USER_INVALIDO, "password": PASS_INVALIDO},
    {"email": USER_VALIDO, "password": PASS_VALIDO}
]

def login(driver):
    wait = WebDriverWait(driver, 10)
    for credencial in credenciales:
        driver.get(f"{BASE_URL}#/login")
        print(f"Pagina cargada: {driver.title}")

        input_email = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        input_password = wait.until(EC.presence_of_element_located((By.NAME, "password")))

        input_email.send_keys(Keys.CONTROL + "a")
        input_email.send_keys(Keys.DELETE)
        input_password.send_keys(Keys.CONTROL + "a")
        input_password.send_keys(Keys.DELETE)
        time.sleep(1.5)  # Espera para asegurar que los campos estén limpios

        input_email.send_keys(credencial["email"])
        print(f"Email ingresado correctamente: {credencial['email']}")
        input_password.send_keys(credencial["password"])
        print(f"Contraseña ingresada correctamente: {credencial['password']}")

        loggin_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        loggin_button.click()
        print("Botón de login clickeado")
