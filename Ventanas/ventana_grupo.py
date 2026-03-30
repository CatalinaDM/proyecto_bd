import tkinter as tk
from tkinter import ttk, messagebox

from utils.exportar import exportar_csv, exportar_json, exportar_xml
from utils.importar import importar_csv, importar_json, importar_xml

from Backup.backup import realizar_backup
from Backup.restore import restaurar_backup

from Grupo.editar_grupo import actualizar_en_bd 
from Grupo.eliminar_grupo import eliminar_grupo, eliminar_todos_grupos
from Grupo.agregar_grupo import agregar_grupo
from Grupo.buscar_grupo import buscar_en_bd


class VentanaGrupo:

    def __init__(self, root):
        self.root = root
        self.root.title("Administración de Grupos")
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
        tk.Label(self.root, text="Gestión de Grupos",
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
                  command=lambda: eliminar_grupo(self.ent_clave.get(), self)).pack(pady=3)

        # ====== ACCIONES ======
        acciones = tk.Frame(container, bg="#F8F1F1")
        acciones.pack(fill="x", pady=10)

        tk.Button(acciones, text="Agregar",
                  bg="#16C79A", fg="white", relief="flat",
                  width=20,
                  command=lambda: agregar_grupo(self.ent_clave.get(), self.ent_nombre.get(), self)
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

        conf_gru = {
            "col": "Grupo",
            "csv_f": "cveGru,nomGru",
            "file": "grupos_export",
            "xml_r": "Grupos",
            "xml_h": "Grupo",
            "xml_m": {"cveGru": "Clave", "nomGru": "Nombre"}
        }

        funciones_importar = {
            "csv": importar_csv, 
            "json": importar_json, 
            "xml": importar_xml
        }

        for i, fmt in enumerate(formatos):
            if fmt == "csv":
                cmd_exp = lambda: exportar_csv(conf_gru["col"], conf_gru["csv_f"], conf_gru["file"])
            elif fmt == "json":
                cmd_exp = lambda: exportar_json(conf_gru["col"], conf_gru["file"])
            else: 
                cmd_exp = lambda: exportar_xml(conf_gru["col"], conf_gru["xml_r"], conf_gru["xml_h"], conf_gru["xml_m"], conf_gru["file"])

            tk.Button(card_formatos, text=f"Exportar {fmt.upper()}",
                      bg="#11698E", fg="white", relief="flat",
                      width=15, command=cmd_exp).grid(row=0, column=i, padx=5, pady=5)

            tk.Button(card_formatos, text=f"Importar {fmt.upper()}",
                      bg="#16C79A", fg="white", relief="flat",
                      width=15, command=funciones_importar[fmt]).grid(row=1, column=i, padx=5, pady=5)

        # ====== GLOBALES ======
        card_global = tk.Frame(container, bg="#F8F1F1")
        card_global.pack(fill="x", pady=10)

        tk.Button(card_global, text="Eliminar todos los grupos",
                  bg="#c0392b", fg="white", relief="flat",
                  width=50, command=self.eliminar_todos).pack(pady=4)

    # ====== LÓGICA (IGUAL) ======

    def click_buscar(self):
        termino = self.ent_clave.get().strip()

        if not termino:
            messagebox.showwarning("Aviso", "Ingresa la clave del grupo")
            return

        res = buscar_en_bd(termino)

        if res:
            self.ent_clave.config(state="normal")
            self.ent_clave.delete(0, tk.END)
            self.ent_clave.insert(0, res.get("cveGru", ""))
            self.ent_clave.config(state="readonly")

            self.ent_nombre.delete(0, tk.END)
            self.ent_nombre.insert(0, res.get("nomGru", ""))
        else:
            messagebox.showwarning("Error", "No encontrado")

    def click_modificar(self):
        cve = self.ent_clave.get().strip()
        nom = self.ent_nombre.get().strip()

        if not cve or not nom:
            messagebox.showwarning("Aviso", "Datos incompletos")
            return

        if actualizar_en_bd(cve, nom):
            messagebox.showinfo("Éxito", "Actualizado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo actualizar")

    def limpiar_campos(self):
        self.ent_clave.config(state="normal")
        self.ent_clave.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)

    def eliminar_todos(self):
        if messagebox.askyesno("Confirmación", "¿Eliminar todos los grupos?"):
            eliminar_todos_grupos()