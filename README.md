# 🏛️ Library-Factory UNEXCA: Sistema de Gestión de Préstamos

## Descripción
**Library-Factory UNEXCA** (desarrollado por el equipo *Los Apóstoles*) es una solución de ingeniería de software diseñada para la administración, préstamo y auditoría en tiempo real de los bienes e inventario de la universidad (Libros, Laptops y Equipos Audiovisuales). 

El sistema implementa de forma rigurosa el patrón creacional **Factory Method** para garantizar una instanciación dinámica, limpia y escalable de los recursos, asegurando el cumplimiento del principio Abierto/Cerrado (SOLID). Esta versión introduce una arquitectura robusta de tres capas conectada a persistencia relacional y una interfaz de usuario inteligente basada en roles.

---

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.x
* **Interfaz Gráfica:** Tkinter (Con diseño optimizado *Grid Dashboard*)
* **Persistencia:** SQLite 3 (Base de datos relacional integrada)
* **Control de Versiones:** Git / GitHub
* **Metodología:** Desarrollo Ágil (Scrum)
* **Estado Actual:** `Versión 1.0 BETA` 

---

## 🏗️ Arquitectura del Proyecto (Módulos de Tres Capas)

El proyecto sigue una estricta separación de responsabilidades para aislar la interfaz gráfica de la lógica de negocio y los accesos SQL:

📁 library_factory_unexca/
📁 data/
   biblioteca.db
📁 src/
   📁 database/
      conexion.py                 # Capa de Datos: Inicialización y consultas seguras en SQLite
      inventario_controller.py    # Capa de Negocio: Controlador lógico de flujos y transacciones

   📁 factory/
      resource.py                 # Patrón Creacional: Implementación del Factory Method
LICENSE                           
REDME                             # Documentacion del Proyecto
front_menus                       # Font del Proyecto

---

## ⚙️ Características Clave Implementadas

1.  **Fábrica de Recursos (Factory Method):** Centralización de la creación de objetos (`Libro`, `Laptop`, `Audiovisual`) mediante una llave (*Factory Key*), guardando metadatos estructurados en formato JSON dentro de la base de datos relacional.
2.  **Seguridad por Roles:** El sistema autentica mediante Cédula e identifica automáticamente el privilegio del usuario para desplegar vistas específicas:
    * **Administrador:** Acceso total, instanciación en fábrica de recursos, gestión CRUD de usuarios y auditoría global.
    * **Bibliotecario:** Operación exprés orientada a transacciones y consulta de inventario.
    * **Estudiante:** Panel protegido y confidencial restringido únicamente a sus movimientos personales.
3.  **Panel de Auditoría Dinámico:** Interfaz centralizada con sistema de pestañas (`Notebook`) y redirección inteligente que evita la duplicidad de pantallas y optimiza la navegación.
4.  **Diseño Cohesivo y Profesional:** Inclusión visual de la etiqueta `Version 1.0 BETA` en el Login y barras de pie de página de todos los menús del sistema.

---

## 👥 Equipo (LOS APÓSTOLES)

* **Líder de Equipo:**
    * Luis Arturo Silva Rollin — V-28.101.742
* **Líderes de Desarrollo:**
    * José Miguel Niño Gil — V-29.909.282
    * Deninson José Godoy Celis — V-28.158.313
* **Equipo de Pruebas:**
    * Manuel Téllez — V-20.027.142
    * Manuel Jesús Noriega López — V-25.216.071
* **Equipo de Documentarion:**
    * Yuseily Nathaly Valero Albarrán — V-31.660.944
* **Equipo de Desarrollo (Integrantes):**
    * Luis Arturo Silva Rollin — V-28.101.742
    * Manuel Jesús Noriega López — V-25.216.071
    * Manuel Téllez — V-20.027.142
    * José Miguel Niño Gil — V-29.909.282
    * Yuseily Nathaly Valero Albarrán — V-31.660.944
    * Deninson José Godoy Celis — V-28.158.313

---
*Trayecto II-I de Informática — Universidad Nacional Experimental de la Gran Caracas (UNEXCA), Sede La Floresta.*
