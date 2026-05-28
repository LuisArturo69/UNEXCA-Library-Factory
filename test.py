from src.factory.resources import resource_factory
from src.database.conexion import DatabaseManager
from src.database.inventario_controller import InventarioController

def inicializar_sistema():
    """Inicializa la infraestructura de la base de datos de los Sprints 1 y 2."""
    print("---  INICIALIZANDO SISTEMA UNEXCA-LIBRARY-FACTORY ---")
    print("Cargando el escudo de persistencia relacional...")
    try:
        # Fase Estructural
        db = DatabaseManager()
        controlador = InventarioController()
        
        print("\n CONTROL DE CALIDAD SPRINT 1 Y 2:")
        print("1. Carpeta 'data/' y archivo 'biblioteca.db' verificados.")
        print("2. Estructura de tablas blindada.")
        print("3. Controlador de inventario en línea.\n")
        return controlador
    except Exception as e:
        print(f"\n ERROR CRÍTICO EN EL ARRANQUE DEL SISTEMA: {e}")
        return None

def main():
    controlador = inicializar_sistema()
    if not controlador:
        return

    # Lista temporal en memoria (opcional, si deseas mantener sincronización con Factory)
    inventory = []

    while True:
        print("\n" + "="*40)
        print(" GESTOR DE RECURSOS Y FACTORY")
        print("="*40)
        print("1. Crear un Libro")
        print("2. Crear una Laptop")
        print("3. Crear una Tablet")
        print("4. Mostrar Inventario de la Base de Datos")
        print("5. Registrar Préstamo de Recurso")
        print("6. Salir")
        print("="*40)
        
        opcion = input("Elige una opción (1-6): ")

        try:
            if opcion == '1':
                t = input(" Ingresa el título del libro: ")
                a = input(" Ingresa el nombre del autor: ")
                
                # 1. Instanciamos el objeto usando el patrón Factory
                nuevo_recurso = resource_factory.crear_recurso('book', titulo=t, autor=a)
                inventory.append(nuevo_recurso)
                
                # 2. Guardamos en la base de datos usando el Controlador (Sprint 2)
                controlador.registrar_recurso(
                    tipo="Libro", 
                    nombre=t, 
                    detalles={"autor": a, "id_factory": nuevo_recurso.id_producto}
                )
                print(f" ¡Libro guardado exitosamente en DB!")

            elif opcion == '2':
                m = input(" Ingresa la marca de la laptop: ")
                r = input(" Ingresa la cantidad de RAM (ej. 8GB): ")
                
                nuevo_recurso = resource_factory.crear_recurso('laptop', marca=m, ram=r)
                inventory.append(nuevo_recurso)
                
                controlador.registrar_recurso(
                    tipo="Laptop", 
                    nombre=f"Laptop {m}", 
                    detalles={"marca": m, "ram": r, "id_factory": nuevo_recurso.id_producto}
                )
                print(f" ¡Laptop guardada exitosamente en DB!")

            elif opcion == '3':
                mod = input(" Ingresa el modelo de la tablet: ")
                
                nuevo_recurso = resource_factory.crear_recurso('tablet', modelo=mod)
                inventory.append(nuevo_recurso)
                
                controlador.registrar_recurso(
                    tipo="Tablet", 
                    nombre=f"Tablet {mod}", 
                    detalles={"modelo": mod, "id_factory": nuevo_recurso.id_producto}
                )
                print(f" ¡Tablet guardada exitosamente en DB!")

            elif opcion == '4':
                print("\n --- INVENTARIO ACTUAL (BASE DE DATOS) ---")
                inventario_db = controlador.consultar_inventario()
                
                if not inventario_db:
                    print("El inventario está vacío. ¡Crea algunos recursos primero!")
                else:
                    for recurso in inventario_db:
                        # Extraemos los datos basándonos en la estructura de tu Sprint 2
                        print(f"▶ ID: {recurso['id']} | Tipo: {recurso['tipo']} | Nombre: {recurso['nombre']} | Estado: {recurso['estado']} | Detalles: {recurso['detalles']}")

            elif opcion == '5':
                print("\n --- SIMULACIÓN DE PRÉSTAMO ---")
                id_rec = input(" Ingresa el ID (numérico) del recurso a prestar: ")
                if id_rec.isdigit():
                    controlador.actualizar_estado(recurso_id=int(id_rec), nuevo_estado="Prestado")
                    print(f" ¡Estado del recurso {id_rec} actualizado a 'Prestado'!")
                else:
                    print(" Error: Por favor ingresa un número de ID válido.")

            elif opcion == '6':
                print("Guardando cambios y cerrando conexiones de base de datos...")
                print("Saliendo del sistema. ¡Hasta pronto!")
                break
            
            else:
                print("Opción no válida. Por favor, escribe un número del 1 al 6.")

        except Exception as e:
            print(f" Ocurrió un error al procesar tu solicitud: {e}")

if __name__ == "__main__":
    main()