# LAB-PRUEBAS-SELENIUM

Pruebas automatizadas con Selenium y Python, utilizando el framework **Pytest**.

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

```env
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

El proyecto está configurado con **Pytest**. Para correr las pruebas y generar las evidencias automáticamente, ejecuta en la raíz del proyecto:

```bash
pytest
```

### ¿Qué sucederá al ejecutar?
1. Se abrirá una ventana de Chrome para cada prueba de forma independiente.
2. `test_login` se ejecutará dos veces: una con datos incorrectos y otra con correctos.
3. `test_add_pet` se ejecutará haciendo uso de un inicio de sesión previo automatizado en segundo plano.
4. Al finalizar, si una prueba es exitosa, se guardará una captura de pantalla en `evidencias/exitosas/`.
5. Si una prueba falla, se guardará una captura de pantalla y el código HTML de la página en `evidencias/fallidas/`.
6. Se generará un archivo `reporte.html` dentro de `evidencias/` con el resumen de la ejecución.

### Ejecutar una sola prueba
Si deseas correr un solo archivo, por ejemplo, solo el test de login:
```bash
pytest tests/test_login.py
```

---

## Qué modificar para agregar una nueva prueba

### Paso 1: Crear el archivo de test

Crear un archivo nuevo dentro de `tests/`, por ejemplo `test_registro.py`. Asegúrate de que el nombre del archivo empiece con `test_`:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import BASE_URL

# Si tu prueba requiere login previo, inyecta 'driver_with_login'
# Si no requiere login, inyecta simplemente 'driver'
def test_registro(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(f"{BASE_URL}#/registro")
    print(f"Página cargada: {driver.title}")

    # Acá van los pasos de la prueba
    input_nombre = wait.until(EC.presence_of_element_located((By.NAME, "nombre")))
    input_nombre.send_keys("Juan")
    # ...
```

### Paso 2: Ejecutar

Pytest detectará tu nuevo archivo automáticamente. Simplemente corre:

```bash
pytest
```

---

## Estructura del proyecto

```text
LAB-PRUEBAS-SELENIUM/
├── config.py            # Lee las variables del .env
├── .env                 # Variables de entorno (no se sube al repo)
├── .env.example         # Plantilla para crear tu .env
├── .gitignore           # Archivos que git ignora
├── pytest.ini           # Configuración base de Pytest y reportes
├── requirements.txt     # Dependencias del proyecto
├── evidencias/          # (Autogenerada) Aquí se guardan reportes y capturas
└── tests/
    ├── conftest.py      # Fixtures de configuración y captura de evidencias
    ├── test_login.py    # Pruebas de login (parametrizadas)
    └── test_add_pet.py  # Prueba de agregar mascota (con login implícito)
```

---

## Archivos importantes

| Archivo        | Para qué sirve                                     |
|----------------|----------------------------------------------------|
| `.env`         | Guardar URL y credenciales (nunca subir al repo)   |
| `config.py`    | Lee el `.env` y expone las variables como constantes|
| `pytest.ini`   | Configuración para comandos y reportes de pytest   |
| `conftest.py`  | Contiene funciones (fixtures) que se ejecutan antes y después de cada prueba|
| `requirements.txt` | Lista de paquetes que necesita el proyecto     |