from database.conexion import db

def actualizar_alumno_bd(cve, nuevo_nombre):
    """
    Actualiza únicamente el nombre del alumno.
    La clave (cveAlu) se usa como identificador único y no se puede modificar.
    Permite nombres duplicados en la base de datos.
    """
    try:
        cve_clean = str(cve).strip()
        nombre_clean = str(nuevo_nombre).strip()

        resultado = db.Alumno.update_one(
            {"cveAlu": cve_clean},
            {"$set": {"nomAlu": nombre_clean}}
        )
        
        return resultado.matched_count > 0

    except Exception as e:
        print(f"Error al actualizar alumno: {e}")
        return False