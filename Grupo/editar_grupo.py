from database.conexion import grupos

def actualizar_en_bd(cve, nuevo_nombre):
    """Actualiza el documento donde cveGru coincida"""
    try:
        resultado = grupos.update_one(
            {"cveGru": str(cve).strip()},
            {"$set": {"nomGru": nuevo_nombre}}
        )
        return resultado.modified_count > 0
    except Exception as e:
        print(f"Error al actualizar: {e}")
        return False