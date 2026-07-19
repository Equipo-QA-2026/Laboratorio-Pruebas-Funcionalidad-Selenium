"""
Pruebas funcionales de REGISTRO para Automation Exercise.
URL: https://automationexercise.com/login  (sección Signup)

Flujo de registro en Automation Exercise:
    1. En /login → llenar nombre y email en la sección "New User Signup!"
    2. Click en "Signup" → redirige a /signup con el formulario completo
    3. Llenar datos personales y dirección
    4. Click en "Create Account" → muestra página de "Account Created!"

Selectores utilizados (atributos data-qa del sitio):
    Paso 1 (en /login):
        - Nombre:  input[data-qa="signup-name"]
        - Email:   input[data-qa="signup-email"]
        - Botón:   button[data-qa="signup-button"]

    Paso 2 (en /signup - formulario completo):
        - Password:       input[data-qa="password"]
        - Nombre:         input[data-qa="first_name"]
        - Apellido:       input[data-qa="last_name"]
        - Dirección:      input[data-qa="address"]
        - País:           select[data-qa="country"]
        - Estado:         input[data-qa="state"]
        - Ciudad:         input[data-qa="city"]
        - Código postal:  input[data-qa="zipcode"]
        - Teléfono:       input[data-qa="mobile_number"]
        - Botón crear:    button[data-qa="create-account"]

    Página de éxito:
        - Indicador:      [data-qa="account-created"]
        - Continuar:      [data-qa="continue-button"]

Para adaptar a otra aplicación web:
    1. Cambia los selectores CSS en cada test
    2. Ajusta el flujo si el registro es en una sola página
    3. Actualiza las URLs y textos de validación
"""

import time
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, REGISTRO_NOMBRE, REGISTRO_EMAIL, REGISTRO_PASS


def generar_email_unico():
    """
    Genera un email único para evitar el error
    'Email Address already exist!' al registrar.
    """
    sufijo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"testuser_{sufijo}@testmail.com"


# ──────────────────────────────────────────────
#  CASO 1: Registro exitoso con datos completos
# ──────────────────────────────────────────────
def test_registro_exitoso(driver):
    """
    Verifica el flujo completo de registro:
    1. Ingresar nombre y email en /login (sección Signup)
    2. Llenar el formulario completo en /signup
    3. Verificar que se muestra 'Account Created!'
    4. Limpiar: eliminar la cuenta creada
    """
    wait = WebDriverWait(driver, 10)
    email_unico = generar_email_unico()

    # ── PASO 1: Ir a /login y llenar la sección de Signup ──
    driver.get(f"{BASE_URL}login")
    print(f"\n🌐 Página cargada: {driver.current_url}")

    input_nombre = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-name"]'))
    )
    input_email = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-email"]'))
    )

    input_nombre.clear()
    input_nombre.send_keys(REGISTRO_NOMBRE or "Usuario Test")
    print(f"📝 Nombre ingresado: {REGISTRO_NOMBRE or 'Usuario Test'}")

    input_email.clear()
    input_email.send_keys(email_unico)
    print(f"📧 Email ingresado: {email_unico}")

    # Click en el botón de Signup
    signup_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="signup-button"]'))
    )
    signup_button.click()
    print("🖱️  Botón de Signup clickeado")

    # ── PASO 2: Llenar el formulario completo de registro ──
    #    Esperar a que cargue la página /signup
    wait.until(EC.url_contains("signup"))
    print(f"📄 Redirigido a: {driver.current_url}")

    # Password
    input_password = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="password"]'))
    )
    input_password.send_keys(REGISTRO_PASS or "Test@12345")
    print("🔑 Contraseña ingresada: ******")

    # Datos personales
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="first_name"]').send_keys("Test")
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="last_name"]').send_keys("Usuario")
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="address"]').send_keys("Calle Principal 123")
    print("📋 Datos personales ingresados")

    # País (selector de dropdown)
    select_pais = Select(driver.find_element(By.CSS_SELECTOR, 'select[data-qa="country"]'))
    select_pais.select_by_visible_text("United States")

    # Dirección
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="state"]').send_keys("California")
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="city"]').send_keys("Los Angeles")
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="zipcode"]').send_keys("90001")
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="mobile_number"]').send_keys("1234567890")
    print("📍 Dirección ingresada")

    # ── PASO 3: Enviar el formulario ──
    crear_cuenta_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="create-account"]'))
    )
    crear_cuenta_button.click()
    print("🖱️  Botón 'Create Account' clickeado")

    # ── PASO 4: VALIDACIÓN → Debe aparecer "ACCOUNT CREATED!" ──
    account_created = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-qa="account-created"]'))
    )
    assert account_created.is_displayed(), "❌ No se mostró el mensaje de cuenta creada"
    print("✅ PRUEBA PASÓ → Cuenta creada exitosamente")

    # ── PASO 5: Continuar y limpiar la cuenta ──
    continue_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-qa="continue-button"]'))
    )
    continue_button.click()

    # Eliminar la cuenta de prueba para mantener el entorno limpio
    driver.get(f"{BASE_URL}delete_account")
    try:
        account_deleted = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-qa="account-deleted"]'))
        )
        if account_deleted.is_displayed():
            print("🧹 Cuenta de prueba eliminada correctamente")
            # Click en continuar después de eliminar
            continue_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-qa="continue-button"]'))
            )
            continue_btn.click()
    except Exception:
        print("⚠️  No se pudo eliminar la cuenta de prueba (puede que ya no exista)")


# ──────────────────────────────────────────────
#  CASO 2: Registro con email ya existente
# ──────────────────────────────────────────────
def test_registro_email_existente(driver):
    """
    Verifica que al intentar registrar un email que ya existe,
    el sistema muestra el mensaje 'Email Address already exist!'.

    Usa las credenciales USER_VALIDO del .env (cuenta ya registrada).
    """
    wait = WebDriverWait(driver, 10)

    # Importar email de usuario válido (ya registrado)
    from config import USER_VALIDO

    # 1. Navegar a /login (sección Signup)
    driver.get(f"{BASE_URL}login")
    print(f"\n🌐 Página cargada: {driver.current_url}")

    # 2. Ingresar nombre y email ya existente
    input_nombre = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-name"]'))
    )
    input_email = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-email"]'))
    )

    input_nombre.clear()
    input_nombre.send_keys("Usuario Duplicado")
    input_email.clear()
    input_email.send_keys(USER_VALIDO)
    print(f"📧 Email ya existente ingresado: {USER_VALIDO}")

    # 3. Click en Signup
    signup_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="signup-button"]'))
    )
    signup_button.click()
    print("🖱️  Botón de Signup clickeado")

    # 4. VALIDACIÓN: Debe aparecer "Email Address already exist!"
    mensaje_error = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//p[contains(text(), 'Email Address already exist')]")
        )
    )
    assert mensaje_error.is_displayed(), "❌ No se mostró el error de email duplicado"
    print(f"✅ PRUEBA PASÓ → Mensaje de error visible: '{mensaje_error.text}'")


# ──────────────────────────────────────────────
#  CASO 3: Registro con campos vacíos
# ──────────────────────────────────────────────
def test_registro_campos_vacios(driver):
    """
    Verifica que al intentar hacer signup sin llenar nombre o email,
    el formulario no se envía (validación HTML5 del navegador).
    """
    wait = WebDriverWait(driver, 10)

    # 1. Navegar a /login
    driver.get(f"{BASE_URL}login")
    print(f"\n🌐 Página cargada: {driver.current_url}")

    # 2. Asegurar que los campos estén vacíos
    input_nombre = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-name"]'))
    )
    input_email = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-email"]'))
    )
    input_nombre.clear()
    input_email.clear()

    # 3. Click en Signup con campos vacíos
    signup_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="signup-button"]'))
    )
    signup_button.click()
    print("🖱️  Botón de Signup clickeado con campos vacíos")

    # 4. VALIDACIÓN: Debe seguir en /login (validación HTML5 impide el envío)
    time.sleep(1)  # Pequeña espera para confirmar que no hubo redirección
    assert "login" in driver.current_url, "❌ El formulario se envió con campos vacíos"
    print("✅ PRUEBA PASÓ → El formulario no se envió sin datos")


# ──────────────────────────────────────────────
#  CASO 4: Verificar que la sección de Signup es visible
# ──────────────────────────────────────────────
def test_seccion_signup_visible(driver):
    """
    Verifica que la página de login muestra correctamente
    la sección de 'New User Signup!' con todos sus elementos.
    """
    wait = WebDriverWait(driver, 10)

    # 1. Navegar a /login
    driver.get(f"{BASE_URL}login")
    print(f"\n🌐 Página cargada: {driver.current_url}")

    # 2. VALIDACIÓN: Verificar que los elementos de signup están presentes
    input_nombre = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-name"]'))
    )
    input_email = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-email"]'))
    )
    signup_button = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-qa="signup-button"]'))
    )

    assert input_nombre.is_displayed(), "❌ El campo de nombre no está visible"
    assert input_email.is_displayed(), "❌ El campo de email no está visible"
    assert signup_button.is_displayed(), "❌ El botón de signup no está visible"
    print("✅ PRUEBA PASÓ → Todos los elementos de Signup están visibles")
