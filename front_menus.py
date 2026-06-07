import tkinter as tk
from tkinter import messagebox, ttk

# Colores en azul (diferentes tonalidades)
COLOR_FONDO = "#E3F2FD"      # Azul muy claro (fondo principal)
COLOR_BOTON = "#1976D2"      # Azul medio intenso (botones)
COLOR_BOTON_HOVER = "#1565C0" # Azul más oscuro (hover)
COLOR_TEXTO_BOTON = "white"  # Texto blanco en botones
COLOR_TITULO = "#0D47A1"     # Azul muy oscuro (títulos)
COLOR_FRAME = "#BBDEFB"      # Azul claro para frames secundarios
COLOR_SUBMENU = "#90CAF9"    # Azul intermedio para submenús

# Configuración global de estilos
def configurar_estilos():
    estilo = ttk.Style()
    estilo.theme_use('clam')
    estilo.configure('TLabel', background=COLOR_FONDO, foreground=COLOR_TITULO, font=('Segoe UI', 10))
    estilo.configure('TButton', background=COLOR_BOTON, foreground=COLOR_TEXTO_BOTON,
                     font=('Segoe UI', 10, 'bold'), borderwidth=0, focuscolor='none')
    estilo.map('TButton', background=[('active', COLOR_BOTON_HOVER)])

# --- Funciones placeholder para las acciones ---
def mostrar_mensaje(titulo, mensaje):
    messagebox.showinfo(titulo, mensaje)

# --- Menú Estudiante ---
def menu_estudiante():
    ventana = tk.Toplevel()
    ventana.title("Menú Estudiante")
    ventana.geometry("500x450")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    # Centrar la ventana
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

    tk.Label(ventana, text="MENÚ ESTUDIANTE", font=('Segoe UI', 16, 'bold'),
             bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=20)

    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.pack(expand=True)

    opciones = [
        ("1. Solicitar un préstamo", lambda: mostrar_mensaje("Préstamo", "Función: Solicitar préstamo")),
        ("2. Entregar un préstamo", lambda: mostrar_mensaje("Devolución", "Función: Entregar préstamo")),
        ("3. Consultar inventario", lambda: mostrar_mensaje("Inventario", "Función: Consultar inventario")),
        ("4. Estado de mis préstamos", lambda: mostrar_mensaje("Mis préstamos", "Función: Estado de mis préstamos")),
        ("5. Salir", ventana.destroy)
    ]

    for texto, comando in opciones:
        btn = tk.Button(frame_botones, text=texto, font=('Segoe UI', 11),
                        bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, activebackground=COLOR_BOTON_HOVER,
                        activeforeground="white", width=30, height=1, command=comando)
        btn.pack(pady=8)
        # Efecto hover manual
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLOR_BOTON_HOVER))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_BOTON))

# --- Menú Bibliotecario/Docente ---
def menu_bibliotecario():
    ventana = tk.Toplevel()
    ventana.title("Menú Bibliotecario/Docente")
    ventana.geometry("500x450")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    # Centrar
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

    tk.Label(ventana, text="MENÚ BIBLIOTECARIO/DOCENTE", font=('Segoe UI', 14, 'bold'),
             bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=20)

    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.pack(expand=True)

    opciones = [
        ("1. Registrar préstamo", lambda: mostrar_mensaje("Registrar préstamo", "Función: Registrar préstamo")),
        ("2. Registrar devolución", lambda: mostrar_mensaje("Registrar devolución", "Función: Registrar devolución")),
        ("3. Consultar estado de préstamos", lambda: mostrar_mensaje("Estado préstamos", "Función: Consultar estado")),
        ("4. Consultar inventario", lambda: mostrar_mensaje("Inventario", "Función: Consultar inventario")),
        ("5. Salir", ventana.destroy)
    ]

    for texto, comando in opciones:
        btn = tk.Button(frame_botones, text=texto, font=('Segoe UI', 11),
                        bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, activebackground=COLOR_BOTON_HOVER,
                        activeforeground="white", width=30, height=1, command=comando)
        btn.pack(pady=8)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLOR_BOTON_HOVER))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_BOTON))

# --- Submenús del Administrador ---
def submenu_gestionar_usuarios():
    ventana = tk.Toplevel()
    ventana.title("Gestionar Usuarios")
    ventana.geometry("450x350")
    ventana.configure(bg=COLOR_SUBMENU)
    ventana.resizable(False, False)

    tk.Label(ventana, text="GESTIONAR USUARIOS", font=('Segoe UI', 14, 'bold'),
             bg=COLOR_SUBMENU, fg=COLOR_TITULO).pack(pady=20)

    opciones = [
        ("a. Crear usuario", lambda: mostrar_mensaje("Crear usuario", "Función: Crear usuario")),
        ("b. Editar usuario", lambda: mostrar_mensaje("Editar usuario", "Función: Editar usuario")),
        ("c. Eliminar usuario", lambda: mostrar_mensaje("Eliminar usuario", "Función: Eliminar usuario")),
        ("d. Listar usuarios", lambda: mostrar_mensaje("Listar usuarios", "Función: Listar usuarios")),
        ("Volver", ventana.destroy)
    ]

    for texto, comando in opciones:
        btn = tk.Button(ventana, text=texto, font=('Segoe UI', 11),
                        bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, activebackground=COLOR_BOTON_HOVER,
                        activeforeground="white", width=25, height=1, command=comando)
        btn.pack(pady=6)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLOR_BOTON_HOVER))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_BOTON))

def submenu_gestionar_recursos():
    ventana = tk.Toplevel()
    ventana.title("Gestionar Recursos")
    ventana.geometry("450x350")
    ventana.configure(bg=COLOR_SUBMENU)
    ventana.resizable(False, False)

    tk.Label(ventana, text="GESTIONAR RECURSOS", font=('Segoe UI', 14, 'bold'),
             bg=COLOR_SUBMENU, fg=COLOR_TITULO).pack(pady=20)

    opciones = [
        ("a. Agregar recurso", lambda: mostrar_mensaje("Agregar recurso", "Función: Agregar recurso")),
        ("b. Editar recurso", lambda: mostrar_mensaje("Editar recurso", "Función: Editar recurso")),
        ("c. Eliminar recurso", lambda: mostrar_mensaje("Eliminar recurso", "Función: Eliminar recurso")),
        ("d. Listar recursos", lambda: mostrar_mensaje("Listar recursos", "Función: Listar recursos")),
        ("Volver", ventana.destroy)
    ]

    for texto, comando in opciones:
        btn = tk.Button(ventana, text=texto, font=('Segoe UI', 11),
                        bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, activebackground=COLOR_BOTON_HOVER,
                        activeforeground="white", width=25, height=1, command=comando)
        btn.pack(pady=6)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLOR_BOTON_HOVER))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_BOTON))

def ver_estadisticas():
    stats = "📊 ESTADÍSTICAS\n\n• Total de préstamos activos: 0\n• Total de usuarios registrados: 0\n• Total de recursos disponibles: 0"
    messagebox.showinfo("Estadísticas", stats)

# --- Menú Administrador ---
def menu_administrador():
    ventana = tk.Toplevel()
    ventana.title("Menú Administrador")
    ventana.geometry("550x550")
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    # Centrar
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

    tk.Label(ventana, text="MENÚ ADMINISTRADOR", font=('Segoe UI', 16, 'bold'),
             bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=20)

    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.pack(expand=True)

    opciones = [
        ("1. Registrar préstamo", lambda: mostrar_mensaje("Registrar préstamo", "Función: Registrar préstamo")),
        ("2. Registrar devolución", lambda: mostrar_mensaje("Registrar devolución", "Función: Registrar devolución")),
        ("3. Consultar estado de préstamos", lambda: mostrar_mensaje("Estado préstamos", "Función: Consultar estado")),
        ("4. Consultar inventario", lambda: mostrar_mensaje("Inventario", "Función: Consultar inventario")),
        ("5. Gestionar usuarios", submenu_gestionar_usuarios),
        ("6. Gestionar recursos", submenu_gestionar_recursos),
        ("7. Ver estadísticas", ver_estadisticas),
        ("8. Salir", ventana.destroy)
    ]

    for texto, comando in opciones:
        btn = tk.Button(frame_botones, text=texto, font=('Segoe UI', 11),
                        bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, activebackground=COLOR_BOTON_HOVER,
                        activeforeground="white", width=35, height=1, command=comando)
        btn.pack(pady=6)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLOR_BOTON_HOVER))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_BOTON))

# --- Menú Principal ---
class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Préstamos")
        self.root.geometry("550x450")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)

        # Centrar ventana principal
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')

        # Título
        tk.Label(self.root, text="SISTEMA DE GESTIÓN DE PRÉSTAMOS",
                 font=('Segoe UI', 18, 'bold'), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=30)

        # Subtítulo
        tk.Label(self.root, text="Seleccione su tipo de usuario",
                 font=('Segoe UI', 12), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=5)

        frame_botones = tk.Frame(self.root, bg=COLOR_FONDO)
        frame_botones.pack(expand=True)

        # Botones principales
        botones = [
            ("👨‍🎓 Acceder como ESTUDIANTE", menu_estudiante),
            ("📚 Acceder como BIBLIOTECARIO/DOCENTE", menu_bibliotecario),
            ("🔧 Acceder como ADMINISTRADOR", menu_administrador),
            ("🚪 Salir del programa", self.root.quit)
        ]

        for texto, comando in botones:
            btn = tk.Button(frame_botones, text=texto, font=('Segoe UI', 12, 'bold'),
                            bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, activebackground=COLOR_BOTON_HOVER,
                            activeforeground="white", width=35, height=2, command=comando)
            btn.pack(pady=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLOR_BOTON_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_BOTON))

        # Crédito al pie
        tk.Label(self.root, text="© Sistema de Préstamos - Todos los derechos reservados",
                 font=('Segoe UI', 8), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(side=tk.BOTTOM, pady=10)

# --- Punto de entrada ---
if __name__ == "__main__":
    root = tk.Tk()
    configurar_estilos()
    app = Aplicacion(root)
    root.mainloop()