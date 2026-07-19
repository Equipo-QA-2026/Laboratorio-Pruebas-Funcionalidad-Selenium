import os
import sys

# Configuración de variables de entorno en diccionario
def cargar_env(ruta=".env"):
    """
    Carga las variables de entorno desde un archivo .env.
    Retorna un diccionario con las claves y valores encontrados.
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


def validar_variable(env, nombre, descripcion):
    """
    Valida que una variable de entorno exista y no esté vacía.
    Muestra un mensaje de error claro si falta.
    """
    valor = env.get(nombre)
    if not valor or valor.startswith("dato de") or valor.startswith("url del"):
        print(f"⚠️  Variable '{nombre}' no configurada → {descripcion}")
        print(f"   Abre el archivo .env y completa el valor de {nombre}")
        return None
    return valor


env = cargar_env()

# --- Variables de entorno para LOGIN ---
BASE_URL = validar_variable(env, "BASE_URL", "URL base de la aplicación a probar")
USER_VALIDO = validar_variable(env, "USER_VALIDO", "Email de un usuario válido")
PASS_VALIDO = validar_variable(env, "PASS_VALIDO", "Contraseña de un usuario válido")
USER_INVALIDO = validar_variable(env, "USER_INVALIDO", "Email de un usuario inválido")
PASS_INVALIDO = validar_variable(env, "PASS_INVALIDO", "Contraseña inválida")

# --- Variables de entorno para REGISTRO ---
REGISTRO_NOMBRE = validar_variable(env, "REGISTRO_NOMBRE", "Nombre para registrar un usuario nuevo")
REGISTRO_EMAIL = validar_variable(env, "REGISTRO_EMAIL", "Email para registrar un usuario nuevo")
REGISTRO_PASS = validar_variable(env, "REGISTRO_PASS", "Contraseña para el nuevo usuario")
