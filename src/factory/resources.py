from abc import ABC, abstractmethod

# 1. Clase Base Abstracta
class resource (ABC):
    @abstractmethod
    def use(self) -> str:
        """Método que todas las clases hijas deben implementar."""
        pass

# Subclases Recursos (Clases hijas)
class book (resource):
    def __init__(self, titulo: str, autor: str):
        self.titulo = titulo
        self.autor = autor

    def use(self) -> str:
        return f" Leyendo el libro '{self.titulo}' de {self.autor}."

class laptop (resource):
    def __init__(self, marca: str, ram: str):
        self.marca = marca
        self.ram = ram

    def use(self) -> str:
        return f" Programando en la laptop {self.marca} con {self.ram} de RAM."

class tablet (resource):
    def __init__(self, modelo: str):
        self.modelo = modelo

    def use(self) -> str:
        return f" Navegando y tomando notas en la tablet {self.modelo}."

# 3. La Clase Estrella: Factory
class resource_factory:
    @staticmethod
    def crear_recurso(tipo_equipo: str, **kwargs) -> resource:
        """
        Recibe el tipo de equipo como string y los argumentos necesarios (kwargs).
        Devuelve la instancia de la clase correspondiente.
        """
        tipo_equipo = tipo_equipo.lower()
        
        if tipo_equipo == 'book':
            return book(**kwargs)
        elif tipo_equipo == 'laptop':
            return laptop(**kwargs)
        elif tipo_equipo == 'tablet':
            return tablet(**kwargs)
        else:
            raise ValueError(f"Error: El tipo de equipo '{tipo_equipo}' no es válido o no está soportado.")