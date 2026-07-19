# LAB-PRUEBAS-SELENIUM

Pruebas funcionales automatizadas con Selenium, Python y pytest.
Configurado para probar [Automation Exercise](https://automationexercise.com/), pero adaptable a cualquier aplicación web.

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
BASE_URL=https://automationexercise.com/
USER_VALIDO=tu_email@ejemplo.com
PASS_VALIDO=tu_contraseña
USER_INVALIDO=noexiste@fake.com
PASS_INVALIDO=contraseña_falsa
REGISTRO_NOMBRE=Test Usuario
REGISTRO_EMAIL=nuevo_usuario@test.com
REGISTRO_PASS=Password123
```

| Variable           | Descripción                                     |
|--------------------|-------------------------------------------------|
| `BASE_URL`         | URL base de la aplicación a probar              |
| `USER_VALIDO`      | Email de un usuario que existe                  |
| `PASS_VALIDO`      | Contraseña de ese usuario                       |
| `USER_INVALIDO`    | Email de un usuario que no existe               |
| `PASS_INVALIDO`    | Contraseña incorrecta                           |
| `REGISTRO_NOMBRE`  | Nombre para registrar un usuario nuevo          |
| `REGISTRO_EMAIL`   | Email para el nuevo usuario (referencia)        |
| `REGISTRO_PASS`    | Contraseña para el nuevo usuario                |

> **Nota:** Para la prueba de registro exitoso se genera un email aleatorio automáticamente para evitar el error de "email ya existe". Las variables `REGISTRO_*` se usan como datos base.

---

## Ejecutar las pruebas

### Ejecutar TODAS las pruebas
```bash
python main.py
```

### Ejecutar solo pruebas de LOGIN
```bash
python main.py login
```

### Ejecutar solo pruebas de REGISTRO
```bash
python main.py registro
```

### Ejecutar con pytest directamente
```bash
# Todas las pruebas con verbose
pytest tests/ -v -s

# Solo un archivo
pytest tests/test_login.py -v -s

# Solo un caso específico
pytest tests/test_login.py::test_login_credenciales_invalidas -v -s

# Generar reporte HTML
pytest tests/ --html=reportes/reporte.html --self-contained-html -v
```

### Resultados

- En consola verás el detalle de cada prueba con ✅ o ❌
- El reporte HTML se genera en `reportes/reporte.html`
- Abre el reporte en tu navegador para ver un resumen visual

---

## Pruebas incluidas

### 🔐 Test de Login (`tests/test_login.py`)

| Caso | Descripción | Validación |
|------|-------------|------------|
| `test_login_credenciales_invalidas` | Login con email/contraseña incorrectos | Aparece mensaje "Your email or password is incorrect!" |
| `test_login_credenciales_validas` | Login con credenciales correctas | Aparece "Logged in as [usuario]" en la navbar |
| `test_login_campos_vacios` | Click en login sin llenar campos | La página permanece en /login |

### 📝 Test de Registro (`tests/test_registro.py`)

| Caso | Descripción | Validación |
|------|-------------|------------|
| `test_registro_exitoso` | Flujo completo de registro con datos válidos | Aparece "ACCOUNT CREATED!" y se elimina la cuenta |
| `test_registro_email_existente` | Registro con email ya registrado | Aparece "Email Address already exist!" |
| `test_registro_campos_vacios` | Click en signup sin datos | La página permanece en /login |
| `test_seccion_signup_visible` | Verificar que el formulario de signup existe | Campos y botón de signup están visibles |

---

## Estructura del proyecto

```
LAB-PRUEBAS-SELENIUM/
├── main.py              # Punto de entrada, ejecuta pytest con reportes
├── config.py            # Lee y valida las variables del .env
├── conftest.py          # Fixtures de pytest (driver de Chrome compartido)
├── .env                 # Variables de entorno (no se sube al repo)
├── .env.example         # Plantilla para crear tu .env
├── .gitignore           # Archivos que git ignora
├── requirements.txt     # Dependencias del proyecto
├── reportes/            # Reportes HTML generados (no se sube al repo)
└── tests/
    ├── __init__.py      # Marca tests/ como paquete de Python
    ├── test_login.py    # 3 pruebas de login
    └── test_registro.py # 4 pruebas de registro
```

---

## Cómo adaptar a otra aplicación web

### 1. Cambiar la URL
En el archivo `.env`, actualiza `BASE_URL` con la URL de tu aplicación.

### 2. Cambiar los selectores
Cada archivo de test tiene documentados los selectores CSS que usa. Para adaptarlos:

```python
# ANTES (Automation Exercise usa data-qa):
input_email = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-qa="login-email"]'))
)

# DESPUÉS (tu app puede usar name, id, class, etc.):
input_email = wait.until(
    EC.presence_of_element_located((By.NAME, "email"))
    # o (By.ID, "email-input")
    # o (By.CSS_SELECTOR, ".login-form input[type='email']")
    # o (By.XPATH, "//input[@placeholder='Correo electrónico']")
)
```

### 3. Cambiar los textos de validación
Actualiza los textos que se buscan en los asserts según los mensajes de tu aplicación.

---

## Qué hacer si una prueba falla

1. **Revisa la consola** → El mensaje de error indica qué paso falló
2. **Revisa el reporte HTML** → `reportes/reporte.html` tiene capturas y detalles
3. **Verifica los selectores** → Inspecciona la página con F12 y confirma que los selectores coinciden
4. **Verifica el `.env`** → Asegúrate de que las credenciales son correctas
5. **Verifica Chrome/ChromeDriver** → Deben ser versiones compatibles

---

## Archivos importantes

| Archivo             | Para qué sirve                                          |
|---------------------|---------------------------------------------------------|
| `.env`              | Guardar URL y credenciales (nunca subir al repo)        |
| `.env.example`      | Plantilla para que otros sepan qué variables usar       |
| `config.py`         | Lee el `.env` y valida las variables como constantes    |
| `conftest.py`       | Configura el navegador Chrome como fixture de pytest    |
| `main.py`           | Punto de entrada, ejecuta pytest y genera reportes      |
| `requirements.txt`  | Lista de paquetes que necesita el proyecto               |