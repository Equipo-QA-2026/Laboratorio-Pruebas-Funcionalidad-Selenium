import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, USER_VALIDO, PASS_VALIDO, USER_INVALIDO, PASS_INVALIDO

# Lista de casos de prueba. Cada tupla contiene email, contrasena y si se espera exito o no.
credenciales = [
    (USER_INVALIDO, PASS_INVALIDO, False),
    (USER_VALIDO, PASS_VALIDO, True)
]

@pytest.mark.parametrize("email, password, is_valid", credenciales)
def test_login(driver, email, password, is_valid):
    """Verifica el funcionamiento del formulario de inicio de sesion con multiples combinaciones."""
    wait = WebDriverWait(driver, 10)
    
    # Navegar a la vista de login
    driver.get(f"{BASE_URL}#/login")
    print(f"Pagina cargada: {driver.title}")

    # Localizar los campos del formulario
    input_email = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    input_password = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    # Asegurar que los campos esten vacios antes de escribir
    input_email.clear()
    input_password.clear()

    # Ingresar los datos de prueba
    input_email.send_keys(email)
    print(f"Email ingresado: {email}")
    input_password.send_keys(password)
    print(f"Contrasena ingresada: {password}")

    # Enviar el formulario
    loggin_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    loggin_button.click()
    print("Boton de login clickeado")
    
    # Evaluar el resultado esperado de la prueba
    if is_valid:
        # Si las credenciales son correctas, debe redirigir al panel de administracion
        wait.until(EC.url_contains("/admin"))
        print("Login exitoso, redireccion a dashboard detectada.")
    else:
        # Si las credenciales son falsas, no debe ocurrir redireccion
        time.sleep(2)
        assert "/admin" not in driver.current_url, "Error: El login invalido logro acceder al sistema."
