from database.conexion import grupos

def buscar_en_bd(termino):
    """Busca por cveGru o nomGru y retorna el documento o None"""
    try:
        # Buscamos por clave exacta o nombre (usando regex para que sea flexible)
        filtro = {
            "$or": [
                {"cveGru": str(termino).strip()},
                {"nomGru": {"$regex": str(termino).strip(), "$options": "i"}}
            ]
        }
        return grupos.find_one(filtro)
    except Exception as e:
        print(f"Error al buscar: {e}")
        return None