"""
Punto de entrada del Laboratorio de Pruebas Funcionales con Selenium.

Ejecuta todas las pruebas usando pytest y genera un reporte HTML.

Modos de ejecución:
    python main.py                  → Ejecutar TODAS las pruebas
    python main.py login            → Solo pruebas de login
    python main.py registro         → Solo pruebas de registro

El reporte HTML se genera en: reportes/reporte.html
"""

import sys
import os
import pytest


def main():
    # Crear la carpeta de reportes si no existe
    os.makedirs("reportes", exist_ok=True)

    # Argumentos base de pytest
    args = [
        "-v",                                           # Modo verbose (detalle de cada test)
        "--tb=short",                                   # Tracebacks cortos para errores
        f"--html=reportes/reporte.html",                # Reporte HTML
        "--self-contained-html",                        # HTML autocontenido (sin archivos externos)
        "-s",                                           # Mostrar prints en consola
    ]

    # Selección de pruebas por argumento de línea de comandos
    if len(sys.argv) > 1:
        modulo = sys.argv[1].lower()
        if modulo == "login":
            args.append("tests/test_login.py")
            print("🔐 Ejecutando solo pruebas de LOGIN...")
        elif modulo == "registro":
            args.append("tests/test_registro.py")
            print("📝 Ejecutando solo pruebas de REGISTRO...")
        else:
            print(f"⚠️  Módulo '{modulo}' no reconocido.")
            print("   Opciones válidas: login, registro")
            print("   Sin argumento ejecuta todas las pruebas.")
            sys.exit(1)
    else:
        args.append("tests/")
        print("🚀 Ejecutando TODAS las pruebas...")

    print("=" * 60)

    # Ejecutar pytest
    codigo_salida = pytest.main(args)

    print("=" * 60)
    if codigo_salida == 0:
        print("✅ Todas las pruebas pasaron correctamente")
    else:
        print("❌ Algunas pruebas fallaron")
    print(f"📊 Reporte generado en: reportes/reporte.html")

    sys.exit(codigo_salida)


if __name__ == "__main__":
    main()
