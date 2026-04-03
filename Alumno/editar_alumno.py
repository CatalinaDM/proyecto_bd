from database.conexion import db

def actualizar_alumno_bd(cve, nuevo_nombre, nueva_edad, nueva_cve_gru):
    """
    Actualiza todos los atributos del alumno excepto su clave única.
    La clave (cveAlu) se usa como filtro para encontrar el registro.
    """
    try:
        # 1. Limpieza y normalización de datos
        cve_clean = str(cve).strip()
        nombre_clean = str(nuevo_nombre).strip()
        edad_clean = str(nueva_edad).strip()
        grupo_clean = str(nueva_cve_gru).strip()

        # 2. Ejecutar la actualización masiva de campos
        # Usamos $set para actualizar múltiples campos a la vez
        resultado = db.Alumno.update_one(
            {"cveAlu": cve_clean}, # Buscamos al alumno por su clave
            {
                "$set": {
                    "nomAlu": nombre_clean,
                    "edaAlu": edad_clean,
                    "cveGru": grupo_clean
                }
            }
        )
        
        # Retorna True si encontró el registro (aunque no haya habido cambios en el texto)
        return resultado.matched_count > 0

    except Exception as e:
        print(f"Error al actualizar alumno en BD: {e}")
        return False