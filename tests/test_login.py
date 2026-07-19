"""
Pruebas funcionales de LOGIN para Automation Exercise.
URL: https://automationexercise.com/login

Selectores utilizados (atributos data-qa del sitio):
    - Email:    input[data-qa="login-email"]
    - Password: input[data-qa="login-password"]
    - Botón:    button[data-qa="login-button"]

Para adaptar a otra aplicación web:
    1. Cambia los selectores CSS en cada test
    2. Ajusta los textos de validación (mensajes de error/éxito)
    3. Actualiza las URLs si la ruta de login es diferente
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, USER_VALIDO, PASS_VALIDO, USER_INVALIDO, PASS_INVALIDO


# ──────────────────────────────────────────────
#  CASO 1: Login con credenciales inválidas
# ──────────────────────────────────────────────
def test_login_credenciales_invalidas(driver):
    """
    Verifica que al ingresar credenciales incorrectas,
    el sistema muestra un mensaje de error y NO deja entrar.
    """
    wait = WebDriverWait(driver, 10)

    # 1. Navegar a la página de login
    driver.get(f"{BASE_URL}login")
    print(f"\n🌐 Página cargada: {driver.current_url}")

    # 2. Localizar los campos del formulario de login
    #    Selector: data-qa="login-email" y data-qa="login-password"
    input_email = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-email"]'))
    )
    input_password = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-password"]'))
    )

    # 3. Limpiar campos e ingresar credenciales inválidas
    input_email.clear()
    input_password.clear()
    input_email.send_keys(USER_INVALIDO)
    print(f"📧 Email ingresado: {USER_INVALIDO}")
    input_password.send_keys(PASS_INVALIDO)
    print("🔑 Contraseña ingresada: ******")

    # 4. Hacer clic en el botón de login
    #    Selector: data-qa="login-button"
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="login-button"]'))
    )
    login_button.click()
    print("🖱️  Botón de login clickeado")

    # 5. VALIDACIÓN: Debe aparecer un mensaje de error
    #    El sitio muestra: "Your email or password is incorrect!"
    mensaje_error = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Your email or password is incorrect')]"))
    )
    assert mensaje_error.is_displayed(), "❌ No se mostró el mensaje de error para credenciales inválidas"
    print(f"✅ PRUEBA PASÓ → Mensaje de error visible: '{mensaje_error.text}'")


# ──────────────────────────────────────────────
#  CASO 2: Login con credenciales válidas
# ──────────────────────────────────────────────
def test_login_credenciales_validas(driver):
    """
    Verifica que al ingresar credenciales correctas,
    el sistema permite el acceso y muestra el nombre del usuario.

    NOTA: Para que esta prueba funcione, primero debes tener
    una cuenta registrada en Automation Exercise con las
    credenciales definidas en el archivo .env
    """
    wait = WebDriverWait(driver, 10)

    # 1. Navegar a la página de login
    driver.get(f"{BASE_URL}login")
    print(f"\n🌐 Página cargada: {driver.current_url}")

    # 2. Localizar los campos del formulario de login
    input_email = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-email"]'))
    )
    input_password = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-password"]'))
    )

    # 3. Limpiar campos e ingresar credenciales válidas
    input_email.clear()
    input_password.clear()
    input_email.send_keys(USER_VALIDO)
    print(f"📧 Email ingresado: {USER_VALIDO}")
    input_password.send_keys(PASS_VALIDO)
    print("🔑 Contraseña ingresada: ******")

    # 4. Hacer clic en el botón de login
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="login-button"]'))
    )
    login_button.click()
    print("🖱️  Botón de login clickeado")

    # 5. VALIDACIÓN: Debe aparecer "Logged in as [usuario]" en la barra de navegación
    logged_in_text = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Logged in as')]"))
    )
    assert logged_in_text.is_displayed(), "❌ No se detectó el texto 'Logged in as' después del login"
    print(f"✅ PRUEBA PASÓ → Usuario logueado: '{logged_in_text.text.strip()}'")


# ──────────────────────────────────────────────
#  CASO 3: Login con campos vacíos
# ──────────────────────────────────────────────
def test_login_campos_vacios(driver):
    """
    Verifica que al intentar hacer login sin llenar los campos,
    el formulario no se envía (validación HTML5 del navegador).
    """
    wait = WebDriverWait(driver, 10)

    # 1. Navegar a la página de login
    driver.get(f"{BASE_URL}login")
    print(f"\n🌐 Página cargada: {driver.current_url}")

    # 2. Localizar campos y asegurar que estén vacíos
    input_email = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-email"]'))
    )
    input_email.clear()

    # 3. Hacer clic en login sin llenar campos
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="login-button"]'))
    )
    login_button.click()
    print("🖱️  Botón de login clickeado con campos vacíos")

    # 4. VALIDACIÓN: La URL debe seguir siendo /login (no se envió el formulario)
    assert "login" in driver.current_url, "❌ La página navegó fuera de /login con campos vacíos"
    print("✅ PRUEBA PASÓ → El formulario no se envió con campos vacíos")
