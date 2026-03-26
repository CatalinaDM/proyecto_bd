from database.conexion import alumnos, grupos
from tkinter import messagebox

def agregar_alumno(cveAlu, nomAlu, cveGru, ventana=None):
    if not cveAlu or not nomAlu or not cveGru:
        messagebox.showwarning("Aviso", "Todos los campos son obligatorios")
        return False

    # Validar que el grupo exista
    if not grupos.find_one({"cveGru": cveGru}):
        messagebox.showerror("Error", f"El grupo '{cveGru}' no existe.")
        return False

    if alumnos.find_one({"cveAlu": cveAlu}):
        messagebox.showwarning("Aviso", "La clave del alumno ya existe")
        return False

    alumnos.insert_one({"cveAlu": cveAlu, "nomAlu": nomAlu, "cveGru": cveGru})
    messagebox.showinfo("Éxito", "Alumno registrado")
    if ventana: ventana.limpiar_campos()
    return True