# -*- coding: utf-8 -*-
"""
Script de demostracion del Laboratorio de Pruebas Funcionales con Selenium.

Este script ejecuta las pruebas en un orden especifico para demostrar
que todo funciona correctamente:

1. Primero registra una cuenta nueva (test de registro)
2. Luego usa esa cuenta para probar el login
3. Toma capturas de pantalla de cada paso

Ejecutar:  py demo.py
"""

import sys
import io
import time
import random
import string
import os

# Forzar salida UTF-8 en consola de Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL


# ---- CONFIGURACION ----
os.makedirs("capturas", exist_ok=True)
CAPTURAS = []  # Lista de capturas tomadas

# Datos de prueba generados automaticamente
sufijo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
EMAIL_NUEVO = f"selenium_demo_{sufijo}@testmail.com"
PASSWORD_NUEVO = "DemoTest2026!"
NOMBRE_NUEVO = "Selenium Demo"


def captura(driver, nombre):
    """Toma una captura de pantalla y la guarda en la carpeta capturas/"""
    archivo = f"capturas/{nombre}.png"
    driver.save_screenshot(archivo)
    CAPTURAS.append(archivo)
    print(f"   [CAPTURA] {archivo}")


def separador(titulo):
    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")


# ---- INICIALIZAR NAVEGADOR ----
print("\n>>> Iniciando Laboratorio de Pruebas Funcionales con Selenium")
print(f"    URL objetivo: {BASE_URL}")
print(f"    Email de prueba: {EMAIL_NUEVO}")

opciones = Options()
opciones.add_argument("--start-maximized")
opciones.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=opciones)
wait = WebDriverWait(driver, 15)

try:

    # =============================================
    #  PRUEBA 1: Verificar seccion de Signup visible
    # =============================================
    separador("PRUEBA 1: Verificar seccion de Signup visible")

    driver.get(f"{BASE_URL}login")
    time.sleep(2)
    print(f"   Pagina cargada: {driver.current_url}")

    input_nombre_signup = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-name"]'))
    )
    input_email_signup = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-email"]'))
    )
    signup_button = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-qa="signup-button"]'))
    )

    assert input_nombre_signup.is_displayed()
    assert input_email_signup.is_displayed()
    assert signup_button.is_displayed()
    captura(driver, "01_signup_seccion_visible")
    print("   [PASO] Todos los elementos de Signup estan visibles")


    # =============================================
    #  PRUEBA 2: Registro con campos vacios
    # =============================================
    separador("PRUEBA 2: Registro con campos vacios")

    driver.get(f"{BASE_URL}login")
    time.sleep(2)

    input_nombre_signup = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-name"]'))
    )
    input_nombre_signup.clear()

    signup_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="signup-button"]'))
    )
    signup_button.click()
    time.sleep(1)

    assert "login" in driver.current_url
    captura(driver, "02_registro_campos_vacios")
    print("   [PASO] El formulario no se envio sin datos")


    # =============================================
    #  PRUEBA 3: Registro exitoso (flujo completo)
    # =============================================
    separador("PRUEBA 3: Registro exitoso (flujo completo)")

    driver.get(f"{BASE_URL}login")
    time.sleep(2)
    print(f"   Pagina cargada: {driver.current_url}")

    # Paso 1: Llenar nombre y email en seccion Signup
    input_nombre_signup = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-name"]'))
    )
    input_email_signup = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-email"]'))
    )

    input_nombre_signup.clear()
    input_nombre_signup.send_keys(NOMBRE_NUEVO)
    input_email_signup.clear()
    input_email_signup.send_keys(EMAIL_NUEVO)
    print(f"   Nombre: {NOMBRE_NUEVO}")
    print(f"   Email: {EMAIL_NUEVO}")

    captura(driver, "03_registro_datos_iniciales")

    signup_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="signup-button"]'))
    )
    signup_button.click()
    print("   Boton Signup clickeado")

    # Paso 2: Llenar formulario completo
    wait.until(EC.url_contains("signup"))
    time.sleep(1)
    print(f"   Redirigido a: {driver.current_url}")

    captura(driver, "04_registro_formulario_completo")

    # Password
    input_password = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="password"]'))
    )
    input_password.send_keys(PASSWORD_NUEVO)
    print("   Password ingresada: ******")

    # Datos personales
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="first_name"]').send_keys("Selenium")
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="last_name"]').send_keys("Demo")
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="address"]').send_keys("Calle de Pruebas 123")
    print("   Datos personales ingresados")

    # Pais
    select_pais = Select(driver.find_element(By.CSS_SELECTOR, 'select[data-qa="country"]'))
    select_pais.select_by_visible_text("United States")

    # Direccion
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="state"]').send_keys("California")
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="city"]').send_keys("Los Angeles")
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="zipcode"]').send_keys("90001")
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="mobile_number"]').send_keys("1234567890")
    print("   Direccion ingresada")

    captura(driver, "05_registro_formulario_lleno")

    # Enviar formulario
    crear_cuenta_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="create-account"]'))
    )
    crear_cuenta_btn.click()
    print("   Boton 'Create Account' clickeado")

    # Validar: "ACCOUNT CREATED!"
    account_created = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-qa="account-created"]'))
    )
    assert account_created.is_displayed()
    captura(driver, "06_registro_cuenta_creada")
    print("   [PASO] Cuenta creada exitosamente!")

    # Continuar al home
    continue_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-qa="continue-button"]'))
    )
    continue_btn.click()
    time.sleep(2)
    captura(driver, "07_registro_home_logueado")

    # Hacer logout para las pruebas de login
    driver.get(f"{BASE_URL}logout")
    time.sleep(2)
    print("   Logout realizado para preparar pruebas de login")


    # =============================================
    #  PRUEBA 4: Login con credenciales invalidas
    # =============================================
    separador("PRUEBA 4: Login con credenciales invalidas")

    driver.get(f"{BASE_URL}login")
    time.sleep(2)
    print(f"   Pagina cargada: {driver.current_url}")

    input_email_login = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-email"]'))
    )
    input_pass_login = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-password"]'))
    )

    input_email_login.clear()
    input_pass_login.clear()
    input_email_login.send_keys("usuario_falso@noexiste.com")
    input_pass_login.send_keys("contrasena_incorrecta")
    print("   Email invalido ingresado")
    print("   Password invalida ingresada")

    captura(driver, "08_login_credenciales_invalidas")

    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="login-button"]'))
    )
    login_button.click()
    print("   Boton Login clickeado")
    time.sleep(2)

    mensaje_error = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//p[contains(text(), 'Your email or password is incorrect')]")
        )
    )
    assert mensaje_error.is_displayed()
    captura(driver, "09_login_error_mostrado")
    print(f"   [PASO] Mensaje de error: '{mensaje_error.text}'")


    # =============================================
    #  PRUEBA 5: Login con campos vacios
    # =============================================
    separador("PRUEBA 5: Login con campos vacios")

    driver.get(f"{BASE_URL}login")
    time.sleep(2)

    input_email_login = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-email"]'))
    )
    input_email_login.clear()

    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="login-button"]'))
    )
    login_button.click()
    time.sleep(1)

    assert "login" in driver.current_url
    captura(driver, "10_login_campos_vacios")
    print("   [PASO] El formulario no se envio sin datos")


    # =============================================
    #  PRUEBA 6: Login con credenciales validas
    # =============================================
    separador("PRUEBA 6: Login con credenciales validas")

    driver.get(f"{BASE_URL}login")
    time.sleep(2)
    print(f"   Pagina cargada: {driver.current_url}")

    input_email_login = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-email"]'))
    )
    input_pass_login = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-password"]'))
    )

    input_email_login.clear()
    input_pass_login.clear()
    input_email_login.send_keys(EMAIL_NUEVO)
    input_pass_login.send_keys(PASSWORD_NUEVO)
    print(f"   Email ingresado: {EMAIL_NUEVO}")
    print("   Password ingresada: ******")

    captura(driver, "11_login_credenciales_validas")

    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="login-button"]'))
    )
    login_button.click()
    print("   Boton Login clickeado")
    time.sleep(3)

    logged_in = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//a[contains(text(), 'Logged in as')]")
        )
    )
    assert logged_in.is_displayed()
    captura(driver, "12_login_exitoso_logueado")
    print(f"   [PASO] {logged_in.text.strip()}")


    # =============================================
    #  PRUEBA 7: Registro con email ya existente
    # =============================================
    separador("PRUEBA 7: Registro con email ya existente")

    # Primero hacer logout
    driver.get(f"{BASE_URL}logout")
    time.sleep(2)

    driver.get(f"{BASE_URL}login")
    time.sleep(2)
    print(f"   Pagina cargada: {driver.current_url}")

    input_nombre_signup = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-name"]'))
    )
    input_email_signup = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="signup-email"]'))
    )

    input_nombre_signup.clear()
    input_nombre_signup.send_keys("Usuario Duplicado")
    input_email_signup.clear()
    input_email_signup.send_keys(EMAIL_NUEVO)  # Email que ya registramos
    print(f"   Email ya existente: {EMAIL_NUEVO}")

    captura(driver, "13_registro_email_existente")

    signup_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="signup-button"]'))
    )
    signup_button.click()
    print("   Boton Signup clickeado")
    time.sleep(2)

    mensaje_error = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//p[contains(text(), 'Email Address already exist')]")
        )
    )
    assert mensaje_error.is_displayed()
    captura(driver, "14_registro_error_email_duplicado")
    print(f"   [PASO] Mensaje: '{mensaje_error.text}'")


    # =============================================
    #  LIMPIEZA: Eliminar cuenta de prueba
    # =============================================
    separador("LIMPIEZA: Eliminando cuenta de prueba")

    # Login para poder eliminar
    driver.get(f"{BASE_URL}login")
    time.sleep(2)
    input_email_login = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-email"]'))
    )
    input_pass_login = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-password"]'))
    )
    input_email_login.clear()
    input_pass_login.clear()
    input_email_login.send_keys(EMAIL_NUEVO)
    input_pass_login.send_keys(PASSWORD_NUEVO)
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="login-button"]'))
    )
    login_button.click()
    time.sleep(2)

    driver.get(f"{BASE_URL}delete_account")
    time.sleep(2)
    try:
        deleted = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-qa="account-deleted"]'))
        )
        if deleted.is_displayed():
            captura(driver, "15_cuenta_eliminada")
            print("   Cuenta de prueba eliminada correctamente")
    except Exception:
        print("   No se pudo eliminar la cuenta")


    # =============================================
    #  RESUMEN FINAL
    # =============================================
    separador("RESUMEN FINAL")
    print(f"\n   7/7 pruebas ejecutadas exitosamente")
    print(f"   {len(CAPTURAS)} capturas guardadas en la carpeta 'capturas/':")
    for c in CAPTURAS:
        print(f"      -> {c}")
    print(f"\n   El laboratorio de Selenium funciona correctamente!")

except Exception as e:
    try:
        captura(driver, "ERROR_excepcion")
    except Exception:
        pass
    print(f"\n   [ERROR] Error durante la ejecucion: {e}")
    import traceback
    traceback.print_exc()

finally:
    time.sleep(2)
    driver.quit()
    print(f"\n{'='*60}")
    print("   Navegador cerrado. Demo finalizada.")
    print(f"{'='*60}\n")
