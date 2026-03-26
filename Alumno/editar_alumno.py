from database.conexion import alumnos, grupos

def actualizar_en_bd(cveAlu, nuevo_nombre, nueva_cveGru):
    try:
        # Validar que el nuevo grupo exista si se cambió
        if not grupos.find_one({"cveGru": nueva_cveGru}):
            print("Error: El grupo destino no existe")
            return False

        resultado = alumnos.update_one(
            {"cveAlu": cveAlu},
            {"$set": {"nomAlu": nuevo_nombre, "cveGru": nueva_cveGru}}
        )
        return resultado.modified_count > 0
    except Exception as e:
        return False