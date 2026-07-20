# Laboratorio de Pruebas Funcionales con Selenium

Pruebas funcionales automatizadas con **Selenium**, **Python** y **pytest**.
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
cd Laboratorio-Pruebas-Funcionalidad-Selenium
```

### 2. Crear el entorno virtual

```bash
python -m venv .venv
```

Activarlo:

```bash
# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate
```

> Si se activó correctamente vas a ver `(.venv)` al inicio de la línea de comandos.

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
| `USER_VALIDO`      | Email de un usuario que ya existe en el sitio   |
| `PASS_VALIDO`      | Contraseña de ese usuario                       |
| `USER_INVALIDO`    | Email de un usuario que no existe               |
| `PASS_INVALIDO`    | Contraseña incorrecta                           |
| `REGISTRO_NOMBRE`  | Nombre para registrar un usuario nuevo          |
| `REGISTRO_EMAIL`   | Email para el nuevo usuario (referencia)        |
| `REGISTRO_PASS`    | Contraseña para el nuevo usuario                |

> **Nota:** Para la prueba de registro exitoso se genera un email aleatorio automáticamente para evitar el error de "email ya existe".

---

## Cómo ejecutar las pruebas

### Ejecutar TODAS las pruebas (7 tests)
```bash
python main.py
```

### Ejecutar solo pruebas de LOGIN (3 tests)
```bash
python main.py login
```

### Ejecutar solo pruebas de REGISTRO (4 tests)
```bash
python main.py registro
```

### Ejecutar con pytest directamente
```bash
# Todas las pruebas con detalle
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
- Las capturas de pantalla se guardan automáticamente en `capturas/`
- El reporte HTML se genera en `reportes/reporte.html`

---

## Arquitectura del proyecto

```
Laboratorio-Pruebas-Funcionalidad-Selenium/
├── main.py              # Punto de entrada — ejecuta pytest con reportes
├── conftest.py          # Configuración central (variables .env + fixtures + capturas)
├── .env                 # Variables de entorno (no se sube al repo)
├── .env.example         # Plantilla para crear tu .env
├── .gitignore           # Archivos que git ignora
├── requirements.txt     # Dependencias del proyecto
├── capturas/            # Screenshots automáticos de cada test
├── reportes/            # Reportes HTML generados
└── tests/
    ├── __init__.py      # Marca tests/ como paquete de Python
    ├── helpers.py       # Funciones auxiliares (selectores + acciones)
    ├── test_login.py    # 3 pruebas de login
    └── test_registro.py # 4 pruebas de registro
```

### ¿Cómo interactúan los archivos?

```
                         ┌─────────────────────────────────────────────┐
  python main.py    ───► │  conftest.py                                │
                         │  ├── Lee variables del .env                 │
                         │  ├── Fixture driver (abre Chrome)           │
                         │  ├── Fixture wait (WebDriverWait de 10s)    │
                         │  └── Hook de capturas automáticas           │
                         └──────────────┬──────────────────────────────┘
                                        │ inyecta driver y wait
                         ┌──────────────▼──────────────────────────────┐
                         │  tests/                                     │
                         │  ├── helpers.py  (selectores + funciones)   │
                         │  ├── test_login.py      ← usa helpers.py   │
                         │  └── test_registro.py   ← usa helpers.py   │
                         └─────────────────────────────────────────────┘
```

| Archivo             | Rol                                                     |
|---------------------|---------------------------------------------------------|
| `conftest.py`       | Lee `.env`, configura Chrome, crea fixtures, toma capturas |
| `tests/helpers.py`  | Centraliza selectores CSS y funciones reutilizables     |
| `tests/test_login.py` | 3 pruebas del formulario de login                    |
| `tests/test_registro.py` | 4 pruebas del formulario de registro              |
| `main.py`           | Punto de entrada que ejecuta pytest y genera reportes   |

---

## Explicación detallada de cada archivo

---

### 📄 `conftest.py` — Configuración central

Este archivo tiene 3 responsabilidades:

#### 1. Carga de variables de entorno

Lee el archivo `.env` línea por línea y extrae las variables (URL, credenciales). Si el archivo no existe, muestra un error con instrucciones.

```python
# Función interna que lee el .env y devuelve un diccionario
_env = _cargar_env()

# Valida y exporta cada variable como constante
BASE_URL      = _validar(_env, "BASE_URL", "URL base de la aplicación")
USER_VALIDO   = _validar(_env, "USER_VALIDO", "Email de un usuario válido")
# ... etc
```

#### 2. Fixtures de pytest (inyección de dependencias)

Los **fixtures** son funciones que pytest inyecta automáticamente en los tests que los piden como parámetro.

```python
@pytest.fixture(scope="session")
def driver():
    # Abre Chrome maximizado y lo comparte entre TODOS los tests
    navegador = webdriver.Chrome(options=opciones)
    yield navegador        # ← entrega el navegador a los tests
    navegador.quit()       # ← cierra Chrome al terminar TODO

@pytest.fixture(scope="session")
def wait(driver):
    # Crea un WebDriverWait que espera hasta 10 segundos
    return WebDriverWait(driver, 10)
```

> **¿Cómo funciona?** Cuando un test declara `def test_algo(driver, wait):`, pytest automáticamente llama a estos fixtures y le pasa los objetos al test.

#### 3. Hook de capturas automáticas

Después de cada test (pase o falle), toma un screenshot y lo guarda en `capturas/`:

```
capturas/PASSED_test_login_credenciales_invalidas_121922.png
capturas/FAILED_test_login_credenciales_validas_121937.png
```

---

### 📄 `tests/helpers.py` — Funciones auxiliares

Centraliza toda la lógica repetida aplicando el concepto de **Page Object Model simplificado**.

#### Diccionario de selectores

Todos los selectores CSS están en un solo lugar. Si el sitio web cambia un atributo, solo se actualiza aquí:

```python
SELECTORES = {
    "login_email":    'input[data-qa="login-email"]',
    "login_password": 'input[data-qa="login-password"]',
    "login_button":   'button[data-qa="login-button"]',
    "signup_name":    'input[data-qa="signup-name"]',
    # ... etc
}
```

#### Funciones de localización (esperas explícitas)

Selenium necesita **esperar** a que los elementos aparezcan en la página antes de interactuar con ellos. Cada función usa un tipo de espera diferente:

| Función | Expected Condition | ¿Cuándo usarla? |
|---------|-------------------|------------------|
| `encontrar(wait, "login_email")` | `presence_of_element_located` | El elemento **existe** en el DOM |
| `encontrar_clickable(wait, "login_button")` | `element_to_be_clickable` | El elemento es **visible + habilitado** |
| `encontrar_visible(wait, "account_created")` | `visibility_of_element_located` | El elemento es **visible** en pantalla |

#### Funciones de formularios

| Función | ¿Qué hace? |
|---------|------------|
| `llenar_campo(wait, "login_email", "user@mail.com")` | Limpia el campo y escribe el texto |
| `llenar_formulario_login(wait, email, password)` | Llena email + password, retorna botón de login |
| `llenar_formulario_signup(wait, nombre, email)` | Llena nombre + email, retorna botón de signup |
| `llenar_formulario_registro_completo(driver, wait, password)` | Llena el formulario completo de /signup |

#### Funciones de navegación y limpieza

| Función | ¿Qué hace? |
|---------|------------|
| `ir_a_login(driver)` | Navega a `/login` |
| `cerrar_sesion(driver)` | Navega a `/logout` para cerrar sesión |
| `generar_email_unico()` | Genera un email aleatorio como `testuser_abc123@testmail.com` |
| `eliminar_cuenta_prueba(driver, wait)` | Elimina la cuenta de prueba en `/delete_account` |

---

## 🔐 Pruebas de Login — `tests/test_login.py`

Ejecutar solo estas pruebas: `python main.py login`

---

### Test 1: `test_login_credenciales_invalidas`

**Objetivo:** Verificar que el sistema rechaza credenciales incorrectas y muestra un mensaje de error.

**Flujo paso a paso:**

```
  1. ir_a_login(driver)                              → Navega a /login
  2. llenar_formulario_login(wait, email, password)   → Llena los campos con datos INVÁLIDOS
     ├── llenar_campo(wait, "login_email", email)     → Busca el input de email, lo limpia, escribe
     ├── llenar_campo(wait, "login_password", pass)   → Busca el input de password, lo limpia, escribe
     └── return encontrar_clickable("login_button")   → Retorna el botón listo para click
  3. boton.click()                                    → Hace click en "Login"
  4. wait.until(EC.visibility_of_element_located(...)) → Espera a que aparezca el mensaje de error
  5. assert mensaje_error.is_displayed()              → Verifica que el error sea visible
```

**Resultado esperado:** Aparece el texto _"Your email or password is incorrect!"_

---

### Test 2: `test_login_credenciales_validas`

**Objetivo:** Verificar que credenciales correctas permiten el acceso al sistema.

**Flujo paso a paso:**

```
  1. ir_a_login(driver)                              → Navega a /login
  2. llenar_formulario_login(wait, email, password)   → Llena los campos con datos VÁLIDOS del .env
     ├── llenar_campo(wait, "login_email", email)
     ├── llenar_campo(wait, "login_password", pass)
     └── return encontrar_clickable("login_button")
  3. boton.click()                                    → Hace click en "Login"
  4. wait.until(EC.visibility_of_element_located(...)) → Espera a que aparezca "Logged in as"
  5. assert logged_in.is_displayed()                  → Verifica que el usuario está logueado
  6. cerrar_sesion(driver)                            → Navega a /logout para limpiar la sesión
```

**Resultado esperado:** Aparece el texto _"Logged in as Bryan"_ en la barra de navegación.

---

### Test 3: `test_login_campos_vacios`

**Objetivo:** Verificar que el formulario no se envía sin datos (validación HTML5).

**Flujo paso a paso:**

```
  1. ir_a_login(driver)                       → Navega a /login
  2. encontrar(wait, "login_email").clear()    → Busca el campo de email y lo vacía
  3. encontrar_clickable("login_button").click() → Hace click en "Login" con campos vacíos
  4. assert "login" in driver.current_url     → Verifica que sigue en /login (no navegó)
```

**Resultado esperado:** La URL sigue siendo `/login` — el navegador bloquea el envío porque los campos `required` están vacíos.

---

## 📝 Pruebas de Registro — `tests/test_registro.py`

Ejecutar solo estas pruebas: `python main.py registro`

---

### Test 1: `test_registro_exitoso`

**Objetivo:** Verificar el flujo completo de registro de una cuenta nueva.

**Flujo paso a paso:**

```
  1. generar_email_unico()                           → Crea email aleatorio: testuser_x7k2m9@testmail.com
  2. ir_a_login(driver)                              → Navega a /login

  ── PASO 1: Sección de Signup en /login ──
  3. llenar_formulario_signup(wait, nombre, email)    → Llena nombre y email
     ├── llenar_campo(wait, "signup_name", nombre)
     ├── llenar_campo(wait, "signup_email", email)
     └── return encontrar_clickable("signup_button")
  4. boton.click()                                    → Click en "Signup" → redirige a /signup

  ── PASO 2: Formulario completo en /signup ──
  5. wait.until(EC.url_contains("signup"))            → Espera la redirección
  6. llenar_formulario_registro_completo(driver, wait, password)
     ├── encontrar(wait, "password").send_keys(...)   → Contraseña
     ├── find_element("first_name").send_keys(...)    → Nombre
     ├── find_element("last_name").send_keys(...)     → Apellido
     ├── find_element("address").send_keys(...)       → Dirección
     ├── Select("country").select_by_visible_text(...) → País (dropdown)
     ├── find_element("state").send_keys(...)         → Estado
     ├── find_element("city").send_keys(...)          → Ciudad
     ├── find_element("zipcode").send_keys(...)       → Código postal
     └── find_element("mobile_number").send_keys(...) → Teléfono

  ── PASO 3: Enviar y validar ──
  7. encontrar_clickable("create_account").click()    → Click en "Create Account"
  8. encontrar_visible(wait, "account_created")       → Espera mensaje de éxito
  9. assert cuenta_creada.is_displayed()              → Verifica "ACCOUNT CREATED!"

  ── PASO 4: Limpieza ──
  10. encontrar_clickable("continue_button").click()  → Click en "Continue"
  11. eliminar_cuenta_prueba(driver, wait)            → Navega a /delete_account y elimina la cuenta
```

**Resultado esperado:** Se muestra _"ACCOUNT CREATED!"_ y la cuenta se elimina al final para mantener el entorno limpio.

---

### Test 2: `test_registro_email_existente`

**Objetivo:** Verificar que no se puede registrar un email que ya tiene cuenta.

**Flujo paso a paso:**

```
  1. ir_a_login(driver)                              → Navega a /login
  2. llenar_formulario_signup(wait, nombre, email)    → Llena con email YA REGISTRADO (USER_VALIDO del .env)
     ├── llenar_campo(wait, "signup_name", "Usuario Duplicado")
     ├── llenar_campo(wait, "signup_email", USER_VALIDO)
     └── return encontrar_clickable("signup_button")
  3. boton.click()                                    → Click en "Signup"
  4. wait.until(EC.visibility_of_element_located(...)) → Espera mensaje de error
  5. assert mensaje_error.is_displayed()              → Verifica que aparece el error
```

**Resultado esperado:** Aparece _"Email Address already exist!"_

---

### Test 3: `test_registro_campos_vacios`

**Objetivo:** Verificar que el formulario de signup no se envía sin datos.

**Flujo paso a paso:**

```
  1. ir_a_login(driver)                          → Navega a /login
  2. encontrar(wait, "signup_name").clear()       → Vacía el campo nombre
  3. encontrar(wait, "signup_email").clear()      → Vacía el campo email
  4. encontrar_clickable("signup_button").click() → Click en "Signup" sin datos
  5. time.sleep(1)                               → Espera breve
  6. assert "login" in driver.current_url        → Verifica que sigue en /login
```

**Resultado esperado:** La URL sigue siendo `/login` — la validación HTML5 impide el envío.

---

### Test 4: `test_seccion_signup_visible`

**Objetivo:** Verificar que la sección de signup muestra todos sus elementos correctamente.

**Flujo paso a paso:**

```
  1. ir_a_login(driver)                              → Navega a /login
  2. encontrar(wait, "signup_name").is_displayed()    → ¿Campo nombre visible? ✅
  3. encontrar(wait, "signup_email").is_displayed()   → ¿Campo email visible? ✅
  4. encontrar(wait, "signup_button").is_displayed()  → ¿Botón signup visible? ✅
```

**Resultado esperado:** Los 3 elementos del formulario de signup están presentes y visibles en la página.

---

## Conceptos clave de Selenium demostrados

| Concepto | Dónde se usa | Descripción |
|----------|-------------|-------------|
| **WebDriver** | `conftest.py` | Controla el navegador Chrome programáticamente |
| **Esperas explícitas** | `helpers.py` | `WebDriverWait` + Expected Conditions — espera inteligente |
| **Selectores CSS** | `helpers.py` | Atributos `data-qa` para localizar elementos en el DOM |
| **Selectores XPath** | `test_login.py`, `test_registro.py` | Para buscar texto dentro de etiquetas HTML |
| **Select (dropdowns)** | `helpers.py` | Clase `Select` para interactuar con `<select>` de HTML |
| **Fixtures de pytest** | `conftest.py` | Inyección de dependencias automática |
| **Capturas de pantalla** | `conftest.py` | Hook que toma screenshot al terminar cada test |
| **Assertions** | Todos los tests | `assert` verifica que el resultado es el esperado |

---

## Cómo adaptar a otra aplicación web

### 1. Cambiar la URL
En el archivo `.env`, actualiza `BASE_URL` con la URL de tu aplicación.

### 2. Cambiar los selectores
Los selectores están centralizados en `tests/helpers.py` en el diccionario `SELECTORES`:

```python
# En tests/helpers.py — solo actualizar aquí
SELECTORES = {
    "login_email":    'input[data-qa="login-email"]',    # ← cambiar selector
    "login_password": 'input[data-qa="login-password"]',
    "login_button":   'button[data-qa="login-button"]',
    # ...
}
```

### 3. Cambiar los textos de validación
Actualiza los textos en los `assert` de cada test según los mensajes de tu aplicación.

---

## Qué hacer si una prueba falla

1. **Revisa la consola** → El mensaje de error indica qué paso falló
2. **Revisa las capturas** → `capturas/` tiene screenshots de cada test
3. **Revisa el reporte HTML** → `reportes/reporte.html`
4. **Verifica los selectores** → Inspecciona la página con F12
5. **Verifica el `.env`** → Asegúrate de que las credenciales son correctas
6. **Verifica Chrome/ChromeDriver** → Deben ser versiones compatibles