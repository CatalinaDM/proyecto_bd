from database.conexion import grupos
from tkinter import messagebox

# ELIMINAR UNO
def eliminar_grupo(cveGru,ventana=None):
    try:
        if not cveGru:
            messagebox.showwarning("Aviso", "Ingrese la clave del grupo")
            return False
        
        # Verificar si existe antes de eliminar
        existe = grupos.find_one({"cveGru": cveGru})
        if not existe:
            messagebox.showwarning("Aviso", f"No existe un grupo con la clave '{cveGru}'")
            return False
        
        # Eliminar el grupo
        resultado = grupos.delete_one({"cveGru": cveGru})
        
        if resultado.deleted_count > 0:
            messagebox.showinfo("Éxito", f"Grupo '{cveGru}' eliminado correctamente")
            ventana.limpiar_campos()
            return True
        else:
            messagebox.showwarning("Aviso", "No se pudo eliminar el grupo")
            return False
            
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar grupo: {str(e)}")
        return False


# ELIMINAR TODOS
def eliminar_todos_grupos():
    
  try:
        # Validar si hay grupos para eliminar
        total_grupos = grupos.count_documents({})
        
        if total_grupos == 0:
             messagebox.showwarning("Aviso", "No hay grupos para eliminar"),
             return False
        
        # Eliminar todos los grupos
        resultado = grupos.delete_many({})
        
        # Verificar que se eliminaron correctamente
        if resultado.deleted_count > 0:
            messagebox.showinfo("Éxito", f"Se eliminaron {resultado.deleted_count} grupos correctamente")
            return True

        else:
            messagebox.showwarning("Aviso", "No se pudo eliminar ningún grupo"),
            return False
            
  except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar grupos: {str(e)}")
        return False