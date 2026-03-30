from database.conexion import db 

def buscar_alumno_bd(termino):
    """Busca únicamente por cveAlu exacta en la colección Alumno"""
    try:
        filtro = {"cveAlu": str(termino).strip()}
        return db.Alumno.find_one(filtro)
    except Exception as e:
        print(f"Error al buscar alumno: {e}")
        return None