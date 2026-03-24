from database.conexion import grupos
from tkinter import messagebox

def agregar_grupo(cveGru, nomGru, ventana=None):

    # Validar campos vacíos
    if not cveGru or not nomGru:
        messagebox.showwarning("Advertencia", "Debe ingresar clave y nombre")
        return False

    # Validar si ya existe la clave
    existe_clave = grupos.find_one({"cveGru": cveGru})
    if existe_clave:
        messagebox.showwarning("Advertencia", "Ya existe un grupo con esa clave")
        return False

    # Insertar si todo está correcto
    grupos.insert_one({
        "cveGru": cveGru,
        "nomGru": nomGru
    })

    messagebox.showinfo("Éxito", "Grupo agregado correctamente")
    if ventana:
        ventana.limpiar_campos()
    return True