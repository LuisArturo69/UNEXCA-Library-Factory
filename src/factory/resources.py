from abc import ABC, abstractmethod
import random
import sqlite3

# Función para generar un ID aleatorio único verificando en la BDD
def generar_id_unico() -> str:
    """
    Genera un número aleatorio de 6 dígitos y verifica en la BDD 
    que no esté repetido. Si se repite, genera uno nuevo.
    """
    while True:
        # Generamos un ID aleatorio, por ejemplo, entre 100000 y 999999
        nuevo_id = str(random.randint(100000, 999999))
        
        try:
            # Nos conectamos a la BDD para verificar si el ID ya existe
            conexion = sqlite3.connect('biblioteca_v2.db')
            cursor = conexion.cursor()
            
            # Consultamos si hay algún registro con ese id_producto
            # (Asumimos que la columna en tu tabla se llama id_producto)
            cursor.execute("SELECT 1 FROM recursos WHERE id_producto = ?", (nuevo_id,))
            resultado = cursor.fetchone()
            
            conexion.close()
            
            # Si el resultado es None, el ID está libre y rompemos el ciclo
            if not resultado:
                return nuevo_id
                
        except sqlite3.OperationalError:
            # Si la base de datos o la tabla aún no existen (primera ejecución),
            # entonces el ID no puede estar repetido.
            return nuevo_id

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
        
        # Si el usuario o el sistema no enviaron un ID en los argumentos, 
        # generamos uno único automáticamente desde nuestra función.
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