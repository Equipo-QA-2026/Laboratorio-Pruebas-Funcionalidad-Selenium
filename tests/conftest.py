import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, USER_VALIDO, PASS_VALIDO

# Definicion de rutas absolutas para almacenar las evidencias generadas
EVIDENCIAS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "evidencias")
EXITOSAS_DIR = os.path.join(EVIDENCIAS_DIR, "exitosas")
FALLIDAS_DIR = os.path.join(EVIDENCIAS_DIR, "fallidas")

@pytest.fixture(scope="function")
def driver():
    """Inicializa una instancia del navegador para la prueba y la cierra al finalizar."""
    _driver = webdriver.Chrome()
    _driver.maximize_window()
    yield _driver
    _driver.quit()

@pytest.fixture(scope="function")
def driver_with_login(driver):
    """Ejecuta el flujo de inicio de sesion antes de ceder el control a la prueba principal."""
    wait = WebDriverWait(driver, 10)
    driver.get(f"{BASE_URL}#/login")
    
    # Localizar e ingresar las credenciales validas
    input_email = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    input_password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    input_email.send_keys(USER_VALIDO)
    input_password.send_keys(PASS_VALIDO)
    
    # Presionar el boton de ingreso
    loggin_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    loggin_button.click()
    
    # Confirmar que la redireccion al panel principal ocurrio (salio del login)
    wait.until(EC.url_changes(f"{BASE_URL}#/login"))
    return driver

import re

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Intercepta los resultados de cada prueba para guardar capturas de pantalla y codigo fuente."""
    outcome = yield
    report = outcome.get_result()
    
    # Solo actuar cuando la prueba termina su fase de ejecucion
    if report.when == "call":
        driver_fixture = item.funcargs.get('driver') or item.funcargs.get('driver_with_login')
        
        if driver_fixture:
            # Limpiar el nombre de la prueba para evitar caracteres invalidos en Windows (*, /, etc)
            nombre_prueba = re.sub(r'[\\/*?:"<>|]', "", item.name)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            if report.failed:
                # Guardar captura y codigo HTML si la prueba fracaso
                screenshot_path = os.path.join(FALLIDAS_DIR, f"{nombre_prueba}_{timestamp}.png")
                html_path = os.path.join(FALLIDAS_DIR, f"{nombre_prueba}_{timestamp}.html")
                driver_fixture.save_screenshot(screenshot_path)
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(driver_fixture.page_source)
                print(f"\n[FALLO] Evidencias guardadas en: {FALLIDAS_DIR}")
                
            elif report.passed:
                # Guardar captura unicamente si la prueba tuvo exito
                screenshot_path = os.path.join(EXITOSAS_DIR, f"{nombre_prueba}_{timestamp}.png")
                driver_fixture.save_screenshot(screenshot_path)
                print(f"\n[EXITO] Evidencia guardada en: {EXITOSAS_DIR}")
