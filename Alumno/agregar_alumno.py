from database.conexion import alumnos
from tkinter import messagebox

def agregar_alumno(cveAlu, nomAlu, edaAlu, cveGru, ventana=None):
    """
    Registra un nuevo alumno con sus datos completos y relación de grupo.
    """
    # 1. Validar campos vacíos (Todos son obligatorios ahora)
    if not all([cveAlu, nomAlu, edaAlu, cveGru]):
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return False

    try:
        # 2. Normalización de datos (Todo a String y sin espacios extra)
        cve_clean = str(cveAlu).strip()
        nom_clean = str(nomAlu).strip()
        eda_clean = str(edaAlu).strip()
        gru_clean = str(cveGru).strip()

        # 3. Validar si ya existe la clave (ID único)
        existe_clave = alumnos.find_one({"cveAlu": cve_clean})
        if existe_clave:
            messagebox.showwarning("Advertencia", f"La clave '{cve_clean}' ya pertenece a otro alumno")
            return False

        # 4. Insertar el documento completo
        alumnos.insert_one({
            "cveAlu": cve_clean,
            "nomAlu": nom_clean,
            "edaAlu": eda_clean,
            "cveGru": gru_clean  # Relación con la colección Grupo
        })

        messagebox.showinfo("Éxito", "Alumno registrado correctamente")
        
        if ventana:
            ventana.limpiar_campos()
        return True

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar en la base de datos: {e}")
        return False