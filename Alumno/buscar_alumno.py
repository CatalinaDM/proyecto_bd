from database.conexion import alumnos

def buscar_en_bd(termino):
    """
    Busca un alumno por su clave (cveAlu) exacta.
    Retorna el documento del alumno o None si no se encuentra.
    """
    try:
        # Limpiamos espacios en blanco y aseguramos que sea string
        filtro = {"cveAlu": str(termino).strip()}
        
        # Realizamos la búsqueda en la colección de alumnos
        alumno = alumnos.find_one(filtro)
        
        return alumno
        
    except Exception as e:
        print(f"Error al buscar alumno: {e}")
        return None