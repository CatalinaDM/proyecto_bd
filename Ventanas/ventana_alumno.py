import tkinter as tk
from tkinter import ttk, messagebox

from utils.exportar import exportar_csv, exportar_json, exportar_xml
from utils.importar_alumno import importar_csv_alumno, importar_json_alumno, importar_xml_alumno

from Backup.backup import realizar_backup
from Backup.restore import restaurar_backup

from Alumno.editar_alumno import actualizar_alumno_bd
from Alumno.eliminar_alumno import eliminar_alumno, eliminar_todos_alumnos
from Alumno.agregar_alumno import agregar_alumno
from Alumno.buscar_alumno import buscar_alumno_bd


class VentanaAlumno:

    def __init__(self, root):
        self.root = root
        self.root.title("Administración de Alumnos")
        self.root.geometry("420x500")
        self.root.configure(bg="#F8F1F1")

        # ====== ESTILOS ======
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Card.TFrame", background="#F8F1F1")
        style.configure("TLabel", background="#F8F1F1", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#F8F1F1", foreground="white",
                        font=("Segoe UI", 16, "bold"))

        style.configure("Primary.TButton", background="#16C79A", foreground="white")
        style.map("Primary.TButton", background=[("active", "#13a37f")])

        style.configure("Secondary.TButton", background="#11698E", foreground="white")
        style.map("Secondary.TButton", background=[("active", "#0e5675")])

        # ====== HEADER ======
        tk.Label(self.root, text="Gestión de Alumnos",
                 bg="#F8F1F1", fg="#19456B",
                 font=("Segoe UI", 18, "bold")).pack(pady=15)

        # ====== CONTENEDOR ======
        container = tk.Frame(self.root, bg="#F8F1F1")
        container.pack(fill="both", expand=True, padx=15)

        # ====== TARJETA DATOS ======
        card_datos = tk.Frame(container, bg="#F8F1F1", bd=0, relief="flat")
        card_datos.pack(fill="x", pady=10)

        tk.Label(card_datos, text="Clave:", bg="#F8F1F1").grid(row=0, column=0, padx=10, pady=10)
        self.ent_clave = tk.Entry(card_datos, width=30, relief="flat", bg="white")
        self.ent_clave.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(card_datos, text="Nombre:", bg="#F8F1F1").grid(row=1, column=0, padx=10, pady=10)
        self.ent_nombre = tk.Entry(card_datos, width=30, relief="flat", bg="white")
        self.ent_nombre.grid(row=1, column=1, padx=10, pady=10)

        # BOTONES LATERALES
        side_btns = tk.Frame(card_datos, bg="#F8F1F1")
        side_btns.grid(row=0, column=2, rowspan=2, padx=10)

        tk.Button(side_btns, text="Buscar", bg="#11698E", fg="white",
                  relief="flat", width=12, command=self.click_buscar).pack(pady=3)

        tk.Button(side_btns, text="Limpiar", bg="#11698E", fg="white",
                  relief="flat", width=12, command=self.limpiar_campos).pack(pady=3)

        tk.Button(side_btns, text="Eliminar", bg="#c0392b", fg="white",
                  relief="flat", width=12,
                  command=lambda: eliminar_alumno(self.ent_clave.get(), self)).pack(pady=3)

        # ====== ACCIONES ======
        acciones = tk.Frame(container, bg="#F8F1F1")
        acciones.pack(fill="x", pady=10)

        tk.Button(acciones, text="Agregar",
                  bg="#16C79A", fg="white", relief="flat",
                  width=20,
                  command=lambda: agregar_alumno(self.ent_clave.get(), self.ent_nombre.get(), self)
                  ).pack(side="left", padx=5)

        tk.Button(acciones, text="Modificar",
                  bg="#11698E", fg="white", relief="flat",
                  width=20,
                  command=self.click_modificar
                  ).pack(side="left", padx=5)

        # ====== IMPORTAR / EXPORTAR ======
        card_formatos = tk.Frame(container, bg="#F8F1F1")
        card_formatos.pack(fill="x", pady=10)

        formatos = ["csv", "json", "xml"]
        # Configuración específica para Alumnos
        conf_alu = {
            "col": "Alumno",
            "csv_f": "cveAlu,nomAlu",
            "file": "alumnos_export",
            "xml_r": "Alumnos",
            "xml_h": "Alumno",
            "xml_m": {"cveAlu": "Clave", "nomAlu": "Nombre"}
        }

        # Funciones de importar (estas parecen seguir siendo individuales por ahora)
        funciones_importar = {
            "csv": importar_csv_alumno, 
            "json": importar_json_alumno, 
            "xml": importar_xml_alumno
        }

        for i, fmt in enumerate(formatos):
        # --- BOTONES DE EXPORTAR ---
            if fmt == "csv":
                cmd_exp = lambda: exportar_csv(conf_alu["col"], conf_alu["csv_f"], conf_alu["file"])
            elif fmt == "json":
                cmd_exp = lambda: exportar_json(conf_alu["col"], conf_alu["file"])
            else:
                cmd_exp = lambda: exportar_xml(conf_alu["col"], conf_alu["xml_r"], conf_alu["xml_h"], conf_alu["xml_m"], "alumnos_export")

            tk.Button(card_formatos, text=f"Exportar {fmt.upper()}",
              bg="#11698E", fg="white", relief="flat",
              width=15, command=cmd_exp).grid(row=0, column=i, padx=5, pady=5)

            # --- BOTONES DE IMPORTAR ---
            tk.Button(card_formatos, text=f"Importar {fmt.upper()}",
              bg="#16C79A", fg="white", relief="flat",
              width=15, command=funciones_importar[fmt]).grid(row=1, column=i, padx=5, pady=5)

        # ====== GLOBALES ======
        card_global = tk.Frame(container, bg="#F8F1F1")
        card_global.pack(fill="x", pady=10)

        tk.Button(card_global, text="Eliminar todos los alumnos",
                  bg="#c0392b", fg="white", relief="flat",
                  width=50, command=self.eliminar_todos_alumnos).pack(pady=4)

    # ====== LÓGICA (IGUAL) ======

    def click_buscar(self):
        termino = self.ent_clave.get().strip()

        if not termino:
            messagebox.showwarning("Aviso", "Ingresa la clave del alumno")
            return

        res = buscar_alumno_bd(termino)

        if res:
            self.ent_clave.config(state="normal")
            self.ent_clave.delete(0, tk.END)
            self.ent_clave.insert(0, res.get("cveAlu", ""))
            self.ent_clave.config(state="readonly")

            self.ent_nombre.delete(0, tk.END)
            self.ent_nombre.insert(0, res.get("nomAlu", ""))
        else:
            messagebox.showwarning("Error", "No encontrado")

    def click_modificar(self):
        cve = self.ent_clave.get().strip()
        nom = self.ent_nombre.get().strip()

        if not cve or not nom:
            messagebox.showwarning("Aviso", "Datos incompletos")
            return

        if actualizar_alumno_bd(cve, nom):
            messagebox.showinfo("Éxito", "Actualizado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo actualizar")

    def limpiar_campos(self):
        self.ent_clave.config(state="normal")
        self.ent_clave.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)

    def eliminar_todos_alumnos(self):
        if messagebox.askyesno("Confirmación", "¿Eliminar todos los alumnos?"):
            eliminar_todos_alumnos()