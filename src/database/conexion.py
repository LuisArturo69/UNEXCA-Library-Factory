def crear_tablas(self):
        """Crea las tablas definitivas basadas en las 4 tablas de Excel."""
        conn = self.conectar()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            # 1. Tabla de Roles de Usuario (user_roles) - NUEVA
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_roles (
                    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
                    Roll TEXT NOT NULL UNIQUE,
                    Descripcion TEXT NOT NULL,
                    Permisos TEXT NOT NULL
                );
            """)

            # 2. Tabla de Usuarios (Users) - Modificada FK
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                    cedula TEXT NOT NULL UNIQUE,
                    nombre TEXT NOT NULL,
                    fecha_creacion TEXT NOT NULL,
                    roll INTEGER, -- Ahora apunta al id_rol numérico de user_roles
                    pasword TEXT NOT NULL,
                    mail TEXT NOT NULL,
                    FOREIGN KEY (roll) REFERENCES user_roles(id_rol)
                );
            """)

            # 3. Tabla Principal de Inventario (Features)
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

            # 4. Tabla de Historial (movements) - Modificada FK
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS movements (
                    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_recurso INTEGER,
                    usuario TEXT NOT NULL,
                    Rollusuario INTEGER, -- Ahora apunta al id_rol numérico de user_roles
                    Tipodeaccion TEXT NOT NULL CHECK(Tipodeaccion IN ('Prestamo', 'Devolucion')),
                    fecha TEXT NOT NULL,
                    FOREIGN KEY (id_recurso) REFERENCES Features(id_recurso) ON DELETE CASCADE,
                    FOREIGN KEY (Rollusuario) REFERENCES user_roles(id_rol)
                );
            """)

            # POBILACIÓN AUTOMÁTICA DE ROLES POR DEFECTO
            # Inserta los 4 roles basicos si la tabla está recién creada (vacía)
            cursor.execute("SELECT COUNT(*) FROM user_roles;")
            if cursor.fetchone()[0] == 0:
                roles_defecto = [
                    (1, 'Admin', 'Administrador', 'Full'),
                    (2, 'Sistem', 'Persinal de sistemas', 'sistemas'),
                    (3, 'UserBiblio', 'Bibliotecarios', 'biblioteca'),
                    (4, 'UserBasic', 'Usuario Comun', 'basic')
                ]
                cursor.executemany("""
                    INSERT INTO user_roles (id_rol, Roll, Descripcion, Permisos)
                    VALUES (?, ?, ?, ?);
                """, roles_defecto)
                print("🔹 Roles por defecto cargados exitosamente en 'user_roles'.")

            conn.commit()
            print("✅ Estructura completa de 4 tablas inicializada y vinculada.")
        except sqlite3.Error as e:
            print(f"❌ ERROR DE BLINDAJE (Creación de Tablas Completa): {e}")
        finally:
            conn.close()
