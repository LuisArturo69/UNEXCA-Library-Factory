  #Creado el 12/05/2026 Luis Silva (Primer paso del proyecto segun conversado) se encargará de que el programa nunca se cierre inesperadamente
import json
import os

class JSONManager:
    """Clase para gestionar archivos JSON de forma segura"""

    @staticmethod
    def guardar_datos(archivo, datos):
        """Guarda información en un JSON. Si falla, lanza un error controlado."""
        try:
            # Asegurar que la carpeta 'data' exista
            os.makedirs(os.path.dirname(archivo), exist_ok=True)
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ ERROR DE BLINDAJE (Guardado): {e}")
            return False

    @staticmethod
    def cargar_datos(archivo):
        """Carga datos de un JSON. Si el archivo no existe, devuelve una lista vacía."""
        if not os.path.exists(archivo):
            print(f"⚠️ El archivo {archivo} no existe. Creando entorno nuevo...")
            return []
        
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"❌ ERROR DE BLINDAJE: El archivo {archivo} está corrupto.")
            return []
