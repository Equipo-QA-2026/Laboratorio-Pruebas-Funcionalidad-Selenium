# Configuración de variables de entorno en diccionario
def cargar_env(ruta=".env"):
    config = {}
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, valor = linea.split("=", 1)
            config[clave.strip()] = valor.strip().strip("\"'")
    return config

env = cargar_env()

# Variables de entorno
BASE_URL = env.get("BASE_URL")
USER_VALIDO = env.get("USER_VALIDO")
PASS_VALIDO = env.get("PASS_VALIDO")
USER_INVALIDO = env.get("USER_INVALIDO")
PASS_INVALIDO = env.get("PASS_INVALIDO")
