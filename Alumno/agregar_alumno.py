from database.conexion import alumnos
from tkinter import messagebox

def agregar_alumno(cveAlu, nomAlu, ventana=None):

    # Validar campos vacíos
    if not cveAlu or not nomAlu:
        messagebox.showwarning("Advertencia", "Debe ingresar clave y nombre")
        return False

    # Validar si ya existe la clave
    existe_clave = alumnos.find_one({"cveAlu": cveAlu})
    if existe_clave:
        messagebox.showwarning("Advertencia", "Ya existe un alumno con esa clave")
        return False

    # Insertar si todo está correcto
    alumnos.insert_one({
        "cveAlu": cveAlu,
        "nomAlu": nomAlu
    })

    messagebox.showinfo("Éxito", "Alumno agregado correctamente")
    if ventana:
        ventana.limpiar_campos()
    return True