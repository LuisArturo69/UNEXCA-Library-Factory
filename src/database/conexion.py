import os
import sqlite3

class DatabaseManager:
    def __init__(self, db_path="data/biblioteca.db"):
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        self.db_path = db_path
        self.connection = None
        self._connect()
        self.crear_tablas()

    def _connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

    def conectar(self):
        """Retorna una conexión activa. Si la actual está cerrada, la reabre."""
        if self.connection is None:
            self._connect()
        else:
            # Verificar si la conexión existente está cerrada
            try:
                # Intenta una operación mínima; si falla, la conexión está muerta
                self.connection.cursor().execute("SELECT 1").fetchone()
            except sqlite3.ProgrammingError:
                # La conexión está cerrada o es inválida -> reconectar
                self._connect()
        return self.connection

    def crear_tablas(self):
        if not self.connection:
            return
        cursor = self.connection.cursor()
        # 1. user_roles
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_roles (
                id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
                Roll TEXT NOT NULL UNIQUE,
                Descripcion TEXT NOT NULL,
                Permisos TEXT NOT NULL
            );
        """)
        # 2. Users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                fecha_creacion TEXT NOT NULL,
                roll INTEGER,
                pasword TEXT NOT NULL,
                mail TEXT NOT NULL,
                FOREIGN KEY (roll) REFERENCES user_roles(id_rol)
            );
        """)
        # 3. Features (Inventario)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Features (
                id_recurso INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_de_bien TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                lastupdate TEXT NOT NULL,
                lasttime TEXT NOT NULL,
                unidades INTEGER NOT NULL DEFAULT 0
            );
        """)
        # 4. movements (Historial)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movements (
                id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
                id_recurso INTEGER,
                usuario TEXT NOT NULL,
                Rollusuario INTEGER,
                Tipodeaccion TEXT NOT NULL CHECK(Tipodeaccion IN ('Prestamo', 'Devolucion')),
                fecha TEXT NOT NULL,
                FOREIGN KEY (id_recurso) REFERENCES Features(id_recurso) ON DELETE CASCADE,
                FOREIGN KEY (Rollusuario) REFERENCES user_roles(id_rol)
            );
        """)
        # Roles por defecto
        cursor.execute("SELECT COUNT(*) FROM user_roles;")
        if cursor.fetchone()[0] == 0:
            roles_defecto = [
                (1, 'Admin', 'Administrador', 'Full'),
                (2, 'Sistem', 'Personal de sistemas', 'sistemas'),
                (3, 'UserBiblio', 'Bibliotecarios', 'biblioteca'),
                (4, 'UserBasic', 'Usuario Comun', 'basic')
            ]
            cursor.executemany("""
                INSERT INTO user_roles (id_rol, Roll, Descripcion, Permisos)
                VALUES (?, ?, ?, ?);
            """, roles_defecto)
            print("🔹 Roles por defecto cargados.")
        self.connection.commit()
        print("✅ Tablas creadas/verificadas correctamente.")

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None  