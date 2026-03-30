import tkinter as tk
from tkinter import ttk
from Ventanas.ventana_grupo import VentanaGrupo
from Ventanas.ventana_alumno import VentanaAlumno
# (ajusta la ruta si es diferente)

class VentanaPrincipal:

    def __init__(self, root):
        self.root = root
        self.root.title("Ventana Principal")
        self.root.geometry("420x500")
        self.root.configure(bg="#F8F1F1")

        tk.Label(self.root, text="Ventana Principal",
                 bg="#F8F1F1", fg="#19456B",
                 font=("Segoe UI", 18, "bold")).pack(pady=15)

        # 🔹 BOTÓN IR A GRUPOS
        tk.Button(self.root, text="Ir a Grupos",
                  bg="#11698E", fg="white",
                  width=30,
                  command=self.abrir_grupos).pack(pady=10)

        # 🔹 BOTÓN IR A ALUMNOS (luego creas esa clase)
        tk.Button(self.root, text="Ir a Alumnos",
                  bg="#16C79A", fg="white",
                  width=30,
                  command=self.abrir_alumnos).pack(pady=10)

        # 🔹 BACKUP
        tk.Button(self.root, text="Ejecutar Backup de BD",
                  bg="#11698E", fg="white",
                  width=30,
                  command=self.ejecutar_backup).pack(pady=10)

        # 🔹 RESTORE
        tk.Button(self.root, text="Restaurar BD",
                  bg="#16C79A", fg="white",
                  width=30,
                  command=self.restaurar_bd).pack(pady=10)
        
    def abrir_grupos(self):
        nueva = tk.Toplevel(self.root)
        VentanaGrupo(nueva)

    def abrir_alumnos(self):
        nueva = tk.Toplevel(self.root)
        VentanaAlumno(nueva) 

    def ejecutar_backup(self):
        from Backup.backup import realizar_backup
        realizar_backup()

    def restaurar_bd(self):
        from Backup.restore import restaurar_bd_completa
        restaurar_bd_completa()