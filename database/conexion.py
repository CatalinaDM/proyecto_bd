from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["BD_GrupoAlumno"]

#Collections dentro de BD_GrupoAlumno
alumnos = db["Alumno"]
grupos = db["Grupo"]