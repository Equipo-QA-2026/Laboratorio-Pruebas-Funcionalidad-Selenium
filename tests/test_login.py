"""
Pruebas funcionales de LOGIN — Automation Exercise.

Estas pruebas verifican el comportamiento del formulario de login
en tres escenarios distintos:

  Caso 1: Credenciales inválidas → debe mostrar mensaje de error
  Caso 2: Credenciales válidas   → debe mostrar "Logged in as"
  Caso 3: Campos vacíos          → no debe enviar el formulario

Cada test recibe los fixtures 'driver' y 'wait' automáticamente
desde conftest.py (inyección de dependencias de pytest).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL, USER_VALIDO, PASS_VALIDO, USER_INVALIDO, PASS_INVALIDO
from tests.helpers import ir_a_login, cerrar_sesion, llenar_formulario_login, encontrar, encontrar_clickable


# ──────────────────────────────────────────────
#  CASO 1: Login con credenciales inválidas
# ──────────────────────────────────────────────
def test_login_credenciales_invalidas(driver, wait):
    """
    Verifica que al ingresar credenciales incorrectas,
    el sistema muestra un mensaje de error y NO deja entrar.
    """
    # 1. Navegar a la página de login
    ir_a_login(driver)
    print(f"\n🌐 Página cargada: {driver.current_url}")

    # 2. Llenar formulario con credenciales inválidas y hacer click
    boton = llenar_formulario_login(wait, USER_INVALIDO, PASS_INVALIDO)
    print(f"📧 Email ingresado: {USER_INVALIDO}")
    print("🔑 Contraseña ingresada: ******")
    driver.execute_script("arguments[0].click();", boton)
    print("🖱️  Botón de login clickeado")

    # 3. VALIDACIÓN: Debe aparecer mensaje de error (usamos role="alert" o MuiAlert)
    mensaje_error = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[@role='alert'] | //*[contains(@class, 'MuiAlert-message')]")
        )
    )
    assert mensaje_error.is_displayed(), "❌ No se mostró el mensaje de error"
    print(f"✅ PRUEBA PASÓ → Mensaje de error visible: '{mensaje_error.text}'")


# ──────────────────────────────────────────────
#  CASO 2: Login con credenciales válidas
# ──────────────────────────────────────────────
def test_login_credenciales_validas(driver, wait):
    """
    Verifica que al ingresar credenciales correctas,
    el sistema permite el acceso y muestra el nombre del usuario.

    NOTA: Requiere una cuenta registrada previamente con las
    credenciales definidas en el archivo .env
    """
    # 1. Navegar a la página de login
    ir_a_login(driver)
    print(f"\n🌐 Página cargada: {driver.current_url}")

    # 2. Llenar formulario con credenciales válidas y hacer click
    boton = llenar_formulario_login(wait, USER_VALIDO, PASS_VALIDO)
    print(f"📧 Email ingresado: {USER_VALIDO}")
    print("🔑 Contraseña ingresada: ******")
    
    boton.click()
    print("🖱️  Botón de login clickeado")

    # 3. VALIDACIÓN: Redirección al dashboard y mensaje de bienvenida (página principal)
    wait.until(EC.url_contains("dashboard"))
    
    # Validar que se muestre algún elemento de la página principal
    bienvenida = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'bienvenido')] | //*[contains(text(), 'Dashboard')]")
        )
    )
    assert bienvenida.is_displayed(), "❌ No se cargó correctamente la página principal"
    print("✅ PRUEBA PASÓ → Redirección a la página principal exitosa")
    
    # Opcional: imprimir la URL actual para depuración
    print(f"✅ PRUEBA PASÓ → Usuario logueado y página principal visible en: {driver.current_url}")

    # Cerrar sesión para no afectar los tests siguientes
    cerrar_sesion(driver)


# ──────────────────────────────────────────────
#  CASO 3: Login con campos vacíos
# ──────────────────────────────────────────────
def test_login_campos_vacios(driver, wait):
    """
    Verifica que al intentar hacer login sin llenar los campos,
    el formulario no se envía (validación HTML5 del navegador).
    """
    # 1. Navegar a la página de login
    ir_a_login(driver)
    print(f"\n🌐 Página cargada: {driver.current_url}")

    # 2. Asegurar que el campo esté vacío y hacer click en login
    encontrar(wait, "login_email").clear()
    # Click en login con campos vacíos
    boton = encontrar_clickable(wait, "login_button")
    driver.execute_script("arguments[0].click();", boton)
    print("🖱️  Botón de login clickeado con campos vacíos")

    # 3. VALIDACIÓN: La URL debe seguir siendo #/login
    assert "login" in driver.current_url, "❌ La página navegó fuera de #/login"
    print("✅ PRUEBA PASÓ → El formulario no se envió con campos vacíos")
