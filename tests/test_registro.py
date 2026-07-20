"""
Pruebas funcionales de REGISTRO — Automation Exercise.

Estas pruebas verifican el comportamiento del formulario de registro
en cuatro escenarios distintos:

  Caso 1: Registro exitoso          → flujo completo hasta "ACCOUNT CREATED!"
  Caso 2: Email ya existente        → debe mostrar "Email Address already exist!"
  Caso 3: Campos vacíos             → no debe enviar el formulario
  Caso 4: Sección Signup visible    → elementos del formulario presentes

El flujo de registro en Automation Exercise tiene 2 pasos:
  Paso 1: En /login → llenar nombre y email → click "Signup"
  Paso 2: En /signup → llenar formulario completo → click "Create Account"
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL, REGISTRO_NOMBRE, REGISTRO_PASS, USER_VALIDO
from tests.helpers import (
    ir_a_login,
    encontrar,
    encontrar_clickable,
    encontrar_visible,
    llenar_formulario_signup,
    llenar_formulario_registro_completo,
    generar_email_unico,
    eliminar_cuenta_prueba,
)


# ──────────────────────────────────────────────
#  CASO 1: Registro exitoso con datos completos
# ──────────────────────────────────────────────
def test_registro_exitoso(driver, wait):
    """
    Verifica el flujo completo de registro:
    1. Ingresar nombre y email en /login (sección Signup)
    2. Llenar el formulario completo en /signup
    3. Verificar que se muestra 'Account Created!'
    4. Limpiar: eliminar la cuenta creada
    """
    email_unico = generar_email_unico()

    # ── PASO 1: Ir a /login y llenar la sección de Signup ──
    ir_a_login(driver)
    print(f"\n🌐 Página cargada: {driver.current_url}")

    boton = llenar_formulario_signup(wait, REGISTRO_NOMBRE or "Usuario Test", email_unico)
    print(f"📝 Nombre ingresado: {REGISTRO_NOMBRE or 'Usuario Test'}")
    print(f"📧 Email ingresado: {email_unico}")
    boton.click()
    print("🖱️  Botón de Signup clickeado")

    # ── PASO 2: Llenar el formulario completo de registro ──
    wait.until(EC.url_contains("signup"))
    print(f"📄 Redirigido a: {driver.current_url}")

    llenar_formulario_registro_completo(driver, wait, REGISTRO_PASS or "Test@12345")
    print("🔑 Contraseña ingresada: ******")
    print("📋 Datos personales ingresados")
    print("📍 Dirección ingresada")

    # ── PASO 3: Enviar el formulario ──
    encontrar_clickable(wait, "create_account").click()
    print("🖱️  Botón 'Create Account' clickeado")

    # ── PASO 4: VALIDACIÓN → Debe aparecer "ACCOUNT CREATED!" ──
    cuenta_creada = encontrar_visible(wait, "account_created")
    assert cuenta_creada.is_displayed(), "❌ No se mostró el mensaje de cuenta creada"
    print("✅ PRUEBA PASÓ → Cuenta creada exitosamente")

    # ── PASO 5: Limpiar la cuenta de prueba ──
    encontrar_clickable(wait, "continue_button").click()
    eliminar_cuenta_prueba(driver, wait)


# ──────────────────────────────────────────────
#  CASO 2: Registro con email ya existente
# ──────────────────────────────────────────────
def test_registro_email_existente(driver, wait):
    """
    Verifica que al intentar registrar un email que ya existe,
    el sistema muestra el mensaje 'Email Address already exist!'.

    Usa USER_VALIDO del .env (cuenta ya registrada).
    """
    # 1. Ir a /login e intentar signup con email ya registrado
    ir_a_login(driver)
    print(f"\n🌐 Página cargada: {driver.current_url}")

    boton = llenar_formulario_signup(wait, "Usuario Duplicado", USER_VALIDO)
    print(f"📧 Email ya existente ingresado: {USER_VALIDO}")
    boton.click()
    print("🖱️  Botón de Signup clickeado")

    # 2. VALIDACIÓN: Debe aparecer "Email Address already exist!"
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
def test_registro_campos_vacios(driver, wait):
    """
    Verifica que al intentar hacer signup sin llenar nombre o email,
    el formulario no se envía (validación HTML5 del navegador).
    """
    # 1. Ir a /login y asegurar campos vacíos
    ir_a_login(driver)
    print(f"\n🌐 Página cargada: {driver.current_url}")

    encontrar(wait, "signup_name").clear()
    encontrar(wait, "signup_email").clear()

    # 2. Click en Signup con campos vacíos
    encontrar_clickable(wait, "signup_button").click()
    print("🖱️  Botón de Signup clickeado con campos vacíos")
    time.sleep(1)  # Breve espera para confirmar que no hubo redirección

    # 3. VALIDACIÓN: Debe seguir en /login
    assert "login" in driver.current_url, "❌ El formulario se envió con campos vacíos"
    print("✅ PRUEBA PASÓ → El formulario no se envió sin datos")


# ──────────────────────────────────────────────
#  CASO 4: Verificar sección de Signup visible
# ──────────────────────────────────────────────
def test_seccion_signup_visible(driver, wait):
    """
    Verifica que la página de login muestra correctamente
    la sección de 'New User Signup!' con todos sus elementos.
    """
    # 1. Ir a /login
    ir_a_login(driver)
    print(f"\n🌐 Página cargada: {driver.current_url}")

    # 2. VALIDACIÓN: Verificar que los elementos de signup están presentes
    assert encontrar(wait, "signup_name").is_displayed(), "❌ Campo nombre no visible"
    assert encontrar(wait, "signup_email").is_displayed(), "❌ Campo email no visible"
    assert encontrar(wait, "signup_button").is_displayed(), "❌ Botón signup no visible"
    print("✅ PRUEBA PASÓ → Todos los elementos de Signup están visibles")
