from database.conexion import alumnos
from tkinter import messagebox

def eliminar_alumno(cveAlu, ventana=None):
    if not cveAlu: return False
    if alumnos.delete_one({"cveAlu": cveAlu}).deleted_count > 0:
        messagebox.showinfo("Éxito", "Alumno eliminado")
        if ventana: ventana.limpiar_campos()
        return True
    return False

def eliminar_todos_alumnos():
    if alumnos.count_documents({}) == 0: return False
    alumnos.delete_many({})
    messagebox.showinfo("Éxito", "Todos los alumnos eliminados")