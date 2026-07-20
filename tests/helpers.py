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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL


# ═══════════════════════════════════════════════════
#  SELECTORES CSS — atributos data-qa del sitio
# ═══════════════════════════════════════════════════
# Centralizar selectores facilita el mantenimiento:
# si un selector cambia en la aplicación, se actualiza solo aquí.

SELECTORES = {
    # Formulario de Login (en #/login)
    "login_email":      'input[name="email"]',
    "login_password":   'input[name="password"]',
    "login_button":     'button[type="submit"]',

    # Formulario de Registro (en #/register)
    "signup_name":       'input[name="first_name"]',
    "signup_lastname":   'input[name="last_name"]',
    "signup_email":      'input[name="email"]',
    "signup_phone":      'input[name="phone_number"]',
    "signup_password":   'input[name="password"]',
    "signup_confirm":    'input[name="confirmPassword"]',
    "signup_button":     'button[type="submit"]',
}


# ═══════════════════════════════════════════════════
#  FUNCIONES DE NAVEGACIÓN
# ═══════════════════════════════════════════════════

def ir_a_login(driver):
    """Navega a la página de login de la aplicación."""
    driver.get(f"{BASE_URL}#/login")


def ir_a_registro(driver):
    """Navega directamente a la página de registro de la aplicación."""
    driver.get(f"{BASE_URL}#/register")


def cerrar_sesion(driver):
    """Cierra la sesión del usuario limpiando el almacenamiento local."""
    driver.execute_script("localStorage.clear(); sessionStorage.clear();")
    driver.get(f"{BASE_URL}#/login")


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
    # Limpiamos con teclas para asegurar que React detecte el borrado
    campo.send_keys(Keys.CONTROL + "a")
    campo.send_keys(Keys.DELETE)
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


def llenar_formulario_registro_completo(wait, nombre, apellido, email, telefono, password):
    """
    Llena el formulario completo de registro en #/register.
    """
    llenar_campo(wait, "signup_name", nombre)
    llenar_campo(wait, "signup_lastname", apellido)
    llenar_campo(wait, "signup_email", email)
    llenar_campo(wait, "signup_phone", telefono)
    llenar_campo(wait, "signup_password", password)
    llenar_campo(wait, "signup_confirm", password)
    
    return encontrar_clickable(wait, "signup_button")


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
    En este caso, la plataforma SmartAdopt no tiene una URL simple de /delete_account
    como automationexercise. Por lo tanto, no se ejecutará la eliminación aquí.
    Si la BD se limpia periódicamente, esto es suficiente.
    """
    pass
