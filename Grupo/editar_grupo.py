from database.conexion import grupos

def actualizar_en_bd(cve, nuevo_nombre):
    """
    Actualiza el documento donde cveGru coincida, siempre y cuando 
    el nuevo nombre no exista ya en la base de datos.
    """
    try:
        cve_clean = str(cve).strip()
        nombre_clean = str(nuevo_nombre).strip()

        existe = grupos.find_one({
            "$or": [
                {"nomGru": nombre_clean}
            ]
        })

        if existe:
            print(f"Error: El nombre '{nombre_clean}' ya está registrado.")
            return False

        resultado = grupos.update_one(
            {"cveGru": cve_clean},
            {"$set": {"nomGru": nombre_clean}}
        )
        
        return resultado.modified_count > 0

    except Exception as e:
        print(f"Error al actualizar: {e}")
        return False