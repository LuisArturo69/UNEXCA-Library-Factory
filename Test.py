"""
SISTEMA DE VALIDACIÓN DE USUARIO Y CONTRASEÑA DESDE ARCHIVO JSON
"""

import json
import sys

# CONSTANTES GLOBALES

user_file = "users_developers.json"


default_users = {           # Usuarios por defecto (se usan si el archivo no existe)
    "dgodoy": "DeninG2026",
    "jniño": "JoseN2026",
    "yvalero": "YuseilyV2026",
    "mnoriega": "ManuelN2026",
    "lsilva": "LuisS2026",
    "mtellez": "ManuelT2026"
}

# FUNCIONES DE GESTIÓN DE USUARIOS

def load_or_create_users(): # Función para cargar usuarios desde el 
    try:                    # archivo JSON o crear el archivo con usuarios por defecto
        with open(user_file, "r") as archivo:
            usuarios = json.load(archivo)
            print(" Archivo de usuarios cargado correctamente.")
            return usuarios
            
    except FileNotFoundError:
        with open(user_file, "w") as archivo: # El archivo no existe, lo creamos con los usuarios por defecto
            json.dump(default_users, archivo, indent=4)
        print(" Archivo de usuarios creado con los usuarios por defecto.")
        return default_users
    
    except json.JSONDecodeError:
        print(" Error: El archivo JSON tiene formato inválido.")
        print("   Usando usuarios por defecto temporalmente.")
        return default_users


def validate_user(): # Función para validar usuario y contraseña
    """
    Función principal que valida usuario y contraseña.
    Solicita las credenciales una sola vez por intento.
    Permite reintentos hasta que el usuario decida salir.
    """
    # Cargar los usuarios
    user = load_or_create_users()
    
    while True:
        
        print("\n" + "=" * 50)
        print("         INICIO DE SESIÓN")
        print("=" * 50)
        print("(Escriba 'salir' como usuario para terminar)\n")
        
        # ========== SOLICITAR USUARIO (UNA SOLA VEZ) ==========
        usuario = input(" Usuario: ").strip()
        
        if usuario.lower() == "salir": #Condición para salir del programa.
            print("\n Saliendo del programa...")
            return False
        
        if not usuario: # Validación que el usuario no esté vacío
            print("\n Error: El usuario no puede estar vacío.")
            input("\nPresione Enter para continuar...")
            continue
        
        # ========== SOLICITAR CONTRASEÑA (UNA SOLA VEZ) ==========
        password = input(" Contraseña: ").strip()
        
        if not password: # Validar que la contraseña no esté vacía
            print("\n Error: La contraseña no puede estar vacía.")
            input("\nPresione Enter para continuar...")
            continue
        
        # ========== VERIFICAR CREDENCIALES ==========
        if usuario in user and user[usuario] == password:
            print("\n" + "*" * 20)
            print(f" ¡ACCESO CONCEDIDO!")
            print(f" Bienvenido/a, {usuario}")
            print(" " * 20)
            return True
        else:
            print("\n Usuario o contraseña " \
            "INCORRECTOS.")
            
            while True:
                reintentar = input("\n¿Desea intentar de nuevo? (s/n): ").strip().lower()
                if reintentar in ("s", "n", "si", "no"):
                    if reintentar in ("s", "si"):
                        break  
                    else:
                        print("\n Saliendo del programa...")
                        return False
                else:
                    print(" Respuesta inválida. Escriba 's' para sí o 'n' para no.")


# ========================================================================
# PROGRAMA PRINCIPAL
# ========================================================================

def main():
    """Función principal del programa"""
    print("\n" + "" * 25)
    print("     BIENVENIDO AL SISTEMA DE VALIDACIÓN")
    print("" * 25)
    
    # Pausa opcional
    input("\nPresione Enter para continuar...")
    
    if validate_user(): # Ejecutar validación
        print("\n" + "-" * 50)
        print(" ACCESO AL SISTEMA PRINCIPAL")
        print("-" * 50)
        print(" Ha iniciado sesión correctamente.")
        print(" Puede acceder a las funciones del sistema.\n")
        
        # ========== Menú principal en desarrollo ==========
        print(" Menú principal:")
        print("   1. Observar el inventario")
        print("   2. Solicitar un prestamo")
        print("   3. Cerrar sesión")
        # =====================================================
        
    else:
        print("\n Acceso denegado. El programa finalizará.")

# Función para ejecutar el programa principal
if __name__ == "__main__":
    main() 
