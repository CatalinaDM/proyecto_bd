import tkinter as tk
from tkinter import messagebox
from database.conexion import grupos
from Ventanas.ventana_grupo import VentanaGrupo 

def ejecutar_actualizacion(cve, nuevo_nom):
    """Lógica conectada a los campos reales de tu MongoDB"""
    if not cve or not nuevo_nom:
        messagebox.showwarning("Atención", "Campos incompletos.")
        return

    try:
        resultado = grupos.update_one(
            {"_id": cve}, 
            {"$set": {"nomGru": nuevo_nom}}
        )
        
        if resultado.modified_count > 0:
            messagebox.showinfo("Éxito", f"Grupo {cve} actualizado correctamente.")
        elif resultado.matched_count > 0:
            messagebox.showwarning("Aviso", "No se realizaron cambios (el nombre es igual).")
        else:
            messagebox.showwarning("Error", f"No se encontró el ID: {cve}")
    except Exception as e:
        messagebox.showerror("Error de BD", f"Ocurrió un error: {e}")

def abrir_ventana_edicion():
    root = tk.Tk()
    app = VentanaGrupo(root, comando_modificar=ejecutar_actualizacion)
    root.mainloop()

if __name__ == "__main__":
    print("Iniciando Interfaz de Usuario...")
    abrir_ventana_edicion()