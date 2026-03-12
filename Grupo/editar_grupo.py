from database.conexion import grupos

def modificar_grupo(clave_busqueda, nuevo_nombre):
    """
    Busca un grupo por su clave (Clave) y actualiza su nombre.
    """
    try:
        # 1. Verificar si el grupo existe
        grupo_existente = grupos.find_one({"Clave": clave_busqueda})

        if grupo_existente:
            # 2. Ejecutar la actualización
            resultado = grupos.update_one(
                {"Clave": clave_busqueda},
                {"$set": {"Nombre": nuevo_nombre}}
            )
            
            if resultado.modified_count > 0:
                return "Éxito", f"Grupo '{clave_busqueda}' actualizado correctamente."
            else:
                return "Info", "No se realizaron cambios (los datos son idénticos)."
        else:
            return "Error", f"No se encontró el grupo con clave: {clave_busqueda}"
            
    except Exception as e:
        return "Error", f"Ocurrió un error: {e}"