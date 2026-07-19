import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def driver():
    """
    Fixture de pytest que inicializa el navegador Chrome
    y lo comparte entre todas las pruebas de la sesión.

    Al finalizar todas las pruebas, cierra el navegador automáticamente.

    Para cambiar de navegador, modifica webdriver.Chrome() por:
    - webdriver.Firefox()  → para Firefox
    - webdriver.Edge()     → para Edge
    """
    opciones = Options()
    # Descomenta la siguiente línea para ejecutar sin abrir ventana del navegador:
    # opciones.add_argument("--headless")
    opciones.add_argument("--start-maximized")
    opciones.add_argument("--disable-extensions")

    navegador = webdriver.Chrome(options=opciones)
    navegador.implicitly_wait(5)

    yield navegador

    # Cleanup: cerrar el navegador al terminar todas las pruebas
    navegador.quit()


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
