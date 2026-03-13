from database.conexion import grupos

def agregar_grupo(cveGru, nomGru):

    # Validar campos vacíos
    if not cveGru or not nomGru:
        return False, "Debe ingresar clave y nombre"

    # Validar si ya existe la clave
    existe_clave = grupos.find_one({"cveGru": cveGru})
    if existe_clave:
        return False, "Ya existe un grupo con esa clave"

    # Validar si ya existe el nombre
    existe_nombre = grupos.find_one({"nomGru": nomGru})
    if existe_nombre:
        return False, "Ya existe un grupo con ese nombre"

    # Insertar si todo está correcto
    grupos.insert_one({
        "cveGru": cveGru,
        "nomGru": nomGru
    })

    return True, "Grupo agregado correctamente"