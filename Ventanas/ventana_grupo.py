import tkinter as tk
from tkinter import ttk, messagebox
from Grupo.eliminar_grupo import eliminar_grupo, eliminar_todos_grupos
from Grupo.agregar_grupo import agregar_grupo

class VentanaGrupo:
    def __init__(self, root, comando_modificar=None, comando_buscar=None):
        self.root = root
        # Guardamos las referencias a las funciones que vienen de afuera
        self.comando_modificar = comando_modificar
        self.comando_buscar = comando_buscar
        
        self.root.title("Admon Grupo")
        self.root.geometry("450x450")
        
        # --- SECCIÓN SUPERIOR: INPUTS Y BOTONES CRUD ---
        frame_superior = tk.Frame(self.root, padx=10, pady=10)
        frame_superior.pack(fill="x")

        # Labels e Inputs (Izquierda)
        tk.Label(frame_superior, text="Clave:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.ent_clave = tk.Entry(frame_superior, width=25)
        self.ent_clave.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_superior, text="Nombre:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.ent_nombre = tk.Entry(frame_superior, width=25)
        self.ent_nombre.grid(row=1, column=1, padx=5, pady=5)

        # Botones CRUD (Derecha)
        # El botón buscar llama a la función local que luego llama al controlador
        self.btn_buscar = tk.Button(frame_superior, text="Buscar", width=12, command=self.click_buscar)
        self.btn_buscar.grid(row=0, column=2, padx=10)

        self.btn_limpiar = tk.Button(frame_superior, text="Limpiar", width=12, command=self.limpiar_campos)
        self.btn_limpiar.grid(row=1, column=2, padx=10)

        self.btn_eliminar = tk.Button(frame_superior, text="Eliminar", width=12,command=self.eliminar)
        self.btn_eliminar.grid(row=2, column=2, padx=10, pady=5)

        # Botón Agregar y Modificar (Abajo de los inputs)
        self.btn_agregar = tk.Button(frame_superior, text="Agregar", width=12,command=self.agregar)
        self.btn_agregar.grid(row=2, column=0, pady=10)

        # El botón modificar llama a la función local que enviará los datos
        self.btn_modificar = tk.Button(frame_superior, text="Modificar", width=12, command=self.click_modificar)
        self.btn_modificar.grid(row=2, column=1, pady=10)

        # --- SECCIÓN MEDIA: EXPORTAR / IMPORTAR ---
        frame_formatos = tk.Frame(self.root, padx=10)
        frame_formatos.pack(fill="x")

        formatos = ["csv", "json", "xml"]
        for i, fmt in enumerate(formatos):
            tk.Button(frame_formatos, text=f"Exportar {fmt}", width=15).grid(row=0, column=i, padx=2, pady=2)
            tk.Button(frame_formatos, text=f"Importar {fmt}", width=15).grid(row=1, column=i, padx=2, pady=2)

        # --- SECCIÓN INFERIOR: ACCIONES GLOBALES ---
        frame_global = tk.Frame(self.root, padx=10, pady=20)
        frame_global.pack(fill="x")

        self.btn_backup = tk.Button(frame_global, text="Ejecutar Backup", width=50)
        self.btn_backup.pack(pady=2)

        self.btn_eliminar_todos = tk.Button(frame_global, text="Eliminar todos los Grupos", width=50, command=self.eliminar_todos)
        self.btn_eliminar_todos.pack(pady=2)

        self.btn_restaurar_todos = tk.Button(frame_global, text="Restaurar todos los Grupos", width=50)
        self.btn_restaurar_todos.pack(pady=2)

    # --- MÉTODOS DE SOPORTE PARA LA INTERFAZ ---

    def click_modificar(self):
        if self.comando_modificar:
            clave = self.ent_clave.get()
            nombre = self.ent_nombre.get()
            self.comando_modificar(clave, nombre)

    def click_buscar(self):
        """Manda la clave al comando de búsqueda externo si existe"""
        if self.comando_buscar:
            clave = self.ent_clave.get()
            self.comando_buscar(clave, self) # Pasamos 'self' para que el buscador pueda escribir en los campos

    def limpiar_campos(self):
        """Limpia los cuadros de texto"""
        self.ent_clave.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)

    def eliminar(self):

        clave = self.ent_clave.get()

        if not clave:
            messagebox.showwarning("Aviso", "Ingrese la clave del grupo")
            return

        eliminar_grupo(clave)

        messagebox.showinfo(
            "Eliminar",
            "Grupo eliminado correctamente"
        )

    def eliminar_todos(self):

        confirmar = messagebox.askyesno(
            "Confirmación",
            "¿Estás seguro de eliminar TODOS los grupos?"
        )

        if confirmar:

            eliminar_todos_grupos()

            messagebox.showinfo(
                "Eliminar",
                "Todos los grupos fueron eliminados"
            )
    def agregar(self):

        clave = self.ent_clave.get()
        nombre = self.ent_nombre.get()

        if not clave or not nombre:
            messagebox.showwarning("Aviso", "Ingrese la clave y el nombre del grupo")
            return

        agregar_grupo(clave, nombre)

        messagebox.showinfo(
            "Agregar",
            "Grupo agregado correctamente"
        )


