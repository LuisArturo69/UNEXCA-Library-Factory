import sqlite3
from src.database.conexion import DatabaseManager

class InventarioController:
    """Controlador encargado de las operaciones CRUD del inventario en SQLite."""

    def __init__(self):
        # Reutilizamos el gestor de conexión que creaste en el Sprint 1
        self.db_manager = DatabaseManager()

    def registrar_recurso(self, tipo, nombre, estado="Disponible", detalles=None):
        """
        C: CREATE - Inserta un recurso y sus detalles específicos de forma segura.
        'detalles' debe ser un diccionario. Ej: {"autor": "Leithold"} o {"serial": "XYZ"}
        """
        conn = self.db_manager.conectar()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            
            # 1. Insertar en la tabla general de recursos
            cursor.execute("""
                INSERT INTO recursos (tipo, nombre_recurso, estado)
                VALUES (?, ?, ?);
            """, (tipo, nombre, estado))
            
            # Obtener el ID generado automáticamente para este recurso
            recurso_id = cursor.lastrowid

            # 2. Insertar los detalles específicos (Atributos dinámicos para el Factory)
            if detalles and isinstance(detalles, dict):
                for clave, valor in detalles.items():
                    cursor.execute("""
                        INSERT INTO detalles_recursos (recurso_id, clave, valor)
                        VALUES (?, ?, ?);
                    """, (recurso_id, clave, str(valor)))

            # Guardamos los cambios de forma definitiva (Transacción exitosa)
            conn.commit()
            print(f"✅ Recurso '{nombre}' [{tipo}] registrado con ID: {recurso_id}")
            return True

        except sqlite3.Error as e:
            # Si algo falla, cancelamos toda la operación para evitar datos huérfanos
            conn.rollback()
            print(f"❌ ERROR DE BLINDAJE (CRUD Registrar): {e}")
            return False
        finally:
            conn.close()

    def consultar_inventario(self):
        """
        R: READ - Obtiene todos los recursos con sus detalles agrupados.
        Devuelve una lista de diccionarios lista para ser usada en la interfaz.
        """
        conn = self.db_manager.conectar()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            
            # Consultamos los recursos básicos
            cursor.execute("SELECT id, tipo, nombre_recurso, estado FROM recursos;")
            recursos_raw = cursor.fetchall()
            
            inventario_completo = []

            for r_id, tipo, nombre, estado in recursos_raw:
                # Buscamos los detalles asociados a este ID específico
                cursor.execute("SELECT clave, valor FROM detalles_recursos WHERE recurso_id = ?;", (r_id,))
                detalles_raw = cursor.fetchall()
                diccionario_detalles = {clave: valor for clave, valor in detalles_raw}

                # Estructuramos el objeto completo
                item = {
                    "id": r_id,
                    "tipo": tipo,
                    "nombre": nombre,
                    "estado": estado,
                    "detalles": diccionario_detalles
                }
                inventario_completo.append(item)

            return inventario_completo

        except sqlite3.Error as e:
            print(f"❌ ERROR DE BLINDAJE (CRUD Consultar): {e}")
            return []
        finally:
            conn.close()

    def actualizar_estado(self, recurso_id, nuevo_estado):
        """
        U: UPDATE - Modifica el estado del recurso (Disponible, Prestado, Mantenimiento).
        """
        conn = self.db_manager.conectar()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE recursos 
                SET estado = ? 
                WHERE id = ?;
            """, (nuevo_estado, recurso_id))
            
            conn.commit()
            if cursor.rowcount > 0:
                print(f"✅ Estado del recurso ID {recurso_id} actualizado a: {nuevo_estado}")
                return True
            else:
                print(f"⚠️ No se encontró ningún recurso con el ID {recurso_id}")
                return False
        except sqlite3.Error as e:
            print(f"❌ ERROR DE BLINDAJE (CRUD Actualizar): {e}")
            return False
        finally:
            conn.close()

    def eliminar_recurso(self, recurso_id):
        """
        D: DELETE - Elimina un recurso del sistema.
        Gracias a 'ON DELETE CASCADE' en la base de datos, sus detalles se borran solos.
        """
        conn = self.db_manager.conectar()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recursos WHERE id = ?;", (recurso_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"🗑️ Recurso ID {recurso_id} eliminado permanentemente del sistema.")
                return True
            return False
        except sqlite3.Error as e:
            print(f"❌ ERROR DE BLINDAJE (CRUD Eliminar): {e}")
            return False
        finally:
            conn.close()
