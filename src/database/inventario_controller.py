import sqlite3
from datetime import datetime
from src.database.conexion import DatabaseManager

class InventarioController:
    """Controlador encargado de las operaciones CRUD del inventario adaptado a Excel."""

    def __init__(self, db_manager):
        # Inyectamos el gestor que ya inicializó el main de forma segura.
        self.db_manager = db_manager

    # =========================================================================
    # 1. GESTIÓN DE RECURSOS (Tabla: Features)
    # =========================================================================
    def registrar_recurso(self, tipo, nombre, detalles=None):
        """
        C: CREATE - Inserta un recurso en la tabla 'Features' formateando los 
        atributos dinámicos del Factory en un solo string separado por '|'.
        """
        conn = self.db_manager.conectar()
        if not conn: 
            return False
            
        try:
            cursor = conn.cursor()
            
            # Procesar el diccionario de detalles para convertirlo al formato string de Excel
            if detalles and isinstance(detalles, dict):
                # Filtramos 'id_factory' para no mezclarlo con el texto plano si no es necesario
                valores_detalles = [str(v) for k, v in detalles.items() if k != 'id_factory']
                descripcion_compuesta = f"{nombre}|" + "|".join(valores_detalles)
            else:
                descripcion_compuesta = nombre

            # Capturar fecha y hora actual para cumplir con lastupdate y lasttime
            ahora = datetime.now()
            fecha_actual = ahora.strftime("%d/%m/%Y")
            hora_actual = ahora.strftime("%I:%M %p").lower()
            
            # Cantidad inicial por defecto para el recurso creado
            unidades_iniciales = 3 

            cursor.execute("""
                INSERT INTO Features (tipo_de_bien, descripcion, lastupdate, lasttime, unidades)
                VALUES (?, ?, ?, ?, ?);
            """, (tipo.lower(), descripcion_compuesta, fecha_actual, hora_actual, unidades_iniciales))
            
            recurso_id = cursor.lastrowid
            conn.commit()
            print(f"✅ Recurso '{nombre}' registrado en Features con ID: {recurso_id}")
            return True
            
        except sqlite3.Error as e:
            conn.rollback()
            print(f"❌ ERROR DE BLINDAJE (Registrar en Features): {e}")
            return False
        finally:
            conn.close()

    def consultar_inventario(self):
        """
        R: READ - Obtiene de forma masiva y eficiente el inventario de la tabla Features.
        Mantiene compatibilidad de salida para evitar que falle el main.py original.
        """
        conn = self.db_manager.conectar()
        if not conn: 
            return []
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id_recurso, tipo_de_bien, descripcion, lastupdate, lasttime, unidades FROM Features;")
            registros = cursor.fetchall()
            
            inventario_completo = []
            for id_rec, tipo, desc, fecha, hora, und in registros:
                # Estructuramos el diccionario con las claves que tu main.py lee en el ciclo
                item = {
                    "id": id_rec,
                    "tipo": tipo.capitalize(),
                    "nombre": desc.split('|')[0],  # El primer elemento antes del pipe es el nombre
                    "estado": f"{und} Unidades disponibles",
                    "detalles": f"{desc} | Última Modificación: {fecha} {hora}"
                }
                inventario_completo.append(item)
            return inventario_completo
            
        except sqlite3.Error as e:
            print(f"❌ ERROR DE BLINDAJE (Consultar Features): {e}")
            return []
        finally:
            conn.close()

    def eliminar_recurso(self, recurso_id):
        """
        D: DELETE - Elimina un recurso permanentemente de la tabla Features.
        """
        conn = self.db_manager.conectar()
        if not conn: 
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Features WHERE id_recurso = ?;", (recurso_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"🗑️ Recurso ID {recurso_id} eliminado de Features.")
                return True
            else:
                print(f"⚠️ No se encontró el recurso ID {recurso_id}.")
                return False
        except sqlite3.Error as e:
            print(f"❌ ERROR DE BLINDAJE (Eliminar Recurso): {e}")
            return False
        finally:
            conn.close()


    # =========================================================================
    # 2. GESTIÓN DE MOVIMIENTOS (Tabla: movements)
    # =========================================================================
    def registrar_prestamo(self, id_recurso, usuario_nombre="luis", rol_usuario=1):
        """
        U/C: UPDATE/CREATE - Descuenta 1 unidad de stock de Features y asienta
        el registro de la transacción de forma blindada en la tabla 'movements'.
        """
        conn = self.db_manager.conectar()
        if not conn: 
            return False
            
        try:
            cursor = conn.cursor()

            # 1. Verificar existencias del recurso en Features antes de prestar
            cursor.execute("SELECT unidades FROM Features WHERE id_recurso = ?;", (id_recurso,))
            recurso = cursor.fetchone()

            if not recurso:
                print(f"⚠️ El recurso con ID {id_recurso} no existe en el sistema.")
                return False

            unidades_actuales = recurso[0]
            if unidades_actuales <= 0:
                print(f"❌ Operación rechazada: No quedan unidades físicas disponibles para el ID {id_recurso}.")
                return False

            # Generar datos de fecha y hora para el registro
            ahora = datetime.now()
            fecha_actual = ahora.strftime("%d/%m/%Y")
            hora_actual = ahora.strftime("%I:%M %p").lower()

            # 2. Actualizar stock restando una unidad e indicando momento de la acción
            cursor.execute("""
                UPDATE Features 
                SET unidades = ?, lastupdate = ?, lasttime = ? 
                WHERE id_recurso = ?;
            """, (unidades_actuales - 1, fecha_actual, hora_actual, id_recurso))

            # 3. Insertar el registro correspondiente en la tabla movements
            cursor.execute("""
                INSERT INTO movements (id_recurso, usuario, Rollusuario, Tipodeaccion, fecha)
                VALUES (?, ?, ?, ?, ?);
            """, (id_recurso, usuario_nombre, rol_usuario, 'Prestamo', fecha_actual))

            # Transacción completa segura
            conn.commit()
            print(f"✅ Préstamo procesado con éxito para el recurso ID {id_recurso}.")
            print(f"📉 Stock actualizado: {unidades_actuales - 1} unidades restantes.")
            return True
            
        except sqlite3.Error as e:
            conn.rollback()
            print(f"❌ ERROR DE BLINDAJE (Transacción Préstamo): {e}")
            return False
        finally:
            conn.close()


    # =========================================================================
    # 3. GESTIÓN DE USUARIOS Y ROLES (Tablas: Users / user_roles)
    # =========================================================================
    def registrar_usuario(self, cedula, nombre, roll=4, pasword="123", mail="correo@gmail.com"):
        """Inserta un nuevo usuario en la tabla Users usando llaves foráneas a user_roles."""
        conn = self.db_manager.conectar()
        if not conn: 
            return False
            
        try:
            cursor = conn.cursor()
            fecha_actual = datetime.now().strftime("%d/%m/%Y")
            
            cursor.execute("""
                INSERT INTO Users (cedula, nombre, fecha_creacion, roll, pasword, mail)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (cedula, nombre, fecha_actual, roll, pasword, mail))
            
            conn.commit()
            print(f"👤 Usuario '{nombre}' registrado con éxito en el sistema.")
            return True
        except sqlite3.Error as e:
            print(f"❌ ERROR DE BLINDAJE (Registrar Usuario): {e}")
            return False
        finally:
            conn.close()
