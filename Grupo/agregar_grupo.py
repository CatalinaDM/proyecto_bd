from database.conexion import grupos

# INSERTAR
def agregar_grupo(cveGru, nomGru):
    grupos.insert_one({
        "cveGru": cveGru,
        "nomGru": nomGru
    })