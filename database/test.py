from database.conexion import client, db

try:
    # El comando 'ping' es la forma oficial de saber si hay respuesta
    client.admin.command('ping')
    print("✅ ¡Conexión exitosa! MongoDB está respondiendo.")
    print(f"Bases de datos disponibles: {client.list_database_names()}")
    print(f"Colecciones en BD_GrupoAlumno: {db.list_collection_names()}")
except Exception as e:
    print(f"❌ Error de conexión: {e}")