import sqlite3
import os

class DatabaseManager:
    """Clase encargada de conectar y asegurar la integridad de la base de datos."""
    
#    def __init__(self, db_path="data/biblioteca.db"):
#        self.db_path = db_path
#        # Blindaje: Asegurar que la carpeta data exista antes de conectar
#        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
#        self.crear_tablas()
#-------------------------------------------------------------------------------------
    def __init__(self, db_path="data/biblioteca.db"):
        # Blindaje: Si la ruta es relativa, la convertimos en una ruta absoluta
        # calculada desde la ubicación real de este archivo del proyecto.
        if not os.path.isabs(db_path):
            # Ruta de 'src/database'
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Subimos dos niveles para llegar a la raíz del proyecto
            raiz_proyecto = os.path.dirname(os.path.dirname(base_dir))
            # Unimos la raíz con la ruta del archivo (ej: 'C:/.../proyecto/data/biblioteca.db')
            self.db_path = os.path.join(raiz_proyecto, db_path)
        else:
            self.db_path = db_path

        # Asegurar que la carpeta 'data' exista en la ruta absoluta correcta antes de conectar
        carpeta_data = os.path.dirname(self.db_path)
        os.makedirs(carpeta_data, exist_ok=True)
        
        self.crear_tablas()
#------------------------------------------------------------------------------------- 
    def conectar(self):
        """Establece conexión con la base de datos aplicando el escudo try-except."""
        try:
            conn = sqlite3.connect(self.db_path)
            # Activar el soporte para llaves foráneas (Foreign Keys)
            conn.execute("PRAGMA foreign_keys = ON;")
            return conn
        except sqlite3.Error as e:
            print(f"❌ ERROR DE BLINDAJE (Conexión SQL): {e}")
            return None

    def crear_tablas(self):
        """Crea las tablas iniciales si no existen en el sistema."""
        conn = self.conectar()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            # 1. Tabla de Usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    cedula TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    contrasena TEXT NOT NULL,
                    rol TEXT NOT NULL CHECK(rol IN ('Administrador', 'Operador'))
                );
            """)

            # 2. Tabla General de Recursos (Inventario)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recursos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL CHECK(tipo IN ('Libro', 'Laptop', 'Tablet')),
                    nombre_recurso TEXT NOT NULL,
                    estado TEXT NOT NULL DEFAULT 'Disponible' CHECK(estado IN ('Disponible', 'Prestado', 'Mantenimiento'))
                );
            """)

            # 3. Tabla de Detalles Específicos (Para el Factory Method)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detalles_recursos (
                    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                    recurso_id INTEGER,
                    clave TEXT NOT NULL,       -- Ej: 'autor', 'serial', 'pantalla'
                    valor TEXT NOT NULL,       -- Ej: 'Louis Leithold', 'HP123', '10.5'
                    FOREIGN KEY (recurso_id) REFERENCES recursos(id) ON DELETE CASCADE
                );
            """)

            # 4. Tabla de Historial de Movimientos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS movimientos (
                    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
                    recurso_id INTEGER,
                    usuario_cedula TEXT,
                    tipo_accion TEXT NOT NULL CHECK(tipo_accion IN ('Préstamo', 'Devolución')),
                    fecha TEXT NOT NULL,
                    FOREIGN KEY (recurso_id) REFERENCES recursos(id),
                    FOREIGN KEY (usuario_cedula) REFERENCES usuarios(cedula)
                );
            """)

            conn.commit()
            print("✅ Estructura de tablas SQLite inicializada y blindada.")
        except sqlite3.Error as e:
            print(f"❌ ERROR DE BLINDAJE (Creación de Tablas): {e}")
        finally:
            conn.close()
