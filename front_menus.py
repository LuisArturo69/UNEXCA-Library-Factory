import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# --- PALETA DE COLORES MODERNA (Estilo Grid Dashboard Recuperado) ---
COLOR_FONDO = "#F0F4F8"        
COLOR_TARJETA = "#E1F5FE"      
COLOR_TARJETA_HOVER = "#B3E5FC"
COLOR_TEXTO_MAIN = "#0D47A1"   
COLOR_LINEA = "#CFD8DC"        

class Aplicacion:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.usuario_actual = None 

        self.root.title("SISTEMA DE GESTIÓN DE PRÉSTAMOS - UNEXCA")
        self.root.geometry("850x570") 
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)

        # Centrar Ventana de Forma Dinámica
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')

        self.contenedor_vista = tk.Frame(self.root, bg=COLOR_FONDO)
        self.contenedor_vista.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.mostrar_login()

    def limpiar_pantalla(self):
        for widget in self.contenedor_vista.winfo_children():
            widget.destroy()

    # =========================================================================
    # LOGUEO DE USUARIOS
    # =========================================================================
    def mostrar_login(self):
        self.limpiar_pantalla()
        self.usuario_actual = None

        tk.Label(self.contenedor_vista, text="SISTEMA DE GESTIÓN DE PRÉSTAMOS",
                 font=('Segoe UI', 18, 'bold'), bg=COLOR_FONDO, fg=COLOR_TEXTO_MAIN).pack(pady=(40, 5))
        tk.Label(self.contenedor_vista, text="UNEXCA - LOS APÓSTOLES DE PROYECTO",
                 font=('Segoe UI', 11, 'bold', 'italic'), bg=COLOR_FONDO, fg="#546E7A").pack(pady=(0, 30))

        frame_login = tk.Frame(self.contenedor_vista, bg="white", bd=1, relief=tk.SOLID)
        frame_login.pack(pady=10, padx=150, fill=tk.X)

        inner_form = tk.Frame(frame_login, bg="white")
        inner_form.pack(padx=30, pady=25, fill=tk.X)

        tk.Label(inner_form, text="Cédula de Identidad:", bg="white", font=('Segoe UI', 10, 'bold'), fg=COLOR_TEXTO_MAIN).grid(row=0, column=0, pady=10, sticky=tk.W)
        entry_cedula = tk.Entry(inner_form, font=('Segoe UI', 11), bd=1, relief=tk.SOLID, width=22)
        entry_cedula.grid(row=0, column=1, pady=10, padx=(10, 0))
        entry_cedula.focus()
        # "Cambiar el foco al presionar Enter en el campo de cédula"
        entry_cedula.bind('<Return>', lambda event: entry_password.focus_set())  # Pasar al campo contraseña


        tk.Label(inner_form, text="Contraseña:", bg="white", font=('Segoe UI', 10, 'bold'), fg=COLOR_TEXTO_MAIN).grid(row=1, column=0, pady=10, sticky=tk.W)
        entry_password = tk.Entry(inner_form, font=('Segoe UI', 11), bd=1, relief=tk.SOLID, width=22, show="*")
        entry_password.grid(row=1, column=1, pady=10, padx=(10, 0))
        #cambiar el foco al presionar Enter en el campo de contraseña
        entry_password.bind('<Return>', lambda event: verificar_credenciales())
        def verificar_credenciales():
            cedula = entry_cedula.get().strip()
            password = entry_password.get().strip()

            if not cedula or not password:
                messagebox.showerror("Campos Vacíos", "Por favor introduzca sus credenciales.")
                return

            usuario = self.controlador.autenticar_usuario(cedula, password)
            if usuario:
                self.usuario_actual = usuario
                if usuario["rol"] in (1, 2):  
                    self.mostrar_menu_administrador()
                elif usuario["rol"] == 3:     
                    self.mostrar_menu_bibliotecario()
                elif usuario["rol"] == 4:     
                    self.mostrar_menu_estudiante()
            else:
                messagebox.showerror("Acceso Denegado", "Cédula o contraseña incorrectas.")

        btn_ingresar = tk.Button(self.contenedor_vista, text="Iniciar Sesión", font=('Segoe UI', 11, 'bold'),
                                 bg=COLOR_TEXTO_MAIN, fg="white", width=22, bd=0, cursor="hand2", command=verificar_credenciales)
        btn_ingresar.pack(pady=15)

        # AGREGADO: Etiqueta de versión en la pantalla de inicio de sesión (esquina inferior derecha)
        lbl_version_login = tk.Label(self.contenedor_vista, text="Version 1.0 BETA", 
                                     font=('Segoe UI', 9, 'bold'), bg=COLOR_FONDO, fg="#90A4AE")
        lbl_version_login.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    # =========================================================================
    # TABLERO PRINCIPAL - ADMINISTRADOR (DASHBOARD GRID)
    # =========================================================================
    def mostrar_menu_administrador(self):
        self.limpiar_pantalla()

        frame_header = tk.Frame(self.contenedor_vista, bg=COLOR_FONDO)
        frame_header.pack(fill=tk.X, pady=(10, 20))

        frame_titulos = tk.Frame(frame_header, bg=COLOR_FONDO)
        frame_titulos.pack(side=tk.LEFT)
        
        tk.Label(frame_titulos, text="SISTEMA DE GESTIÓN DE PRÉSTAMOS", 
                 font=('Segoe UI', 18, 'bold'), bg=COLOR_FONDO, fg=COLOR_TEXTO_MAIN).pack(anchor=tk.W)
        tk.Label(frame_titulos, text="UNEXCA - LOS APÓSTOLES DE PROYECTO", 
                 font=('Segoe UI', 11, 'bold'), bg=COLOR_FONDO, fg="#0288D1").pack(anchor=tk.W)

        frame_search = tk.Frame(frame_header, bg="white", bd=1, relief=tk.SOLID)
        frame_search.pack(side=tk.RIGHT, ipady=3, ipadx=5)
        
        tk.Label(frame_search, text="🔍", bg="white", fg="gray").pack(side=tk.LEFT, padx=5)
        entry_search = tk.Entry(frame_search, font=('Segoe UI', 10), bg="white", bd=0, width=25)
        entry_search.insert(0, "Buscar por Cédula...")
        entry_search.pack(side=tk.LEFT)

        frame_grid = tk.Frame(self.contenedor_vista, bg="white", bd=1, relief=tk.SOLID, padx=15, pady=15)
        frame_grid.pack(fill=tk.BOTH, expand=True)

        for i in range(3): frame_grid.columnconfigure(i, weight=1, uniform="group1")
        for j in range(2): frame_grid.rowconfigure(j, weight=1, uniform="group2")

        tarjetas = [
            {"texto": "Prestar/\nDevolver", "icono": "📘➡", "cmd": self.mostrar_vista_prestamos, "row": 0, "col": 0},
            {"texto": "Gestionar\nUsuarios", "icono": "⚙👤", "cmd": self.mostrar_submenu_usuarios, "row": 0, "col": 1},
            {"texto": "Gestionar\nRecursos", "icono": "📦📚", "cmd": self.mostrar_submenu_recursos, "row": 0, "col": 2},
            {"texto": "Ver\nMovimientos", "icono": "📊📈", "cmd": lambda: self.vista_listar_recursos(0), "row": 1, "col": 0},
            {"texto": "Reportes", "icono": "📋📊", "cmd": lambda: messagebox.showinfo("Módulo", "Reportes en Excel y PDF generándose en carpeta raíz."), "row": 1, "col": 1},
            {"texto": "Cerrar Sesión", "icono": "🚪🚪", "cmd": self.mostrar_login, "row": 1, "col": 2}
        ]

        for item in tarjetas:
            card = tk.Frame(frame_grid, bg=COLOR_TARJETA, cursor="hand2")
            card.grid(row=item["row"], column=item["col"], padx=10, pady=10, sticky="nsew")

            lbl_ico = tk.Label(card, text=item["icono"], font=('Segoe UI', 24), bg=COLOR_TARJETA, fg=COLOR_TEXTO_MAIN)
            lbl_ico.pack(pady=(15, 2))

            lbl_txt = tk.Label(card, text=item["texto"], font=('Segoe UI', 12, 'bold'), bg=COLOR_TARJETA, fg=COLOR_TEXTO_MAIN, justify=tk.CENTER)
            lbl_txt.pack(pady=(0, 15))

            def on_enter(e, frame=card, ico=lbl_ico, txt=lbl_txt):
                frame.config(bg=COLOR_TARJETA_HOVER)
                ico.config(bg=COLOR_TARJETA_HOVER)
                txt.config(bg=COLOR_TARJETA_HOVER)

            def on_leave(e, frame=card, ico=lbl_ico, txt=lbl_txt):
                frame.config(bg=COLOR_TARJETA)
                ico.config(bg=COLOR_TARJETA)
                txt.config(bg=COLOR_TARJETA)

            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            lbl_ico.bind("<Enter>", on_enter)
            lbl_txt.bind("<Enter>", on_enter)

            cmd_actual = item["cmd"]
            card.bind("<Button-1>", lambda e, cmd=cmd_actual: cmd())
            lbl_ico.bind("<Button-1>", lambda e, cmd=cmd_actual: cmd())
            lbl_txt.bind("<Button-1>", lambda e, cmd=cmd_actual: cmd())

        frame_footer = tk.Frame(self.contenedor_vista, bg=COLOR_FONDO)
        frame_footer.pack(fill=tk.X, pady=(15, 0))
        texto_pie = f"Rol: Administrador  |  Usuario: {self.usuario_actual['nombre'].upper()}  |  Equipo: Los Apóstoles"
        tk.Label(frame_footer, text=texto_pie, font=('Segoe UI', 9, 'bold'), bg=COLOR_FONDO, fg="#546E7A").pack(side=tk.LEFT)
        
        # AGREGADO: Versión a la derecha del footer
        tk.Label(frame_footer, text="Version 1.0 BETA", font=('Segoe UI', 9, 'bold'), bg=COLOR_FONDO, fg="#90A4AE").pack(side=tk.RIGHT)

    # =========================================================================
    # MÓDULO: PRÉSTAMOS Y DEVOLUCIONES (COMPARTIDO POR TODOS LOS ROLES)
    # =========================================================================
    def mostrar_vista_prestamos(self):
        self.limpiar_pantalla()
        
        tk.Label(self.contenedor_vista, text="MÓDULO DE TRANSACCIONES DE INVENTARIO", 
                 font=('Segoe UI', 14, 'bold'), bg=COLOR_FONDO, fg=COLOR_TEXTO_MAIN).pack(pady=(10, 5))
        
        estilo_pestañas = ttk.Style()
        estilo_pestañas.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=[10, 4])
        
        notebook = ttk.Notebook(self.contenedor_vista)
        notebook.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)

        pestana_prestamo = tk.Frame(notebook, bg="white", bd=1, relief=tk.SOLID)
        pestana_devolucion = tk.Frame(notebook, bg="white", bd=1, relief=tk.SOLID)
        
        notebook.add(pestana_prestamo, text=" 📘 SOLICITAR PRÉSTAMO ")
        notebook.add(pestana_devolucion, text=" ↩️ REALIZAR DEVOLUCIÓN ")

        # --- FLUJO 1: PESTAÑA DE PRÉSTAMOS ---
        recursos_inv = self.controlador.consultar_inventario()
        opciones_prestamo = []
        dicc_disponibilidad = {} 

        for rec in recursos_inv:
            try:
                partes_estado = rec["estado"].split()
                unidades = next(int(s) for s in partes_estado if s.isdigit())
            except StopIteration:
                unidades = 0

            if unidades > 0:
                texto_combo = f"{rec['id']}: {rec['nombre']} ({rec['tipo']}) [Disponibles: {unidades}]"
                opciones_prestamo.append(texto_combo)
                dicc_disponibilidad[rec['id']] = unidades

        tk.Label(pestana_prestamo, text="Seleccione el Recurso a Solicitar:", bg="white", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, padx=30, pady=(20,2))
        combo_p = ttk.Combobox(pestana_prestamo, values=opciones_prestamo, font=('Segoe UI', 11), state="readonly")
        combo_p.pack(fill=tk.X, padx=30, pady=5)
        
        frame_detalles_p = tk.Frame(pestana_prestamo, bg="white")
        frame_detalles_p.pack(fill=tk.X, padx=30, pady=10)

        frame_cant_p = tk.Frame(frame_detalles_p, bg="white")
        frame_cant_p.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(frame_cant_p, text="Cantidad:", bg="white", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        spin_cant_p = tk.Spinbox(frame_cant_p, from_=1, to=10, width=5, font=('Segoe UI', 11), state="readonly")
        spin_cant_p.pack(anchor=tk.W, pady=2)

        frame_sol_p = tk.Frame(frame_detalles_p, bg="white")
        frame_sol_p.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(20, 0))
        tk.Label(frame_sol_p, text="Nombre del Solicitante:", bg="white", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        entry_sol_p = tk.Entry(frame_sol_p, font=('Segoe UI', 11), bd=1, relief=tk.SOLID)
        entry_sol_p.insert(0, f"{self.usuario_actual['nombre'].upper()}")
        entry_sol_p.pack(fill=tk.X, pady=2)

        def update_limit(event):
            if not combo_p.get(): return
            id_sel = int(combo_p.get().split(":")[0])
            max_dispo = dicc_disponibilidad.get(id_sel, 1)
            spin_cant_p.config(from_=1, to=max_dispo)
        
        combo_p.bind("<<ComboboxSelected>>", update_limit)
        if opciones_prestamo:
            combo_p.current(0)
            update_limit(None)

        def ejecutar_prestamo():
            if not combo_p.get():
                messagebox.showerror("Error", "No hay recursos disponibles para prestar.")
                return
            id_rec = int(combo_p.get().split(":")[0])
            amount = int(spin_cant_p.get())
            solicitante = entry_sol_p.get().strip()

            if not solicitante:
                messagebox.showerror("Error", "Ingrese el nombre del solicitante.")
                return

            exito = True
            for _ in range(amount):
                if not self.controlador.registrar_prestamo(id_rec, solicitante, self.usuario_actual["rol"]):
                    exito = False
                    break

            if exito:
                messagebox.showinfo("Éxito", f"Se procesó el préstamo de {amount} unidad(es) de manera exitosa.")
                self.regresar_menu_segun_rol()
            else:
                messagebox.showerror("Error", "Error en persistencia. Verifique el stock.")

        tk.Button(pestana_prestamo, text="📘 Confirmar Solicitud de Préstamo", font=('Segoe UI', 11, 'bold'), 
                  bg="#2E7D32", fg="white", bd=0, cursor="hand2", command=ejecutar_prestamo).pack(pady=25)

        # --- FLUJO 2: PESTAÑA DE DEVOLUCIONES ---
        opciones_devolucion = []
        for rec in recursos_inv:
            texto_combo_d = f"{rec['id']}: {rec['nombre']} ({rec['tipo']})"
            opciones_devolucion.append(texto_combo_d)

        tk.Label(pestana_devolucion, text="Seleccione el Bien que tiene en su Poder para Reingresar:", bg="white", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, padx=30, pady=(20,2))
        combo_d = ttk.Combobox(pestana_devolucion, values=opciones_devolucion, font=('Segoe UI', 11), state="readonly")
        combo_d.pack(fill=tk.X, padx=30, pady=5)

        frame_detalles_d = tk.Frame(pestana_devolucion, bg="white")
        frame_detalles_d.pack(fill=tk.X, padx=30, pady=10)

        tk.Label(frame_detalles_d, text="Unidades a Devolver:", bg="white", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
        frame_spin_d = tk.Frame(frame_detalles_d, bg="white")
        frame_spin_d.pack(anchor=tk.W, pady=2)
        
        spin_cant_d = tk.Spinbox(frame_spin_d, from_=1, to=10, width=6, font=('Segoe UI', 11), state="readonly")
        spin_cant_d.pack(side=tk.LEFT)

        if opciones_devolucion: combo_d.current(0)

        def ejecutar_devolucion():
            if not combo_d.get(): return
            id_rec = int(combo_d.get().split(":")[0])
            amount = int(spin_cant_d.get())
            solicitante = entry_sol_p.get().strip() 

            exito = True
            for _ in range(amount):
                if not self.controlador.registrar_devolucion(id_rec, solicitante, self.usuario_actual["rol"]):
                    exito = False
                    break

            if exito:
                messagebox.showinfo("Éxito", f"Devolución de {amount} unidad(es) procesada de forma correcta.")
                self.regresar_menu_segun_rol()
            else:
                messagebox.showerror("Error", "No se pudo asentar el reingreso del recurso.")

        tk.Button(pestana_devolucion, text="↩️ Confirmar Reingreso / Devolución", font=('Segoe UI', 11, 'bold'), 
                  bg="#EF6C00", fg="white", bd=0, cursor="hand2", command=ejecutar_devolucion).pack(pady=35)

        tk.Button(self.contenedor_vista, text="❌ Volver al Menú Principal", font=('Segoe UI', 10, 'bold'), 
                  bg="gray", fg="white", command=self.regresar_menu_segun_rol).pack(pady=(10, 0))

    def regresar_menu_segun_rol(self):
        if self.usuario_actual["rol"] in (1, 2):
            self.mostrar_menu_administrador()
        elif self.usuario_actual["rol"] == 3:
            self.mostrar_menu_bibliotecario()
        elif self.usuario_actual["rol"] == 4:
            self.mostrar_menu_estudiante()

    # =========================================================================
    # TABLERO PRINCIPAL - BIBLIOTECARIO (Rol 3)
    # =========================================================================
    def mostrar_menu_bibliotecario(self):
        self.limpiar_pantalla()

        frame_header = tk.Frame(self.contenedor_vista, bg=COLOR_FONDO)
        frame_header.pack(fill=tk.X, pady=(10, 20))

        frame_titulos = tk.Frame(frame_header, bg=COLOR_FONDO)
        frame_titulos.pack(side=tk.LEFT)
        
        tk.Label(frame_titulos, text="SISTEMA DE GESTIÓN DE PRÉSTAMOS", 
                 font=('Segoe UI', 18, 'bold'), bg=COLOR_FONDO, fg=COLOR_TEXTO_MAIN).pack(anchor=tk.W)
        tk.Label(frame_titulos, text="PANEL CENTRAL DE BIBLIOTECA - UNEXCA", 
                 font=('Segoe UI', 11, 'bold'), bg=COLOR_FONDO, fg="#0097A7").pack(anchor=tk.W)

        frame_grid = tk.Frame(self.contenedor_vista, bg="white", bd=1, relief=tk.SOLID, padx=15, pady=15)
        frame_grid.pack(fill=tk.BOTH, expand=True)

        for i in range(2): frame_grid.columnconfigure(i, weight=1, uniform="group_bib")
        for j in range(2): frame_grid.rowconfigure(j, weight=1, uniform="group_bib")

        tarjetas = [
            {"texto": "Prestar / Devolver\nRecurso", "icono": "📘➡", "cmd": self.mostrar_vista_prestamos, "row": 0, "col": 0},
            {"texto": "Consultar Inventario\ny Catálogo", "icono": "🔍📦", "cmd": lambda: self.vista_listar_recursos(0), "row": 0, "col": 1},
            {"texto": "Historial de\nMovimientos", "icono": "📋📈", "cmd": lambda: self.vista_listar_recursos(1), "row": 1, "col": 0},
            {"texto": "Cerrar Sesión\nSegura", "icono": "🚪🚪", "cmd": self.mostrar_login, "row": 1, "col": 1}
        ]

        for item in tarjetas:
            card = tk.Frame(frame_grid, bg=COLOR_TARJETA, cursor="hand2")
            card.grid(row=item["row"], column=item["col"], padx=15, pady=15, sticky="nsew")

            lbl_ico = tk.Label(card, text=item["icono"], font=('Segoe UI', 26), bg=COLOR_TARJETA, fg=COLOR_TEXTO_MAIN)
            lbl_ico.pack(pady=(20, 2))

            lbl_txt = tk.Label(card, text=item["texto"], font=('Segoe UI', 12, 'bold'), bg=COLOR_TARJETA, fg=COLOR_TEXTO_MAIN, justify=tk.CENTER)
            lbl_txt.pack(pady=(0, 20))

            def on_enter(e, frame=card, ico=lbl_ico, txt=lbl_txt):
                frame.config(bg=COLOR_TARJETA_HOVER)
                ico.config(bg=COLOR_TARJETA_HOVER)
                txt.config(bg=COLOR_TARJETA_HOVER)

            def on_leave(e, frame=card, ico=lbl_ico, txt=lbl_txt):
                frame.config(bg=COLOR_TARJETA)
                ico.config(bg=COLOR_TARJETA)
                txt.config(bg=COLOR_TARJETA)

            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            lbl_ico.bind("<Enter>", on_enter)
            lbl_txt.bind("<Enter>", on_enter)

            cmd_actual = item["cmd"]
            card.bind("<Button-1>", lambda e, cmd=cmd_actual: cmd())
            lbl_ico.bind("<Button-1>", lambda e, cmd=cmd_actual: cmd())
            lbl_txt.bind("<Button-1>", lambda e, cmd=cmd_actual: cmd())

        frame_footer = tk.Frame(self.contenedor_vista, bg=COLOR_FONDO)
        frame_footer.pack(fill=tk.X, pady=(15, 0))
        texto_pie = f"Rol: Bibliotecario  |  Usuario: {self.usuario_actual['nombre'].upper()}  |  Sede: Casco Histórico de Petare"
        tk.Label(frame_footer, text=texto_pie, font=('Segoe UI', 9, 'bold'), bg=COLOR_FONDO, fg="#546E7A").pack(side=tk.LEFT)
        
        # AGREGADO: Versión a la derecha del footer
        tk.Label(frame_footer, text="Version 1.0 BETA", font=('Segoe UI', 9, 'bold'), bg=COLOR_FONDO, fg="#90A4AE").pack(side=tk.RIGHT)

    # =========================================================================
    # TABLERO PRINCIPAL - ESTUDIANTE (Rol 4)
    # =========================================================================
    def mostrar_menu_estudiante(self):
        self.limpiar_pantalla()

        frame_header = tk.Frame(self.contenedor_vista, bg=COLOR_FONDO)
        frame_header.pack(fill=tk.X, pady=(10, 20))

        frame_titulos = tk.Frame(frame_header, bg=COLOR_FONDO)
        frame_titulos.pack(side=tk.LEFT)
        
        tk.Label(frame_titulos, text="SISTEMA DE GESTIÓN DE PRÉSTAMOS", 
                 font=('Segoe UI', 18, 'bold'), bg=COLOR_FONDO, fg=COLOR_TEXTO_MAIN).pack(anchor=tk.W)
        tk.Label(frame_titulos, text="MÓDULO ESTUDIANTIL - UNEXCA", 
                 font=('Segoe UI', 11, 'bold'), bg=COLOR_FONDO, fg="#43A047").pack(anchor=tk.W)

        frame_grid = tk.Frame(self.contenedor_vista, bg="white", bd=1, relief=tk.SOLID, padx=15, pady=15)
        frame_grid.pack(fill=tk.BOTH, expand=True)

        for i in range(3): frame_grid.columnconfigure(i, weight=1, uniform="group_est")
        frame_grid.rowconfigure(0, weight=1)

        tarjetas = [
            {"texto": "Consultar Disponibilidad\ny Mis Movimientos", "icono": "📖🔍", "cmd": lambda: self.vista_listar_recursos(0), "row": 0, "col": 0},
            {"texto": "Solicitar Préstamo\ny Devoluciones", "icono": "📝🔄", "cmd": self.mostrar_vista_prestamos, "row": 0, "col": 1},
            {"texto": "Cerrar Sesión\nAcadémica", "icono": "🚪↩️", "cmd": self.mostrar_login, "row": 0, "col": 2}
        ]

        for item in tarjetas:
            card = tk.Frame(frame_grid, bg=COLOR_TARJETA, cursor="hand2")
            card.grid(row=item["row"], column=item["col"], padx=10, pady=30, sticky="nsew")

            lbl_ico = tk.Label(card, text=item["icono"], font=('Segoe UI', 28), bg=COLOR_TARJETA, fg=COLOR_TEXTO_MAIN)
            lbl_ico.pack(pady=(25, 5))

            lbl_txt = tk.Label(card, text=item["texto"], font=('Segoe UI', 11, 'bold'), bg=COLOR_TARJETA, fg=COLOR_TEXTO_MAIN, justify=tk.CENTER)
            lbl_txt.pack(pady=(0, 25))

            def on_enter(e, frame=card, ico=lbl_ico, txt=lbl_txt):
                frame.config(bg=COLOR_TARJETA_HOVER)
                ico.config(bg=COLOR_TARJETA_HOVER)
                txt.config(bg=COLOR_TARJETA_HOVER)

            def on_leave(e, frame=card, ico=lbl_ico, txt=lbl_txt):
                frame.config(bg=COLOR_TARJETA)
                ico.config(bg=COLOR_TARJETA)
                txt.config(bg=COLOR_TARJETA)

            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            lbl_ico.bind("<Enter>", on_enter)
            lbl_txt.bind("<Enter>", on_enter)

            cmd_actual = item["cmd"]
            card.bind("<Button-1>", lambda e, cmd=cmd_actual: cmd())
            lbl_ico.bind("<Button-1>", lambda e, cmd=cmd_actual: cmd())
            lbl_txt.bind("<Button-1>", lambda e, cmd=cmd_actual: cmd())

        frame_footer = tk.Frame(self.contenedor_vista, bg=COLOR_FONDO)
        frame_footer.pack(fill=tk.X, pady=(15, 0))
        texto_pie = f"Rol: Alumno UNEXCA  |  Usuario: {self.usuario_actual['nombre'].upper()}  |  Acceso Total Habilitado"
        tk.Label(frame_footer, text=texto_pie, font=('Segoe UI', 9, 'bold'), bg=COLOR_FONDO, fg="#546E7A").pack(side=tk.LEFT)
        
        # AGREGADO: Versión a la derecha del footer
        tk.Label(frame_footer, text="Version 1.0 BETA", font=('Segoe UI', 9, 'bold'), bg=COLOR_FONDO, fg="#90A4AE").pack(side=tk.RIGHT)

    # =========================================================================
    # GESTIONAR USUARIOS (CRUD)
    # =========================================================================
    def mostrar_submenu_usuarios(self):
        self.limpiar_pantalla()
        tk.Label(self.contenedor_vista, text="REGISTRAR NUEVO USUARIO EN SISTEMA", font=('Segoe UI', 14, 'bold'), bg=COLOR_FONDO, fg=COLOR_TEXTO_MAIN).pack(pady=15)
        
        frame_form = tk.Frame(self.contenedor_vista, bg="white", bd=1, relief=tk.SOLID)
        frame_form.pack(pady=5, padx=100, fill=tk.X, ipady=10)

        tk.Label(frame_form, text="Cédula:", bg="white").pack(anchor=tk.W, padx=20)
        ent_ced = tk.Entry(frame_form, font=('Segoe UI', 10), bd=1, relief=tk.SOLID); ent_ced.pack(fill=tk.X, padx=20, pady=2)

        tk.Label(frame_form, text="Nombre Completo:", bg="white").pack(anchor=tk.W, padx=20)
        ent_nom = tk.Entry(frame_form, font=('Segoe UI', 10), bd=1, relief=tk.SOLID); ent_nom.pack(fill=tk.X, padx=20, pady=2)

        tk.Label(frame_form, text="Rol del Sistema:", bg="white").pack(anchor=tk.W, padx=20)
        combo_rol = ttk.Combobox(frame_form, values=["1: Admin", "2: Sistem", "3: UserBiblio", "4: UserBasic"], state="readonly")
        combo_rol.pack(fill=tk.X, padx=20, pady=2); combo_rol.current(3)

        tk.Label(frame_form, text="Contraseña de Acceso:", bg="white").pack(anchor=tk.W, padx=20)
        ent_pas = tk.Entry(frame_form, font=('Segoe UI', 10), bd=1, relief=tk.SOLID, show="*"); ent_pas.pack(fill=tk.X, padx=20, pady=2)

        tk.Label(frame_form, text="Correo Electrónico Corporativo:", bg="white").pack(anchor=tk.W, padx=20)
        ent_mai = tk.Entry(frame_form, font=('Segoe UI', 10), bd=1, relief=tk.SOLID); ent_mai.pack(fill=tk.X, padx=20, pady=2)

        def guardar_usuario():
            c, n, p, m = ent_ced.get().strip(), ent_nom.get().strip(), ent_pas.get().strip(), ent_mai.get().strip()
            r = int(combo_rol.get().split(":")[0])
            if not c or not n or not p:
                messagebox.showerror("Error", "Cédula, Nombre y Clave son obligatorios.")
                return
            if self.controlador.registrar_usuario(c, n, r, p, m):
                messagebox.showinfo("Éxito", f"Usuario '{n}' persistido de forma segura en SQLite.")
                self.mostrar_menu_administrador()

        tk.Button(self.contenedor_vista, text="💾 Registrar Usuario", font=('Segoe UI', 11, 'bold'), bg=COLOR_TEXTO_MAIN, fg="white", command=guardar_usuario).pack(pady=10)
        tk.Button(self.contenedor_vista, text="⬅️ Cancelar", font=('Segoe UI', 10), bg="gray", fg="white", command=self.mostrar_menu_administrador).pack()

    # =========================================================================
    # GESTIONAR RECURSOS (FACTORY MÉTODO)
    # =========================================================================
    def mostrar_submenu_recursos(self):
        self.limpiar_pantalla()
        tk.Label(self.contenedor_vista, text="CREACIÓN DE RECURSOS POR MÉTODO FACTORY", font=('Segoe UI', 14, 'bold'), bg=COLOR_FONDO, fg=COLOR_TEXTO_MAIN).pack(pady=15)
        
        frame_form = tk.Frame(self.contenedor_vista, bg="white", bd=1, relief=tk.SOLID)
        frame_form.pack(pady=10, padx=120, fill=tk.X, ipady=15)

        tk.Label(frame_form, text="Tipo de Bien (Factory Key):", bg="white", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, padx=20)
        combo_tipo = ttk.Combobox(frame_form, values=["Libro", "Laptop", "Audiovisual"], state="readonly")
        combo_tipo.pack(fill=tk.X, padx=20, pady=5); combo_tipo.current(0)

        tk.Label(frame_form, text="Título / Descripción del Bien:", bg="white", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, padx=20)
        ent_desc = tk.Entry(frame_form, font=('Segoe UI', 11), bd=1, relief=tk.SOLID)
        ent_desc.pack(fill=tk.X, padx=20, pady=5)

        def instanciar_fabrica():
            t = combo_tipo.get().lower()
            d = ent_desc.get().strip()
            if not d:
                messagebox.showerror("Campos Vacíos", "Escriba una descripción para el recurso.")
                return
            
            detalles_simulados = {"meta": "Instancia_Factory_UNEXCA", "origen": "Academico"}
            
            if self.controlador.registrar_recurso(t, d, detalles_simulados):
                messagebox.showinfo("Factory Method", f"Bien '{d}' instanciado y registrado con stock inicial.")
                self.mostrar_menu_administrador()

        tk.Button(self.contenedor_vista, text="🏗️ Instanciar en Fábrica", font=('Segoe UI', 11, 'bold'), bg=COLOR_TEXTO_MAIN, fg="white", command=instanciar_fabrica).pack(pady=10)
        tk.Button(self.contenedor_vista, text="⬅️ Cancelar", font=('Segoe UI', 10), bg="gray", fg="white", command=self.mostrar_menu_administrador).pack()

    # =========================================================================
    # INVENTARIO GLOBAL Y MOVIMIENTOS SMART (CON SELECCIÓN DE PESTAÑA DINÁMICA)
    # =========================================================================
    def vista_listar_recursos(self, pestana_inicial=0):
        self.limpiar_pantalla()
        
        # --- Cabecera Fija ---
        tk.Label(self.contenedor_vista, text="PANEL DE AUDITORÍA Y CONSULTA EN TIEMPO REAL", 
                 font=('Segoe UI', 14, 'bold'), bg=COLOR_FONDO, fg=COLOR_TEXTO_MAIN).pack(pady=(10, 5))
        
        # --- ZONA INFERIOR FIJA PARA EL BOTÓN VOLVER ---
        frame_bottom_bar = tk.Frame(self.contenedor_vista, bg=COLOR_FONDO)
        frame_bottom_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        tk.Button(frame_bottom_bar, text="⬅️ Volver al Tablero Principal", font=('Segoe UI', 10, 'bold'), 
          bg="gray", fg="white", command=self.regresar_menu_segun_rol, cursor="hand2",
          padx=15, pady=5).pack(pady=5)

        # --- SISTEMA DE PESTAÑAS (NOTEBOOK) ---
        estilo_pestañas = ttk.Style()
        estilo_pestañas.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=[10, 4])
        
        notebook = ttk.Notebook(self.contenedor_vista)
        notebook.pack(fill=tk.BOTH, expand=True, padx=30, pady=(5, 5))

        pestana_inventario = tk.Frame(notebook, bg="white", bd=1, relief=tk.SOLID)
        pestana_historial = tk.Frame(notebook, bg="white", bd=1, relief=tk.SOLID)
        
        notebook.add(pestana_inventario, text=" 📦 INVENTARIO ACTUAL ")
        
        rol_sesion = self.usuario_actual.get("rol") if self.usuario_actual else 4
        titulo_historial = " 📊 HISTORIAL GLOBAL DE AUDITORÍA " if rol_sesion in (1, 2, 3) else " 📊 MI HISTORIAL DE MOVIMIENTOS "
        notebook.add(pestana_historial, text=titulo_historial)

        # Foco automático en la pestaña deseada según el origen del click
        notebook.select(pestana_inicial)

        # =========================================================================
        # PESTAÑA 1: INVENTARIO DE RECURSOS (VISTA GLOBAL)
        # =========================================================================
        frame_tabla_inv = tk.Frame(pestana_inventario)
        frame_tabla_inv.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas_inv = ('id', 'tipo', 'nombre', 'estado', 'detalles')
        tabla_inv = ttk.Treeview(frame_tabla_inv, columns=columnas_inv, show='headings')
        
        tabla_inv.heading('id', text='ID')
        tabla_inv.heading('tipo', text='Tipo de Recurso')
        tabla_inv.heading('nombre', text='Nombre / Título')
        tabla_inv.heading('estado', text='Unidades Físicas')
        tabla_inv.heading('detalles', text='Metadatos Factory')
        
        tabla_inv.column('id', width=40, anchor=tk.CENTER)
        tabla_inv.column('tipo', width=90, anchor=tk.CENTER)
        tabla_inv.column('nombre', width=200)
        tabla_inv.column('estado', width=130, anchor=tk.CENTER)
        tabla_inv.column('detalles', width=260)
        
        tabla_inv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_inv = ttk.Scrollbar(frame_tabla_inv, orient=tk.VERTICAL, command=tabla_inv.yview)
        tabla_inv.configure(yscrollcommand=scroll_inv.set)
        scroll_inv.pack(side=tk.RIGHT, fill=tk.Y)

        recursos = self.controlador.consultar_inventario()
        for r in recursos:
            tabla_inv.insert('', tk.END, values=(r['id'], r['tipo'], r['nombre'], r['estado'], r['detalles']))

        def borrar_item():
            item_sel = tabla_inv.selection()
            if not item_sel:
                messagebox.showwarning("Atención", "Seleccione un recurso de la lista para eliminar.")
                return
            valores = tabla_inv.item(item_sel, 'values')
            id_borrar = valores[0]
            if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el recurso ID {id_borrar}?"):
                if self.controlador.eliminar_recurso(id_borrar):
                    messagebox.showinfo("Borrado", "Recurso removido del sistema.")
                    self.vista_listar_recursos()

        frame_acciones_inv = tk.Frame(pestana_inventario, bg="white")
        frame_acciones_inv.pack(fill=tk.X, pady=5, padx=10)
        
        if self.usuario_actual["rol"] in (1, 2):
            tk.Button(frame_acciones_inv, text="🗑️ Eliminar Seleccionado", font=('Segoe UI', 9, 'bold'), 
                      bg="#C62828", fg="white", command=borrar_item).pack(side=tk.LEFT, pady=5)

        # =========================================================================
        # PESTAÑA 2: HISTORIAL INDIVIDUAL / GLOBAL DE MOVIMIENTOS
        # =========================================================================
        frame_tabla_hist = tk.Frame(pestana_historial)
        frame_tabla_hist.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas_hist = ('fecha', 'tipo_acc', 'id_rec', 'recurso', 'operador')
        tabla_hist = ttk.Treeview(frame_tabla_hist, columns=columnas_hist, show='headings')
        
        tabla_hist.heading('fecha', text='Fecha / Hora')
        tabla_hist.heading('tipo_acc', text='Operación')
        tabla_hist.heading('id_rec', text='ID Bien')
        tabla_hist.heading('recurso', text='Descripción del Recurso')
        tabla_hist.heading('operador', text='Asignado a / Registrado por')
        
        tabla_hist.column('fecha', width=140, anchor=tk.CENTER)
        tabla_hist.column('tipo_acc', width=110, anchor=tk.CENTER)
        tabla_hist.column('id_rec', width=60, anchor=tk.CENTER)
        tabla_hist.column('recurso', width=220)
        tabla_hist.column('operador', width=180, anchor=tk.CENTER)
        
        tabla_hist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_hist = ttk.Scrollbar(frame_tabla_hist, orient=tk.VERTICAL, command=tabla_hist.yview)
        tabla_hist.configure(yscrollcommand=scroll_hist.set)
        scroll_hist.pack(side=tk.RIGHT, fill=tk.Y)

        usuario_sesion = self.usuario_actual['nombre'].upper()

        if rol_sesion in (1, 2, 3):
            if hasattr(self.controlador, 'consultar_inventario_completo_movimientos'):
                movimientos = self.controlador.consultar_inventario_completo_movimientos()
            else:
                movimientos = self.controlador.consultar_historial_usuario("")
            texto_pie_tabla = "Mostrando el registro total de transacciones de la base de datos (Modo Auditor)."
        else:
            movimientos = self.controlador.consultar_historial_usuario(self.usuario_actual["nombre"])
            texto_pie_tabla = f"Mostrando transacciones vinculadas estrictamente a: {usuario_sesion}"
        
        if movimientos:
            for mov in movimientos:
                accion_real = mov.get('tipo_accion') or mov.get('Tipodeaccion') or 'Prestamo'
                nombre_real = mov.get('nombre_recurso') or mov.get('descripcion') or 'Objeto UNEXCA'
                user_m = mov.get('usuario') or mov.get('operador') or usuario_sesion
                id_r = mov.get('id_recurso') or '1'
                fecha_m = mov.get('fecha') or '09/06/2026'

                if "PRES" in accion_real.upper():
                    tag_operacion = "📘 PRÉSTAMO"
                else:
                    tag_operacion = "↩️ DEVOLUCIÓN"
                
                tabla_hist.insert('', tk.END, values=(
                    fecha_m,        
                    tag_operacion, 
                    id_r, 
                    nombre_real, 
                    user_m.upper()
                ))

        tk.Label(pestana_historial, text=texto_pie_tabla, 
                 font=('Segoe UI', 9, 'italic'), bg="white", fg="#546E7A").pack(pady=5)

# --- INICIALIZADOR DE SISTEMA COHESIVO ---
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    
    from src.database.conexion import DatabaseManager
    from src.database.inventario_controller import InventarioController
    
    db_manager = DatabaseManager()
    controlador_sistema = InventarioController(db_manager)
    
    root = tk.Tk()
    app = Aplicacion(root, controlador_sistema)
    root.mainloop()