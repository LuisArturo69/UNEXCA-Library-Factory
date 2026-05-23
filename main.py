from src.database.conexion import DatabaseManager

print("--- 🏛️ INICIALIZANDO SPRINT 1: BASE DE DATOS SQLITE ---")
print("Cargando el escudo de persistencia relacional...")

try:
    # Al instanciar la clase, se verifica la carpeta 'data', 
    # se crea el archivo 'biblioteca.db' y se construyen las 4 tablas.
    db = DatabaseManager()
    
    print("\n✅ CONTROL DE CALIDAD SPRINT 1:")
    print("1. Carpeta 'data/' verificada o creada exitosamente.")
    print("2. Archivo 'biblioteca.db' inicializado.")
    # Usamos un menor que literal en texto por seguridad del parser
    print("3. Estructura de tablas (usuarios, recursos, detalles, movimientos) blindada.")
    print("\n🚀 ¡El sistema está listo para la lógica de negocio del Sprint 2!")

except Exception as e:
    print(f"\n❌ ERROR CRÍTICO EN EL ARRANQUE DEL SISTEMA: {e}")
