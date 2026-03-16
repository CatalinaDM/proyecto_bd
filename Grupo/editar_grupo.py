from database.conexion import grupos

def actualizar_en_bd(cve, nuevo_nombre):
    """
    Actualiza únicamente el nombre del grupo.
    La clave (cveGru) se usa como identificador y no se modifica.
    """
    try:
        cve_clean = str(cve).strip()
        nombre_clean = str(nuevo_nombre).strip()

        # 1. Verificar si el nombre ya existe en OTRO grupo diferente al actual
        # Esto evita errores si le das a "Modificar" sin haber cambiado el nombre
        duplicado = grupos.find_one({
            "nomGru": nombre_clean,
            "cveGru": {"$ne": cve_clean}  # Que el nombre exista pero NO sea del grupo actual
        })

        if duplicado:
            print(f"Error: El nombre '{nombre_clean}' ya está registrado en otro grupo.")
            return False

        # 2. Ejecutar la actualización solo del campo nomGru
        resultado = grupos.update_one(
            {"cveGru": cve_clean},        # Filtro por clave
            {"$set": {"nomGru": nombre_clean}} # Solo modificamos el nombre
        )
        
        return resultado.modified_count > 0

    except Exception as e:
        print(f"Error al actualizar: {e}")
        return False