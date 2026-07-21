"""
Configuración central del laboratorio de pruebas con Selenium.

Este archivo unifica toda la configuración del proyecto:
  1. Carga de variables de entorno desde .env (URLs, credenciales)
  2. Fixtures de pytest (driver de Chrome, WebDriverWait)
  3. Hook para capturas de pantalla automáticas tras cada test

pytest descubre conftest.py automáticamente — los fixtures
se inyectan en cada test que los declare como parámetro.
"""

import os
import sys
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


# ═══════════════════════════════════════════════════
#  CARGA DE VARIABLES DE ENTORNO (.env)
# ═══════════════════════════════════════════════════

def _cargar_env(ruta=".env"):
    """
    Lee el archivo .env y retorna un diccionario con las variables.
    Si el archivo no existe, muestra instrucciones y detiene la ejecución.
    """
    config = {}

    if not os.path.exists(ruta):
        print("=" * 60)
        print("ERROR: No se encontró el archivo .env")
        print("Copia el archivo .env.example y renómbralo a .env:")
        print("  copy .env.example .env   (Windows)")
        print("  cp .env.example .env     (Linux/Mac)")
        print("Luego completa las variables con tus datos.")
        print("=" * 60)
        sys.exit(1)

    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, valor = linea.split("=", 1)
            config[clave.strip()] = valor.strip().strip("\"'")
    return config


def _validar(env, nombre, descripcion):
    """Valida que una variable exista y no tenga el valor por defecto."""
    valor = env.get(nombre)
    if not valor or valor.startswith("dato de") or valor.startswith("url del"):
        print(f"⚠️  Variable '{nombre}' no configurada → {descripcion}")
        print(f"   Abre el archivo .env y completa el valor de {nombre}")
        return None
    return valor


# Cargar y validar todas las variables al inicio
_env = _cargar_env()

BASE_URL         = _validar(_env, "BASE_URL",         "URL base de la aplicación a probar")
USER_VALIDO      = _validar(_env, "USER_VALIDO",      "Email de un usuario válido")
PASS_VALIDO      = _validar(_env, "PASS_VALIDO",      "Contraseña de un usuario válido")
USER_INVALIDO    = _validar(_env, "USER_INVALIDO",     "Email de un usuario inválido")
PASS_INVALIDO    = _validar(_env, "PASS_INVALIDO",     "Contraseña inválida")
REGISTRO_NOMBRE  = _validar(_env, "REGISTRO_NOMBRE",   "Nombre para registrar un usuario nuevo")
REGISTRO_EMAIL   = _validar(_env, "REGISTRO_EMAIL",    "Email para registrar un usuario nuevo")
REGISTRO_PASS    = _validar(_env, "REGISTRO_PASS",     "Contraseña para el nuevo usuario")


# ═══════════════════════════════════════════════════
#  FIXTURES DE PYTEST
# ═══════════════════════════════════════════════════

@pytest.fixture(scope="session")
def driver():
    """
    Inicializa el navegador Chrome y lo comparte entre todas las pruebas.
    Al finalizar, cierra el navegador automáticamente.

    Para cambiar de navegador, modifica webdriver.Chrome() por:
    - webdriver.Firefox()  → para Firefox
    - webdriver.Edge()     → para Edge
    """
    opciones = Options()
    # Descomenta la siguiente línea para ejecutar sin abrir ventana:
    # opciones.add_argument("--headless")
    opciones.add_argument("--start-maximized")
    opciones.add_argument("--disable-extensions")

    navegador = webdriver.Chrome(options=opciones)
    navegador.implicitly_wait(5)

    yield navegador

    # Cleanup: cerrar el navegador al terminar todas las pruebas
    navegador.quit()


@pytest.fixture(scope="session")
def wait(driver):
    """
    Crea un WebDriverWait reutilizable (espera hasta 10 segundos).

    Evita repetir 'wait = WebDriverWait(driver, 10)' en cada test.
    Se inyecta automáticamente en cada test que lo declare como parámetro.
    """
    return WebDriverWait(driver, 10)


# ═══════════════════════════════════════════════════
#  HOOK: CAPTURAS DE PANTALLA AUTOMÁTICAS
# ═══════════════════════════════════════════════════

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de pytest que captura screenshots automáticamente
    después de cada prueba (pase o falle).

    Las capturas se guardan en la carpeta 'capturas/' con el formato:
        PASSED_nombre_del_test_HHMMSS.png
        FAILED_nombre_del_test_HHMMSS.png
    """
    outcome = yield
    report = outcome.get_result()

    # Solo capturar en la fase "call" (no en setup/teardown)
    if report.when == "call":
        # Obtener el driver del fixture
        driver = item.funcargs.get("driver", None)
        if driver is not None:
            # Crear carpeta de capturas si no existe
            os.makedirs("capturas", exist_ok=True)

            # Generar nombre del archivo
            timestamp = datetime.now().strftime("%H%M%S")
            estado = "PASSED" if report.passed else "FAILED"
            nombre_test = item.name
            archivo = f"capturas/{estado}_{nombre_test}_{timestamp}.png"

            # Tomar captura de pantalla
            try:
                driver.save_screenshot(archivo)
                print(f"\n📸 Captura guardada: {archivo}")
            except Exception as e:
                print(f"\n⚠️  No se pudo tomar captura: {e}")
