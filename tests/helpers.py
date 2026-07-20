"""
Funciones auxiliares para las pruebas funcionales con Selenium.

Centraliza la localización de elementos y acciones comunes,
aplicando el concepto de Page Object Model simplificado:
  - Los SELECTORES se definen una sola vez en un diccionario.
  - Las funciones encontrar/llenar abstraen las esperas explícitas.
  - Si un selector cambia, solo se actualiza aquí.
"""

import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL


# ═══════════════════════════════════════════════════
#  SELECTORES CSS — atributos data-qa del sitio
# ═══════════════════════════════════════════════════
# Centralizar selectores facilita el mantenimiento:
# si un selector cambia en la aplicación, se actualiza solo aquí.

SELECTORES = {
    # Formulario de Login (en /login)
    "login_email":      'input[data-qa="login-email"]',
    "login_password":   'input[data-qa="login-password"]',
    "login_button":     'button[data-qa="login-button"]',

    # Formulario de Signup — paso 1 (en /login)
    "signup_name":      'input[data-qa="signup-name"]',
    "signup_email":     'input[data-qa="signup-email"]',
    "signup_button":    'button[data-qa="signup-button"]',

    # Formulario de Registro — paso 2 (en /signup)
    "password":         'input[data-qa="password"]',
    "first_name":       'input[data-qa="first_name"]',
    "last_name":        'input[data-qa="last_name"]',
    "address":          'input[data-qa="address"]',
    "country":          'select[data-qa="country"]',
    "state":            'input[data-qa="state"]',
    "city":             'input[data-qa="city"]',
    "zipcode":          'input[data-qa="zipcode"]',
    "mobile_number":    'input[data-qa="mobile_number"]',
    "create_account":   'button[data-qa="create-account"]',

    # Páginas de resultado
    "account_created":  '[data-qa="account-created"]',
    "account_deleted":  '[data-qa="account-deleted"]',
    "continue_button":  '[data-qa="continue-button"]',
}


# ═══════════════════════════════════════════════════
#  FUNCIONES DE NAVEGACIÓN
# ═══════════════════════════════════════════════════

def ir_a_login(driver):
    """Navega a la página de login de la aplicación."""
    driver.get(f"{BASE_URL}login")


def cerrar_sesion(driver):
    """Cierra la sesión del usuario navegando a /logout."""
    driver.get(f"{BASE_URL}logout")


# ═══════════════════════════════════════════════════
#  FUNCIONES DE LOCALIZACIÓN DE ELEMENTOS
# ═══════════════════════════════════════════════════
# Selenium ofrece distintos tipos de esperas explícitas (Expected Conditions).
# Cada función usa la EC adecuada según el caso de uso.

def encontrar(wait, nombre_selector):
    """
    Localiza un elemento usando EC.presence_of_element_located.

    Espera a que el elemento EXISTA en el DOM (aunque no sea visible).
    Útil para campos de formulario que ya están en la página.
    """
    return wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, SELECTORES[nombre_selector])
        )
    )


def encontrar_clickable(wait, nombre_selector):
    """
    Localiza un elemento usando EC.element_to_be_clickable.

    Espera a que el elemento sea VISIBLE y esté HABILITADO.
    Útil para botones y enlaces antes de hacer click.
    """
    return wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, SELECTORES[nombre_selector])
        )
    )


def encontrar_visible(wait, nombre_selector):
    """
    Localiza un elemento usando EC.visibility_of_element_located.

    Espera a que el elemento sea VISIBLE en la pantalla.
    Útil para validar mensajes de éxito o error.
    """
    return wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, SELECTORES[nombre_selector])
        )
    )


# ═══════════════════════════════════════════════════
#  FUNCIONES DE LLENADO DE FORMULARIOS
# ═══════════════════════════════════════════════════

def llenar_campo(wait, nombre_selector, texto):
    """Limpia un campo de texto y escribe el valor indicado."""
    campo = encontrar(wait, nombre_selector)
    campo.clear()
    campo.send_keys(texto)
    return campo


def llenar_formulario_login(wait, email, password):
    """
    Llena el formulario de login con email y contraseña.
    Retorna el botón de login listo para hacer click.
    """
    llenar_campo(wait, "login_email", email)
    llenar_campo(wait, "login_password", password)
    return encontrar_clickable(wait, "login_button")


def llenar_formulario_signup(wait, nombre, email):
    """
    Llena la sección inicial de Signup (nombre y email en /login).
    Retorna el botón de signup listo para hacer click.
    """
    llenar_campo(wait, "signup_name", nombre)
    llenar_campo(wait, "signup_email", email)
    return encontrar_clickable(wait, "signup_button")


def llenar_formulario_registro_completo(driver, wait, password):
    """
    Llena el formulario completo de registro en /signup.
    Incluye: contraseña, datos personales, país y dirección.

    Usa find_element directo (sin espera) porque la página
    ya cargó al llegar a este punto del flujo.
    """
    # Contraseña
    encontrar(wait, "password").send_keys(password)

    # Datos personales
    driver.find_element(By.CSS_SELECTOR, SELECTORES["first_name"]).send_keys("Test")
    driver.find_element(By.CSS_SELECTOR, SELECTORES["last_name"]).send_keys("Usuario")
    driver.find_element(By.CSS_SELECTOR, SELECTORES["address"]).send_keys("Calle Principal 123")

    # País (dropdown — se usa Select de Selenium para interactuar con <select>)
    Select(
        driver.find_element(By.CSS_SELECTOR, SELECTORES["country"])
    ).select_by_visible_text("United States")

    # Dirección
    driver.find_element(By.CSS_SELECTOR, SELECTORES["state"]).send_keys("California")
    driver.find_element(By.CSS_SELECTOR, SELECTORES["city"]).send_keys("Los Angeles")
    driver.find_element(By.CSS_SELECTOR, SELECTORES["zipcode"]).send_keys("90001")
    driver.find_element(By.CSS_SELECTOR, SELECTORES["mobile_number"]).send_keys("1234567890")


# ═══════════════════════════════════════════════════
#  FUNCIONES UTILITARIAS
# ═══════════════════════════════════════════════════

def generar_email_unico():
    """
    Genera un email aleatorio para evitar el error
    'Email Address already exist!' al registrar.
    """
    sufijo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"testuser_{sufijo}@testmail.com"


def eliminar_cuenta_prueba(driver, wait):
    """
    Elimina la cuenta de prueba navegando a /delete_account.
    Se usa para limpiar el entorno después de un registro exitoso.
    """
    driver.get(f"{BASE_URL}delete_account")
    try:
        deleted = encontrar_visible(wait, "account_deleted")
        if deleted.is_displayed():
            print("🧹 Cuenta de prueba eliminada")
            encontrar_clickable(wait, "continue_button").click()
    except Exception:
        print("⚠️  No se pudo eliminar la cuenta de prueba")
