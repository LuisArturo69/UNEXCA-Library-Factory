import tkinter as tk
from tkinter import messagebox, ttk

# --- PALETA DE COLORES EN AZUL ---
COLOR_FONDO = "#E3F2FD"      # Azul muy claro (fondo principal)
COLOR_BOTON = "#1976D2"      # Azul medio intenso (botones)
COLOR_BOTON_HOVER = "#1565C0" # Azul más oscuro (hover)
COLOR_TEXTO_BOTON = "white"  # Texto blanco en botones
COLOR_TITULO = "#0D47A1"     # Azul muy oscuro (títulos)
COLOR_FRAME = "#BBDEFB"      # Azul claro para frames secundarios
COLOR_SUBMENU = "#90CAF9"    # Azul intermedio para submenús

def configurar_estilos():
    estilo = ttk.Style()
    estilo.theme_use('clam')
    estilo.configure('TLabel', background=COLOR_FONDO, foreground=COLOR_TITULO, font=('Segoe UI', 10))
    estilo.configure('TButton', background=COLOR_BOTON, foreground=COLOR_TEXTO_BOTON,
                     font=('Segoe UI', 10, 'bold'), borderwidth=0, focuscolor='none')
    estilo.map('TButton', background=[('active', COLOR_BOTON_HOVER)])

class Aplicacion:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        
        # Guardaremos el usuario que inicia sesión activamente en el sistema
        self.usuario_actual = None 

        self.root.title("Sistema de Gestión de Préstamos - UNEXCA")
        self.root.geometry("1360x768") 
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)

        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')

        self.contenedor_vista = tk.Frame(self.root, bg=COLOR_FONDO)
        self.contenedor_vista.pack(fill=tk.BOTH, expand=True)

        # Arrancar directamente en la pantalla de Login
        self.mostrar_login()

        tk.Label(self.root, text="© Sistema de Préstamos - Todos los derechos reservados",
                 font=('Segoe UI', 8), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(side=tk.BOTTOM, pady=10)

    def limpiar_pantalla(self):
        self.contenedor_vista.config(bg=COLOR_FONDO) 
        for widget in self.contenedor_vista.winfo_children():
            widget.destroy()

    def aplicar_efecto_hover(self, boton):
        boton.bind("<Enter>", lambda e: boton.config(bg=COLOR_BOTON_HOVER))
        boton.bind("<Leave>", lambda e: boton.config(bg=COLOR_BOTON))

    # =========================================================================
    # PANTALLA PRINCIPAL: LOGIN DE CONTROL DE ACCESO
    # =========================================================================
    def mostrar_login(self):
        self.limpiar_pantalla()
        self.usuario_actual = None # Limpiar sesión

        tk.Label(self.contenedor_vista, text="SISTEMA DE GESTIÓN DE PRÉSTAMOS",
                 font=('Segoe UI', 18, 'bold'), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=25)

        tk.Label(self.contenedor_vista, text="Control de Acceso UNEXCA",
                 font=('Segoe UI', 12, 'italic'), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=5)

        # Cuadro de Login
        frame_login = tk.Frame(self.contenedor_vista, bg=COLOR_FRAME, bd=2, relief=tk.GROOVE)
        frame_login.pack(pady=20, padx=100, fill=tk.X)

        tk.Label(frame_login, text="Cédula de Identidad:", bg=COLOR_FRAME, font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, padx=20, pady=15, sticky=tk.W)
        entry_cedula = tk.Entry(frame_login, font=('Segoe UI', 11), width=22)
        entry_cedula.grid(row=0, column=1, padx=20, pady=15)
        entry_cedula.focus()

        tk.Label(frame_login, text="Contraseña:", bg=COLOR_FRAME, font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, padx=20, pady=15, sticky=tk.W)
        entry_password = tk.Entry(frame_login, font=('Segoe UI', 11), width=22, show="*")
        entry_password.grid(row=1, column=1, padx=20, pady=15)

        def verificar_credenciales():
            cedula = entry_cedula.get().strip()
            password = entry_password.get().strip()

            if not cedula or not password:
                messagebox.showerror("Campos Vacíos", "Por favor, introduzca sus credenciales de acceso.")
                return

            # Consultar en la base de datos a través del controlador
            usuario = self.controlador.autenticar_usuario(cedula, password)

            if usuario:
                self.usuario_actual = usuario
                messagebox.showinfo("Acceso Concedido", f"¡Bienvenido(a), {usuario['nombre']}!")
                
                # Enrutar según el rol numérico de la Base de Datos
                rol = usuario["rol"]
                if rol == 1 or rol == 2:  # Admin o Sistem
                    self.mostrar_menu_administrador()
                elif rol == 3:            # UserBiblio
                    self.mostrar_menu_bibliotecario()
                elif rol == 4:            # UserBasic (Estudiante)
                    self.mostrar_menu_estudiante()
                else:
                    messagebox.showerror("Error de Rol", "El rol de este usuario no está catalogado en el sistema.")
            else:
                messagebox.showerror("Acceso Denegado", "Cédula o contraseña incorrectas.\nVerifique los datos ingresados.")

        btn_ingresar = tk.Button(self.contenedor_vista, text="Iniciar Sesión", font=('Segoe UI', 11, 'bold'),
                                 bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=22, command=verificar_credenciales)
        btn_ingresar.pack(pady=10)
        self.aplicar_efecto_hover(btn_ingresar)

        btn_salir = tk.Button(self.contenedor_vista, text="Salir", font=('Segoe UI', 10),
                               bg="#757575", fg="white", width=15, command=self.root.quit)
        btn_salir.pack(pady=5)

    # =========================================================================
    # VISTAS DE MENÚS (SEGURAS POR SESIÓN)
    # =========================================================================
    def mostrar_menu_estudiante(self):
        self.limpiar_pantalla()
        tk.Label(self.contenedor_vista, text=f"MENÚ ESTUDIANTE\nSesión: {self.usuario_actual['nombre']}", 
                 font=('Segoe UI', 14, 'bold'), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=25)

        frame_botones = tk.Frame(self.contenedor_vista, bg=COLOR_FONDO)
        frame_botones.pack(expand=True)

        opciones = [
            ("1. Solicitar un préstamo", lambda: self.vista_formulario_prestamo("SOLICITAR PRÉSTAMO", default_rol=4, retorno=self.mostrar_menu_estudiante)),
            ("2. Entregar un préstamo", lambda: self.vista_formulario_devolucion("ENTREGAR PRÉSTAMO", default_rol=4, retorno=self.mostrar_menu_estudiante)),
            ("3. Consultar inventario disponible", lambda: self.vista_listar_recursos(retorno=self.mostrar_menu_estudiante)),
            ("Cerrar Sesión", self.mostrar_login)
        ]

        for texto, comando in opciones:
            btn = tk.Button(frame_botones, text=texto, font=('Segoe UI', 11),
                            bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=35, height=1, command=comando)
            btn.pack(pady=8)
            self.aplicar_efecto_hover(btn)

    def mostrar_menu_bibliotecario(self):
        self.limpiar_pantalla()
        tk.Label(self.contenedor_vista, text=f"MENÚ BIBLIOTECARIO / DOCENTE\nSesión: {self.usuario_actual['nombre']}", 
                 font=('Segoe UI', 14, 'bold'), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=25)

        frame_botones = tk.Frame(self.contenedor_vista, bg=COLOR_FONDO)
        frame_botones.pack(expand=True)

        opciones = [
            ("1. Registrar préstamo", lambda: self.vista_formulario_prestamo("REGISTRAR PRÉSTAMO - BIBLIOTECA", default_rol=3, retorno=self.mostrar_menu_bibliotecario)),
            ("2. Registrar devolución", lambda: self.vista_formulario_devolucion("REGISTRAR DEVOLUCIÓN - BIBLIOTECA", default_rol=3, retorno=self.mostrar_menu_bibliotecario)),
            ("3. Consultar inventario completo", lambda: self.vista_listar_recursos(retorno=self.mostrar_menu_bibliotecario)),
            ("Cerrar Sesión", self.mostrar_login)
        ]

        for texto, comando in opciones:
            btn = tk.Button(frame_botones, text=texto, font=('Segoe UI', 11),
                            bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=35, height=1, command=comando)
            btn.pack(pady=8)
            self.aplicar_efecto_hover(btn)

    def mostrar_menu_administrador(self):
        self.limpiar_pantalla()
        tk.Label(self.contenedor_vista, text=f"MENÚ ADMINISTRADOR\nSesión: {self.usuario_actual['nombre']}", 
                 font=('Segoe UI', 14, 'bold'), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=20)

        frame_botones = tk.Frame(self.contenedor_vista, bg=COLOR_FONDO)
        frame_botones.pack(expand=True)

        opciones = [
            ("1. Registrar préstamo operativo", lambda: self.vista_formulario_prestamo("REGISTRAR PRÉSTAMO - OPERACIÓN", default_rol=1, retorno=self.mostrar_menu_administrador)),
            ("2. Registrar devolución operativa", lambda: self.vista_formulario_devolucion("REGISTRAR DEVOLUCIÓN - OPERACIÓN", default_rol=1, retorno=self.mostrar_menu_administrador)),
            ("3. Gestionar recursos (CRUD)", self.mostrar_submenu_recursos),
            ("4. Gestionar usuarios (CRUD)", self.mostrar_submenu_usuarios),
            ("🚪 Cerrar Sesión", self.mostrar_login)
        ]

        for texto, comando in opciones:
            btn = tk.Button(frame_botones, text=texto, font=('Segoe UI', 11),
                            bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=38, height=1, command=comando)
            btn.pack(pady=6)
            self.aplicar_efecto_hover(btn)

    # =========================================================================
    # ACCIONES GENERALES DEL SISTEMA (AMIGABLES CON COMBOBOX)
    # =========================================================================
    def vista_listar_recursos(self, retorno):
        self.limpiar_pantalla()
        tk.Label(self.contenedor_vista, text="INVENTARIO GENERAL (TABLA FEATURES)", font=('Segoe UI', 14, 'bold'),
                 bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=15)

        columnas = ('id', 'tipo', 'nombre', 'estado')
        tabla = ttk.Treeview(self.contenedor_vista, columns=columnas, show='headings', height=12)
        
        tabla.heading('id', text='ID Recurso')
        tabla.heading('tipo', text='Tipo de Bien')
        tabla.heading('nombre', text='Nombre de Recurso')
        tabla.heading('estado', text='Disponibilidad Física')

        tabla.column('id', width=80, anchor=tk.CENTER)
        tabla.column('tipo', width=130, anchor=tk.W)
        tabla.column('nombre', width=220, anchor=tk.W)
        tabla.column('estado', width=180, anchor=tk.CENTER)
        tabla.pack(pady=10, padx=20, fill=tk.X)

        recursos = self.controlador.consultar_inventario()
        for r in recursos:
            tabla.insert('', tk.END, values=(r['id'], r['tipo'], r['nombre'], r['estado']))

        btn_volver = tk.Button(self.contenedor_vista, text="Volver", font=('Segoe UI', 11),
                               bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=20, command=retorno)
        btn_volver.pack(pady=15)
        self.aplicar_efecto_hover(btn_volver)

    def vista_formulario_prestamo(self, titulo_vista, default_rol, retorno):
        self.limpiar_pantalla()
        tk.Label(self.contenedor_vista, text=titulo_vista, font=('Segoe UI', 14, 'bold'),
                 bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=20)

        frame_form = tk.Frame(self.contenedor_vista, bg=COLOR_FRAME, bd=2, relief=tk.GROOVE)
        frame_form.pack(pady=10, padx=50, fill=tk.X)

        todos_los_recursos = self.controlador.consultar_inventario()
        recursos_disponibles = [r for r in todos_los_recursos if "0 Unidades" not in r['estado']]
        lista_desplegable = [f"{r['id']}: {r['nombre']} ({r['tipo']})" for r in recursos_disponibles]

        tk.Label(frame_form, text="Seleccione el Recurso:", bg=COLOR_FRAME, font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, padx=10, pady=15, sticky=tk.W)
        combo_recursos = ttk.Combobox(frame_form, values=lista_desplegable, state="readonly", font=('Segoe UI', 10), width=35)
        combo_recursos.grid(row=0, column=1, padx=10, pady=15)
        if lista_desplegable: combo_recursos.current(0)
        else: combo_recursos.set("Sin stock disponible")

        tk.Label(frame_form, text="Usuario Operación:", bg=COLOR_FRAME, font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, padx=10, pady=15, sticky=tk.W)
        entry_user = tk.Entry(frame_form, font=('Segoe UI', 11), width=25)
        # Coloca por defecto el nombre de la persona que inició sesión
        entry_user.insert(0, self.usuario_actual["nombre"]) 
        entry_user.grid(row=1, column=1, padx=10, pady=15)

        def ejecutar_guardado():
            seleccion = combo_recursos.get()
            usuario = entry_user.get().strip()

            if not seleccion or seleccion.startswith("Alerta") or not usuario:
                messagebox.showerror("Error", "Selección o usuario inválido.")
                return

            id_rec = int(seleccion.split(":")[0])
            exito = self.controlador.registrar_prestamo(id_recurso=id_rec, usuario_nombre=usuario, rol_usuario=default_rol)
            if exito:
                messagebox.showinfo("Éxito", "¡Préstamo guardado correctamente!")
                retorno()
            else:
                messagebox.showerror("Error", "No se pudo procesar la transacción.")

        btn_guardar = tk.Button(self.contenedor_vista, text="Procesar Préstamo", font=('Segoe UI', 11, 'bold'),
                                bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=25, command=ejecutar_guardado)
        btn_guardar.pack(pady=15)
        self.aplicar_efecto_hover(btn_guardar)

        btn_cancelar = tk.Button(self.contenedor_vista, text="Cancelar", font=('Segoe UI', 11),
                                 bg="#757575", fg="white", width=25, command=retorno)
        btn_cancelar.pack(pady=5)

    def vista_formulario_devolucion(self, titulo_vista, default_rol, retorno):
        self.limpiar_pantalla()
        tk.Label(self.contenedor_vista, text=titulo_vista, font=('Segoe UI', 14, 'bold'),
                 bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=20)

        frame_form = tk.Frame(self.contenedor_vista, bg=COLOR_FRAME, bd=2, relief=tk.GROOVE)
        frame_form.pack(pady=10, padx=50, fill=tk.X)

        todos_los_recursos = self.controlador.consultar_inventario()
        lista_desplegable = [f"{r['id']}: {r['nombre']} ({r['tipo']})" for r in todos_los_recursos]

        tk.Label(frame_form, text="Recurso a Retornar:", bg=COLOR_FRAME, font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, padx=10, pady=15, sticky=tk.W)
        combo_recursos = ttk.Combobox(frame_form, values=lista_desplegable, state="readonly", font=('Segoe UI', 10), width=35)
        combo_recursos.grid(row=0, column=1, padx=10, pady=15)
        if lista_desplegable: combo_recursos.current(0)

        tk.Label(frame_form, text="Usuario Operación:", bg=COLOR_FRAME, font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, padx=10, pady=15, sticky=tk.W)
        entry_user = tk.Entry(frame_form, font=('Segoe UI', 11), width=25)
        entry_user.insert(0, self.usuario_actual["nombre"])
        entry_user.grid(row=1, column=1, padx=10, pady=15)

        def ejecutar_devolucion():
            seleccion = combo_recursos.get()
            usuario = entry_user.get().strip()

            if not seleccion or not usuario:
                messagebox.showerror("Error", "Debe seleccionar un recurso válido.")
                return

            id_rec = int(seleccion.split(":")[0])
            exito = self.controlador.registrar_devolucion(id_recurso=id_rec, usuario_nombre=usuario, rol_usuario=default_rol)
            if exito:
                messagebox.showinfo("Éxito", "¡Devolución asentada de forma exitosa!")
                retorno()
            else:
                messagebox.showerror("Error", "Error al procesar la devolución.")

        btn_guardar = tk.Button(self.contenedor_vista, text="Registrar Devolución", font=('Segoe UI', 11, 'bold'),
                                bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=25, command=ejecutar_devolucion)
        btn_guardar.pack(pady=15)
        self.aplicar_efecto_hover(btn_guardar)

        btn_cancelar = tk.Button(self.contenedor_vista, text="Cancelar", font=('Segoe UI', 11),
                                 bg="#757575", fg="white", width=25, command=retorno)
        btn_cancelar.pack(pady=5)

    # =========================================================================
    # ACCIONES CRUD ADICIONALES (ADMINISTRADOR)
    # =========================================================================
    def mostrar_submenu_recursos(self):
        self.limpiar_pantalla()
        self.contenedor_vista.config(bg=COLOR_SUBMENU)
        tk.Label(self.contenedor_vista, text="CONTROL DE BIENES E INVENTARIO", font=('Segoe UI', 14, 'bold'),
                 bg=COLOR_SUBMENU, fg=COLOR_TITULO).pack(pady=20)

        frame_botones = tk.Frame(self.contenedor_vista, bg=COLOR_SUBMENU)
        frame_botones.pack(expand=True)

        opciones = [
            ("a. Cargar Nuevo Recurso (Factory)", self.vista_agregar_recurso),
            ("b. Mostrar Inventario Completo", lambda: self.vista_listar_recursos(retorno=self.mostrar_submenu_recursos)),
            ("Volver al Menú Admin", lambda: [self.contenedor_vista.config(bg=COLOR_FONDO), self.mostrar_menu_administrador()])
        ]

        for texto, comando in opciones:
            btn = tk.Button(frame_botones, text=texto, font=('Segoe UI', 11), bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=32, command=comando)
            btn.pack(pady=6)
            self.aplicar_efecto_hover(btn)

    def vista_agregar_recurso(self):
        self.limpiar_pantalla()
        tk.Label(self.contenedor_vista, text="REGISTRAR NUEVO BIEN A FEATURES", font=('Segoe UI', 14, 'bold'), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=20)

        frame_form = tk.Frame(self.contenedor_vista, bg=COLOR_FRAME, bd=2, relief=tk.GROOVE)
        frame_form.pack(pady=10, padx=50, fill=tk.X)

        tk.Label(frame_form, text="Categoría del Recurso:", bg=COLOR_FRAME).grid(row=0, column=0, padx=10, pady=12, sticky=tk.W)
        combo_tipo = ttk.Combobox(frame_form, values=["Libro", "Laptop", "Tablet"], state="readonly", font=('Segoe UI', 10))
        combo_tipo.current(0)
        combo_tipo.grid(row=0, column=1, padx=10, pady=12)

        tk.Label(frame_form, text="Nombre o Título:", bg=COLOR_FRAME).grid(row=1, column=0, padx=10, pady=12, sticky=tk.W)
        entry_nombre = tk.Entry(frame_form, font=('Segoe UI', 11), width=25)
        entry_nombre.grid(row=1, column=1, padx=10, pady=12)

        tk.Label(frame_form, text="Detalle Atributo Extra:", bg=COLOR_FRAME).grid(row=2, column=0, padx=10, pady=12, sticky=tk.W)
        entry_extra = tk.Entry(frame_form, font=('Segoe UI', 11), width=25)
        entry_extra.grid(row=2, column=1, padx=10, pady=12)

        def ejecutar_alta():
            tipo = combo_tipo.get()
            nombre = entry_nombre.get().strip()
            extra = entry_extra.get().strip()

            if not nombre or not extra:
                messagebox.showerror("Error", "Todos los campos son requeridos.")
                return

            detalles_compuestos = {"propiedad_especifica": extra}
            exito = self.controlador.registrar_recurso(tipo=tipo, nombre=nombre, detalles=detalles_compuestos)
            if exito:
                messagebox.showinfo("Éxito", f"Recurso '{nombre}' insertado.")
                self.mostrar_submenu_recursos()
            else:
                messagebox.showerror("Error", "Error al procesar el alta.")

        btn_alta = tk.Button(self.contenedor_vista, text="Insertar Recurso", font=('Segoe UI', 11, 'bold'), bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=25, command=ejecutar_alta)
        btn_alta.pack(pady=15)
        self.aplicar_efecto_hover(btn_alta)

        btn_cancelar = tk.Button(self.contenedor_vista, text="Cancelar", font=('Segoe UI', 11), bg="#757575", fg="white", width=25, command=self.mostrar_submenu_recursos)
        btn_cancelar.pack(pady=5)

    def mostrar_submenu_usuarios(self):
        self.limpiar_pantalla()
        self.contenedor_vista.config(bg=COLOR_SUBMENU)
        tk.Label(self.contenedor_vista, text="CONTROL DE ACCESO Y USUARIOS", font=('Segoe UI', 14, 'bold'), bg=COLOR_SUBMENU, fg=COLOR_TITULO).pack(pady=20)

        frame_botones = tk.Frame(self.contenedor_vista, bg=COLOR_SUBMENU)
        frame_botones.pack(expand=True)

        opciones = [
            ("a. Cargar Nuevo Usuario (Users)", self.vista_agregar_usuario),
            ("Volver al Menú Admin", lambda: [self.contenedor_vista.config(bg=COLOR_FONDO), self.mostrar_menu_administrador()])
        ]

        for texto, comando in opciones:
            btn = tk.Button(frame_botones, text=texto, font=('Segoe UI', 11), bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=32, command=comando)
            btn.pack(pady=6)
            self.aplicar_efecto_hover(btn)

    def vista_agregar_usuario(self):
        self.limpiar_pantalla()
        tk.Label(self.contenedor_vista, text="REGISTRAR NUEVO USUARIO EN SISTEMA", font=('Segoe UI', 14, 'bold'), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=15)

        frame_form = tk.Frame(self.contenedor_vista, bg=COLOR_FRAME, bd=2, relief=tk.GROOVE)
        frame_form.pack(pady=10, padx=50, fill=tk.X)

        fields = ["Cédula de Identidad:", "Nombre Completo:", "Contraseña de Sistema:", "Correo Electrónico:"]
        entries = []
        for i, campo in enumerate(fields):
            tk.Label(frame_form, text=campo, bg=COLOR_FRAME).grid(row=i, column=0, padx=10, pady=7, sticky=tk.W)
            ent = tk.Entry(frame_form, font=('Segoe UI', 10), width=25)
            if "Contraseña" in campo: ent.config(show="*")
            ent.grid(row=i, column=1, padx=10, pady=7)
            entries.append(ent)

        tk.Label(frame_form, text="Nivel de Permisos (Rol):", bg=COLOR_FRAME).grid(row=4, column=0, padx=10, pady=7, sticky=tk.W)
        combo_rol = ttk.Combobox(frame_form, values=["1 - Admin", "2 - Sistem", "3 - UserBiblio", "4 - UserBasic"], state="readonly", font=('Segoe UI', 10))
        combo_rol.current(3)
        combo_rol.grid(row=4, column=1, padx=10, pady=7)

        def ejecutar_guardado_usuario():
            cedula = entries[0].get().strip()
            nombre = entries[1].get().strip()
            pwd = entries[2].get().strip()
            correo = entries[3].get().strip()
            rol_id = int(combo_rol.get().split(" - ")[0])

            if not cedula or not nombre or not pwd or not correo:
                messagebox.showerror("Error", "Todos los datos son requeridos.")
                return

            exito = self.controlador.registrar_usuario(cedula=cedula, nombre=nombre, roll=rol_id, pasword=pwd, mail=correo)
            if exito:
                messagebox.showinfo("Éxito", f"Usuario '{nombre}' guardado.")
                self.mostrar_submenu_usuarios()
            else:
                messagebox.showerror("Error", "No se pudo registrar (Cédula duplicada).")

        btn_guardar = tk.Button(self.contenedor_vista, text="Guardar Usuario", font=('Segoe UI', 11, 'bold'), bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=25, command=ejecutar_guardado_usuario)
        btn_guardar.pack(pady=15)
        self.aplicar_efecto_hover(btn_guardar)

        btn_cancelar = tk.Button(self.contenedor_vista, text="Cancelar", font=('Segoe UI', 11), bg="#757575", fg="white", width=25, command=self.mostrar_submenu_usuarios)
        btn_cancelar.pack(pady=5)


# --- BLOQUE EJECUTABLE PRINCIPAL ---
if __name__ == "__main__":
    import sys
    import os
    # Asegurar rutas absolutas para ejecución flexible
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    
    from src.database.conexion import DatabaseManager
    from src.database.inventario_controller import InventarioController
    
    db_manager = DatabaseManager()
    controlador_sistema = InventarioController(db_manager)
    
    root = tk.Tk()
    configurar_estilos()
    app = Aplicacion(root, controlador_sistema)
    root.mainloop()
