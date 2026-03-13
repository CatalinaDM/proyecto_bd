import json
from datetime import datetime
from tkinter import filedialog, messagebox
from database.conexion import grupos

def realizar_backup():
    """Genera un archivo de respaldo de la colección grupos."""
    try:
        # 1. Obtener todos los datos
        datos = list(grupos.find())
        
        if not datos:
            messagebox.showwarning("Backup", "La base de datos está vacía. No hay nada que respaldar.")
            return

        # 2. Preparar nombre de archivo por defecto (ej: backup_grupos_2024-05-20.json)
        fecha_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_sugerido = f"backup_grupos_{fecha_str}.json"

        # 3. Pedir al usuario dónde guardarlo
        ruta_archivo = filedialog.asksaveasfilename(
            title="Seleccionar destino del Backup",
            initialfile=nombre_sugerido,
            defaultextension=".json",
            filetypes=[("Archivo de Respaldo", "*.json")]
        )

        if ruta_archivo:
            # Convertir ObjectIds a string para que sea compatible con JSON
            for doc in datos:
                if "_id" in doc:
                    doc["_id"] = str(doc["_id"])

            # 4. Guardar los datos
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            
            messagebox.showinfo("Éxito", f"Backup creado correctamente en:\n{ruta_archivo}")
            
    except Exception as e:
        messagebox.showerror("Error de Backup", f"No se pudo completar el respaldo: {e}")