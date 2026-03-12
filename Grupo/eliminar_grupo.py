from database.conexion import grupos

# ELIMINAR UNO
def eliminar_grupo(cveGru):
    grupos.delete_one({"cveGru": cveGru})


# ELIMINAR TODOS
def eliminar_todos_grupos():
    grupos.delete_many({})