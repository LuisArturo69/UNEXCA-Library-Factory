from src.persistence.file_manager import JSONManager

# Ruta de nuestra "Base de Datos" JSON
DB_PATH = "data/inventario.json"

# Datos de prueba (Luego usaremos el Factory para esto)
datos_ejemplo = [
    {"id": 1, "tipo": "Libro", "nombre": "Cien años de soledad"},
    {"id": 2, "tipo": "Laptop", "marca": "Dell"}
]

# 1. Probamos guardar
print("Intentando guardar datos...")
if JSONManager.guardar_datos(DB_PATH, datos_ejemplo):
    print("✅ Datos guardados correctamente.")

# 2. Probamos cargar
print("Intentando leer datos...")
datos_leidos = JSONManager.cargar_datos(DB_PATH)
print(f"✅ Datos recuperados: {datos_leidos}")
