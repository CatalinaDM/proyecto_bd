import tkinter as tk
from tkinter import ttk

class VentanaGrupo:
    def __init__(self, root):
        self.root = root
        self.root.title("Admon Grupo")
        self.root.geometry("450x400")
        
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
        self.btn_buscar = tk.Button(frame_superior, text="Buscar", width=12)
        self.btn_buscar.grid(row=0, column=2, padx=10)

        self.btn_limpiar = tk.Button(frame_superior, text="Limpiar", width=12)
        self.btn_limpiar.grid(row=1, column=2, padx=10)

        self.btn_eliminar = tk.Button(frame_superior, text="Eliminar", width=12)
        self.btn_eliminar.grid(row=2, column=2, padx=10, pady=5)

        # Botón Agregar y Modificar (Abajo de los inputs)
        self.btn_agregar = tk.Button(frame_superior, text="Agregar", width=12)
        self.btn_agregar.grid(row=2, column=0, pady=10)

        self.btn_modificar = tk.Button(frame_superior, text="Modificar", width=12)
        self.btn_modificar.grid(row=2, column=1, pady=10)

        # --- SECCIÓN MEDIA: EXPORTAR / IMPORTAR ---
        frame_formatos = tk.Frame(self.root, padx=10)
        frame_formatos.pack(fill="x")

        # Columnas de Exportar/Importar (CSV, JSON, XML)
        formatos = ["csv", "json", "xml"]
        for i, fmt in enumerate(formatos):
            tk.Button(frame_formatos, text=f"Exportar {fmt}", width=15).grid(row=0, column=i, padx=2, pady=2)
            tk.Button(frame_formatos, text=f"Importar {fmt}", width=15).grid(row=1, column=i, padx=2, pady=2)

        # --- SECCIÓN INFERIOR: ACCIONES GLOBALES ---
        frame_global = tk.Frame(self.root, padx=10, pady=20)
        frame_global.pack(fill="x")

        self.btn_backup = tk.Button(frame_global, text="Ejecutar Backup", width=50)
        self.btn_backup.pack(pady=2)

        self.btn_eliminar_todos = tk.Button(frame_global, text="Eliminar todos los Grupos", width=50)
        self.btn_eliminar_todos.pack(pady=2)

        self.btn_restaurar_todos = tk.Button(frame_global, text="Restaurar todos los Grupos", width=50)
        self.btn_restaurar_todos.pack(pady=2)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = VentanaGrupo(ventana)
    ventana.mainloop()