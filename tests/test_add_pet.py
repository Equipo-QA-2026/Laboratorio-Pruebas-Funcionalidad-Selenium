from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pytest
from config import BASE_URL, USER_VALIDO

def test_add_pet(driver_with_login):
    """Verifica el flujo completo de registro de una nueva mascota en la plataforma."""
    # Si el usuario logueado no es el admin, saltamos la prueba
    if USER_VALIDO != "admin@smartadopt.com":
        pytest.skip(f"El usuario {USER_VALIDO} no es administrador. Omitiendo prueba de registro de mascota.")

    driver = driver_with_login
    wait = WebDriverWait(driver, 10)
    
    # Navegar directamente a la ruta de creacion (el login ya ocurrio gracias al fixture)
    driver.get(f"{BASE_URL}#/admin/pets/new")
    time.sleep(2)  # Pausa para permitir que la Single Page Application cargue la vista
    print(f"Navegando a agregar nueva mascota... URL actual: {driver.current_url}")
    
    # Esperar hasta que el primer campo del formulario sea visible
    print("Esperando a que cargue el formulario...")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "nombre")))
    
    # 1. Seleccionar la especie usando el componente de seleccion de Material UI
    especie_select = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='especie']/preceding-sibling::div[@role='combobox']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", especie_select)
    time.sleep(0.5)
    especie_select.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@data-value='Perro']"))).click()
    print("Especie seleccionada.")
    
    # 2. Completar campos de texto basicos
    driver.find_element(By.CSS_SELECTOR, 'input[name="nombre"]').send_keys("Firulais")
    driver.find_element(By.CSS_SELECTOR, 'input[name="raza"]').send_keys("Mestizo")
    driver.find_element(By.CSS_SELECTOR, 'input[name="edad"]').send_keys("3")
    driver.find_element(By.CSS_SELECTOR, 'input[name="peso"]').send_keys("12.5")
    
    # 3. Seleccionar el genero
    genero_select = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='genero']/preceding-sibling::div[@role='combobox']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", genero_select)
    time.sleep(0.5)
    genero_select.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@role='option' and @data-value='Macho']"))).click()
    
    # 4. Completar ubicacion
    driver.find_element(By.CSS_SELECTOR, 'input[name="ubicacion"]').send_keys("Quito, Refugio Principal")
    
    # 5. Marcar casillas de estado de salud (uso de JS para saltar restricciones visuales de MUI)
    esterilizado_check = driver.find_element(By.CSS_SELECTOR, 'input[name="esterilizado"][type="checkbox"]')
    desparasitado_check = driver.find_element(By.CSS_SELECTOR, 'input[name="desparasitado"][type="checkbox"]')
    if not esterilizado_check.is_selected():
        driver.execute_script("arguments[0].click();", esterilizado_check)
    if not desparasitado_check.is_selected():
        driver.execute_script("arguments[0].click();", desparasitado_check)
        
    # 6. Marcar casillas dinamicas de vacunas
    vacunas = ["Rabia", "Parvovirus"]
    for vacuna in vacunas:
        xpath = f"//label[.//p[text()='{vacuna}']]//input[@type='checkbox']"
        check = driver.find_element(By.XPATH, xpath)
        if not check.is_selected():
            driver.execute_script("arguments[0].click();", check)
            
    # 7. Completar campos de texto finales
    driver.find_element(By.CSS_SELECTOR, 'input[name="condicionesEspeciales"]').send_keys("Ninguna, mascota sana")
    driver.find_element(By.CSS_SELECTOR, 'textarea[name="biografia"]').send_keys("Firulais es un perro rescatado muy alegre. Le encanta salir a pasear por el parque, correr y llevarse bien con los niños. Ideal para familia grande.")
    
    # 8. Cargar una imagen (busca un archivo real y si no existe usa uno temporal de prueba)
    print("Subiendo imagen...")
    imagen_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"][accept="image/*"]')
    firu_path = r"C:\Users\fabia\OneDrive\Imágenes\firu.jpg"
    dummy_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dummy.jpg")
    ruta_imagen = firu_path if os.path.exists(firu_path) else dummy_path
    
    imagen_input.send_keys(ruta_imagen)
    print("Datos llenados correctamente.")
    
    # 9. Enviar el formulario principal
    submit_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
    time.sleep(0.5)
    submit_btn.click()
    print("Boton Guardar clickeado.")
    
    # 10. Validacion final. Asegurar que aparece el mensaje de exito en pantalla.
    print("Esperando confirmacion del sistema...")
    wait_long = WebDriverWait(driver, 30)
    wait_long.until(EC.presence_of_element_located((By.XPATH, "//*[text()='¡Perfil Registrado con Éxito!']")))
    print("Prueba Exitosa: Se verifico la pantalla de confirmacion.")
    time.sleep(2)  # Pausa breve para capturar la imagen con la notificacion visible
