from database.conexion import grupos

def buscar_en_bd(termino):
    """Busca únicamente por cveGru exacta y retorna el documento o None"""
    try:
        filtro = {"cveGru": str(termino).strip()}
        
        return grupos.find_one(filtro)
    except Exception as e:
        print(f"Error al buscar: {e}")
        return None