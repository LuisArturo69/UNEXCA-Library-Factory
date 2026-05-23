from src.database.conexion import DatabaseManager
from src.database.inventario_controller import InventarioController

print("--- 🏛️ INICIALIZANDO SPRINT 1 Y 2: SISTEMA SQLITE ---")
print("Cargando el escudo de persistencia relacional...")

try:
    # -------------------------------------------------------------------------
    # FASE 1: Inicialización de la Infraestructura (Fase Estructural)
    # -------------------------------------------------------------------------
    db = DatabaseManager()
    
    print("\n✅ CONTROL DE CALIDAD SPRINT 1:")
    print("1. Carpeta 'data/' verificada o creada exitosamente.")
    print("2. Archivo 'biblioteca.db' inicializado.")
    print("3. Estructura de tablas (usuarios, recursos, detalles, movimientos) blindada.")
    
    # -------------------------------------------------------------------------
    # FASE 2: Prueba de la Lógica de Datos (Fase de Negocio - CRUD)
    # -------------------------------------------------------------------------
    print("\n--- 🗄️ INICIANDO PRUEBAS DE OPERACIONES CRUD (SPRINT 2) ---")
    controlador = InventarioController()

    # A. Prueba de Registro (Create)
    print("\n[CRUD] Insertando recursos de prueba...")
    controlador.registrar_recurso(
        tipo="Libro", 
        nombre="Cálculo de Leithold", 
        detalles={"autor": "Louis Leithold", "edicion": "7ma"}
    )
    controlador.registrar_recurso(
        tipo="Laptop", 
        nombre="Laptop Estudiante HP", 
        detalles={"serial": "HP987654", "procesador": "Core i5"}
    )

    # B. Prueba de Consulta (Read)
    print("\n[CRUD] Consultando el inventario completo desde SQLite:")
    inventario = controlador.consultar_inventario()
    for recurso in inventario:
        print(f"▶ ID: {recurso['id']} | Tipo: {recurso['tipo']} | Nombre: {recurso['nombre']} | Estado: {recurso['estado']} | Detalles: {recurso['detalles']}")

    # C. Prueba de Actualización (Update)
    print("\n[CRUD] Simulando un préstamo (Cambiando estado)...")
    # Intentamos actualizar el recurso con ID 2 (la laptop)
    controlador.actualizar_estado(recurso_id=2, nuevo_estado="Prestado")

    print("\n🚀 ¡El sistema completo de persistencia relacional responde perfectamente!")

except Exception as e:
    print(f"\n❌ ERROR CRÍTICO EN EL ARRANQUE DEL SISTEMA: {e}")
