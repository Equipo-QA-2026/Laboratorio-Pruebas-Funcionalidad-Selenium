# LAB-PRUEBAS-SELENIUM

Pruebas automatizadas con Selenium y Python.

---

## Requisitos

- Python 3.11 o superior
- Google Chrome instalado
- [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/) compatible con tu versión de Chrome

---

## Instalación paso a paso

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd LAB-PRUEBAS-SELENIUM
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

Activarlo:

```bash
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

> Si se activó correctamente vas a ver `(venv)` al inicio de la línea de comandos.

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Copiar el archivo de ejemplo:

```bash
# Windows
copy .env.example .env

# Linux / Mac
cp .env.example .env
```

Abrir el archivo `.env` y completar con tus datos:

```
BASE_URL=http://localhost:5173/
USER_VALIDO=admin@tuapp.com
PASS_VALIDO=tu_contraseña
USER_INVALIDO=usuario_falso@tuapp.com
PASS_INVALIDO=contraseña_falsa
```

| Variable       | Descripción                          |
|----------------|--------------------------------------|
| `BASE_URL`     | URL base de la aplicación a probar   |
| `USER_VALIDO`  | Email de un usuario que existe       |
| `PASS_VALIDO`  | Contraseña de ese usuario            |
| `USER_INVALIDO`| Email de un usuario que no existe    |
| `PASS_INVALIDO`| Contraseña incorrecta                |

---

## Ejecutar las pruebas

```bash
python main.py
```

Esto va a:
1. Abrir Chrome automáticamente
2. Ir a la página de login
3. Probar primero con credenciales inválidas
4. Probar después con credenciales válidas
5. Cerrar el navegador

---

## Qué modificar para agregar una nueva prueba

### Paso 1: Crear el archivo de test

Crear un archivo nuevo dentro de `tests/`, por ejemplo `test_registro.py`:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import BASE_URL

def registro(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(f"{BASE_URL}#/registro")
    print(f"Página cargada: {driver.title}")

    # Acá van los pasos de la prueba
    input_nombre = wait.until(EC.presence_of_element_located((By.NAME, "nombre")))
    input_nombre.send_keys("Juan")
    # ...
```

### Paso 2: Importar la función en main.py

Abrir `main.py` y agregar la importación:

```python
from tests.test_registro import registro
```

Llamarla dentro de `main()`:

```python
def main():
    driver = inicializar_driver()
    try:
        registro(driver)    # <-- agregar esto
        time.sleep(2)
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        driver.quit()
```

### Paso 3: Ejecutar

```bash
python main.py
```

---

## Estructura del proyecto

```
LAB-PRUEBAS-SELENIUM/
├── main.py              # Punto de entrada, ejecuta las pruebas
├── config.py            # Lee las variables del .env
├── .env                 # Variables de entorno (no se sube al repo)
├── .env.example         # Plantilla para crear tu .env
├── .gitignore           # Archivos que git ignora
├── requirements.txt     # Dependencias del proyecto
└── tests/
    └── test_login.py    # Pruebas de login
```

---

## Archivos importantes

| Archivo        | Para qué sirve                                     |
|----------------|----------------------------------------------------|
| `.env`         | Guardar URL y credenciales (nunca subir al repo)   |
| `.env.example` | Plantilla para que otros sepan qué variables usar  |
| `config.py`    | Lee el `.env` y expone las variables como constantes|
| `main.py`      | Punto de entrada, inicializa Chrome y corre los tests|
| `requirements.txt` | Lista de paquetes que necesita el proyecto     |
