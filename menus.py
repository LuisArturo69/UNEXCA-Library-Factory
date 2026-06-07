"""
SISTEMA DE GESTIÓN DE PRÉSTAMOS
Solo menús anidados - Sin funciones o BDD
"""

def menu_estudiante():
    """Menú para Estudiantes"""
    while True:
        print("\n" + "="*50)
        print("       MENÚ ESTUDIANTE")
        print("="*50)
        print("1. Solicitar un préstamo")
        print("2. Entregar un préstamo")
        print("3. Consultar inventario")
        print("4. Estado de mis préstamos")
        print("5. Salir del sistema")
        print("="*50)
        
        opcion = input("\nElige una opción (1-5): ")
        
        if opcion == '1':
            print("\nHas seleccionado: Solicitar un préstamo")
            # Aqui se añadira la función para solicitar préstamo
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '2':
            print("\n Has seleccionado: Entregar un préstamo")
            # Aqui se añadira la función para entregar préstamo
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '3':
            print("\n Has seleccionado: Consultar inventario")
            # Aqui se añadira la función para consultar inventario
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '4':
            print("\n Has seleccionado: Estado de mis préstamos")
            # Aqui se añadira la función para ver estado de préstamos
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '5':
            print("\n Saliendo del menú Estudiante...")
            break
        else:
            print("\n Opción no válida. Intenta de nuevo.")


def menu_bibliotecario():
    """Menú para Bibliotecarios/Docentes"""
    while True:
        print("\n" + "="*50)
        print("     MENÚ BIBLIOTECARIO/DOCENTE")
        print("="*50)
        print("1. Registrar préstamo")
        print("2. Registrar devolución")
        print("3. Consultar estado de préstamos")
        print("4. Consultar inventario")
        print("5. Salir del sistema")
        print("="*50)
        
        opcion = input("\nElige una opción (1-5): ")
        
        if opcion == '1':
            print("\n Has seleccionado: Registrar préstamo")
            # Aqui se añadira la función para registrar préstamo
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '2':
            print("\n Has seleccionado: Registrar devolución")
            # Aqui se añadira la función para registrar devolución
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '3':
            print("\n Has seleccionado: Consultar estado de préstamos")
            # Aqui se añadira la función para consultar estado de préstamos
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '4':
            print("\n Has seleccionado: Consultar inventario")
            # Aqui se añadira la función para consultar inventario
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '5':
            print("\n Saliendo del menú Bibliotecario...")
            break
        
        else:
            print("\n Opción no válida. Intenta de nuevo.")


def menu_administrador():
    """Menú para Administrador"""
    while True:
        print("\n" + "="*50)
        print("       MENÚ ADMINISTRADOR")
        print("="*50)
        print("1. Registrar préstamo")
        print("2. Registrar devolución")
        print("3. Consultar estado de préstamos")
        print("4. Consultar inventario")
        print("5. Gestionar usuarios")
        print("6. Gestionar recursos")
        print("7. Ver estadísticas")
        print("8. Salir del sistema")
        print("="*50)
        
        opcion = input("\nElige una opción (1-8): ")
        
        if opcion == '1':
            print("\nHas seleccionado: Registrar préstamo")
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '2':
            print("\nHas seleccionado: Registrar devolución")
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '3':
            print("\n Has seleccionado: Consultar estado de préstamos")
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '4':
            print("\n Has seleccionado: Consultar inventario")
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '5':
            print("\nHas seleccionado: Gestionar usuarios")
            # Submenú para gestionar usuarios
            print("\n  --- GESTIONAR USUARIOS ---")
            print("  a. Crear usuario")
            print("  b. Editar usuario")
            print("  c. Eliminar usuario")
            print("  d. Listar usuarios")
            sub_opcion = input("  Elige una opción: ")
            print(f" Has seleccionado: {sub_opcion}")
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '6':
            print("\n Has seleccionado: Gestionar recursos")
            # Submenú para gestionar recursos
            print("\n  --- GESTIONAR RECURSOS ---")
            print("  a. Agregar recurso")
            print("  b. Editar recurso")
            print("  c. Eliminar recurso")
            print("  d. Listar recursos")
            sub_opcion = input("  Elige una opción: ")
            print(f"  Has seleccionado: {sub_opcion}")
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '7':
            print("\n Has seleccionado: Ver estadísticas")
            # Mostrar estadísticas
            print("\n  --- ESTADÍSTICAS ---")
            print("  • Total de préstamos activos: 0")
            print("  • Total de usuarios registrados: 0")
            print("  • Total de recursos disponibles: 0")
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '8':
            print("\nSaliendo del menú Administrador...")
            break
        
        else:
            print("\nOpción no válida. Intenta de nuevo.")


def menu_principal():
    """Menú principal - Selección de tipo de usuario"""
    while True:
        print("\n" + "="*50)
        print("       SISTEMA DE GESTIÓN DE PRÉSTAMOS")
        print("="*50)
        print("1. Acceder como ESTUDIANTE")
        print("2. Acceder como BIBLIOTECARIO/DOCENTE")
        print("3. Acceder como ADMINISTRADOR")
        print("4. Salir del programa")
        print("="*50)
        
        opcion = input("\nElige una opción (1-4): ")
        
        if opcion == '1':
            menu_estudiante()
        elif opcion == '2':
            menu_bibliotecario()
        elif opcion == '3':
            menu_administrador()
        elif opcion == '4':
            print("\n👋 ¡Gracias por usar el sistema! Hasta luego.")
            break
        else:
            print("\n Opción no válida. Intenta de nuevo.")


#Ejecución del programa

if __name__ == "__main__":
    print("\n" * 25)
    print("     BIENVENIDO AL SISTEMA DE PRÉSTAMOS")
    print("" * 25)
    menu_principal()