from database.conexion import grupos,alumnos
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
        
        # Verificar si hay alumnos en este grupo
        alumnos_en_grupo = alumnos.count_documents({"cveGru": cveGru})
        
        if alumnos_en_grupo > 0:
            # Preguntar al usuario si desea eliminar también los alumnos
            respuesta = messagebox.askyesno(
                "Confirmación",
                f"El grupo '{cveGru}' tiene {alumnos_en_grupo} alumno(s) asignado(s).\n\n"
                "¿Deseas eliminar también a todos los alumnos de este grupo?\n"
                "Esto eliminará permanentemente los datos de los alumnos."
            )
            
            if not respuesta:
                messagebox.showinfo("Cancelado", "Eliminación cancelada por el usuario")
                return False
            
            # Eliminar todos los alumnos del grupo
            resultado_alumnos = alumnos.delete_many({"cveGru": cveGru})
            print(f"Se eliminaron {resultado_alumnos.deleted_count} alumnos del grupo {cveGru}")

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
       # Obtener todas las claves de los grupos que vamos a eliminar
        claves_grupos = [grupo["cveGru"] for grupo in grupos.find({}, {"cveGru": 1})]
        
        # Contar cuántos alumnos tienen esas claves de grupo
        alumnos_en_grupos = alumnos.count_documents({"cveGru": {"$in": claves_grupos}})
        
        # Preguntar confirmación
        mensaje = f"Se eliminarán {total_grupos} grupo(s)"
        if alumnos_en_grupos > 0:
            mensaje += f" y {alumnos_en_grupos} alumno(s) asociado(s)"
        mensaje += ".\n\n¿Estás seguro de continuar?"
        
        confirmar = messagebox.askyesno(
            "Confirmación",
            mensaje
        )
        
        if not confirmar:
            return False
        
        # Eliminar SOLO los alumnos que pertenecen a los grupos que estamos eliminando
        resultado_alumnos = alumnos.delete_many({"cveGru": {"$in": claves_grupos}})
        
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