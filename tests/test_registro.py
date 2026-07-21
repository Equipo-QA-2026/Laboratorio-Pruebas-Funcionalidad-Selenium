"""
Pruebas funcionales de REGISTRO — SmartAdopt.

Estas pruebas verifican el comportamiento del formulario de registro
en la página #/register.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL, REGISTRO_NOMBRE, REGISTRO_PASS, USER_VALIDO
from tests.helpers import (
    ir_a_registro,
    encontrar,
    encontrar_clickable,
    encontrar_visible,
    llenar_formulario_registro_completo,
    generar_email_unico,
    eliminar_cuenta_prueba,
    cerrar_sesion
)


# ──────────────────────────────────────────────
#  CASO 1: Registro exitoso con datos completos
# ──────────────────────────────────────────────
def test_registro_exitoso(driver, wait):
    """
    Verifica el flujo completo de registro en #/register.
    """
    email_unico = generar_email_unico()

    # 1. Navegar a registro
    ir_a_registro(driver)
    print(f"\n🌐 Página cargada: {driver.current_url}")

    # 2. Llenar el formulario completo
    boton = llenar_formulario_registro_completo(
        wait, 
        REGISTRO_NOMBRE or "Selenium Test", 
        "Apellido", 
        email_unico, 
        "0999999999", 
        REGISTRO_PASS or "TestPassword2026!"
    )
    print(f"📝 Nombre ingresado: {REGISTRO_NOMBRE or 'Selenium Test'}")
    print(f"📧 Email ingresado: {email_unico}")
    print("🔑 Contraseña y demás datos llenados")
    
    # 3. Enviar el formulario
    driver.execute_script("arguments[0].click();", boton)
    print("🖱️  Botón 'Crear Cuenta' clickeado")

    # 4. VALIDACIÓN → Debe redirigir al login y mostrar éxito
    wait.until(EC.url_contains("login"))
    
    bienvenida = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cuenta creada')]")
        )
    )
    assert bienvenida.is_displayed(), "❌ No se mostró el mensaje de cuenta creada"
    print("✅ PRUEBA PASÓ → Cuenta creada exitosamente")

    # 5. Limpieza
    cerrar_sesion(driver)
    eliminar_cuenta_prueba(driver, wait)


# ──────────────────────────────────────────────
#  CASO 2: Registro con email ya existente
# ──────────────────────────────────────────────
def test_registro_email_existente(driver, wait):
    """
    Verifica que al intentar registrar un email que ya existe,
    el sistema muestra un error.
    """
    ir_a_registro(driver)
    print(f"\n🌐 Página cargada: {driver.current_url}")

    boton = llenar_formulario_registro_completo(
        wait, "Usuario Duplicado", "Test", USER_VALIDO, "0999999999", "TestP@ssword123!"
    )
    print(f"📧 Email ya existente ingresado: {USER_VALIDO}")
    driver.execute_script("arguments[0].click();", boton)
    print("🖱️  Botón de Registro clickeado")

    # VALIDACIÓN: Debe aparecer mensaje de error
    mensaje_error = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Email already registered')]")
        )
    )
    assert mensaje_error.is_displayed(), "❌ No se mostró el error de email duplicado"
    print(f"✅ PRUEBA PASÓ → Mensaje de error visible: '{mensaje_error.text}'")


# ──────────────────────────────────────────────
#  CASO 3: Registro con campos vacíos
# ──────────────────────────────────────────────
def test_registro_campos_vacios(driver, wait):
    """
    Verifica que al intentar hacer signup sin llenar nombre o email,
    el formulario no se envía (validación HTML5 del navegador).
    """
    ir_a_registro(driver)
    print(f"\n🌐 Página cargada: {driver.current_url}")

    encontrar(wait, "signup_name").clear()
    encontrar(wait, "signup_email").clear()

    # Click en Signup con campos vacíos
    boton = encontrar_clickable(wait, "signup_button")
    driver.execute_script("arguments[0].click();", boton)
    print("🖱️  Botón de Registro clickeado con campos vacíos")
    time.sleep(1)  # Breve espera para confirmar que no hubo redirección

    # VALIDACIÓN: Debe seguir en #/register
    assert "register" in driver.current_url, "❌ El formulario se envió con campos vacíos"
    print("✅ PRUEBA PASÓ → El formulario no se envió sin datos")
