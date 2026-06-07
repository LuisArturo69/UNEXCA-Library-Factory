from abc import ABC, abstractmethod
import random

# Función para generar un ID aleatorio simple (sin verificación en BDD)
def generar_id_unico() -> str:
    """
    Genera un número aleatorio de 6 dígitos.
    No se verifica en la base de datos porque el ID del factory
    no es clave primaria; la BD usa su propio autoincremental.
    """
    return str(random.randint(100000, 999999))

# 1. Clase Base Abstracta
class resource(ABC):
    @abstractmethod
    def use(self) -> str:
        """Método que todas las clases hijas deben implementar."""
        pass

# 2. Subclases Recursos (Clases hijas)
class book(resource):
    def __init__(self, id_Product: str, titulo: str, autor: str):
        self.id_producto = id_Product 
        self.titulo = titulo
        self.autor = autor

    def use(self) -> str:
        return f"  Libro '{self.titulo}' de {self.autor} (ID: {self.id_producto})."

class laptop(resource):
    def __init__(self, id_Product: str, marca: str, ram: str):
        self.id_producto = id_Product
        self.marca = marca
        self.ram = ram

    def use(self) -> str:
        return f"  Laptop {self.marca} con {self.ram} de RAM (ID: {self.id_producto})."

class tablet(resource):
    def __init__(self, id_Product: str, modelo: str):
        self.id_producto = id_Product
        self.modelo = modelo

    def use(self) -> str:
        return f"  Tablet {self.modelo} (ID: {self.id_producto})."

# 3. La Clase Estrella: Factory
class resource_factory:
    @staticmethod
    def crear_recurso(tipo_equipo: str, **kwargs) -> resource:
        """
        Recibe el tipo de equipo como string y los argumentos necesarios (kwargs).
        Devuelve la instancia de la clase correspondiente con un ID único automático.
        """
        tipo_equipo = tipo_equipo.lower()
        
        if 'id_Product' not in kwargs:
            kwargs['id_Product'] = generar_id_unico()
            
        if tipo_equipo == 'book':
            return book(**kwargs)
        elif tipo_equipo == 'laptop':
            return laptop(**kwargs)
        elif tipo_equipo == 'tablet':
            return tablet(**kwargs)
        else:
            raise ValueError(f"Error: El tipo de equipo '{tipo_equipo}' no es válido o no está soportado.")