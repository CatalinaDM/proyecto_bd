# Backup/restaurar_backup.py
import json
from tkinter import filedialog, messagebox
from database.conexion import grupos
from bson import ObjectId

def restaurar_backup():
    """Restaura un archivo de backup a la colección grupos."""
    try:
        # 1. Preguntar al usuario qué archivo quiere restaurar
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de Backup para restaurar",
            filetypes=[("Archivo de Respaldo", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if not ruta_archivo:
            messagebox.showwarning("Cancelado", "Operación cancelada por el usuario")
            return

        # 2. Verificar si hay datos actuales en la BD
        grupos_actuales = grupos.count_documents({})
        
        if grupos_actuales > 0:
            respuesta = messagebox.askyesnocancel(
                "Datos existentes",
                f"Actualmente hay {grupos_actuales} grupos en la base de datos.\n\n"
                "¿Qué desea hacer?\n\n"
                "Sí: Reemplazar todos los datos actuales\n"
                "No: agregar solo los nuevos\n"
                "Cancelar: No hacer nada"
            )
            
            if respuesta is None:  # Cancelar
                messagebox.showwarning("Cancelado", "Operación cancelada")
                return
            elif respuesta:  # Sí - Reemplazar
                modo = "reemplazar"
            else:  # No - Merge
                modo = "merge"
        else:
            modo = "insertar"

        # 3. Leer el archivo de backup
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            datos_backup = json.load(f)

        if not datos_backup:
            messagebox.showwarning("Aviso", "El archivo de backup está vacío")
            return

        # 4. Restaurar según el modo elegido
        if modo == "reemplazar":
            grupos.delete_many({})
            
            for doc in datos_backup:
                if "_id" in doc:
                    doc["_id"] = ObjectId(doc["_id"])
                grupos.insert_one(doc)
            
            messagebox.showinfo("Éxito", f" Restauración completada: Se reemplazaron {len(datos_backup)} grupos")
            
        elif modo == "merge":
            insertados = 0
            actualizados = 0
            saltados = 0
            
            for doc in datos_backup:
                existe = grupos.find_one({"cveGru": doc["cveGru"]})
                
                if existe:
                    respuesta_dup = messagebox.askyesno(
                        "Registro duplicado",
                        f"El grupo '{doc['cveGru']} - {doc['nomGru']}' ya existe.\n"
                        "¿Desea actualizarlo con los datos del backup?"
                    )
                    if respuesta_dup:
                        grupos.update_one(
                            {"cveGru": doc["cveGru"]},
                            {"$set": {"nomGru": doc["nomGru"]}}
                        )
                        actualizados += 1
                    else:
                        saltados += 1
                else:
                    if "_id" in doc:
                        doc["_id"] = ObjectId(doc["_id"])
                    grupos.insert_one(doc)
                    insertados += 1
            
            mensaje = f"Resumen de restauración:\n"
            mensaje += f"   - Insertados: {insertados}\n"
            mensaje += f"   - Actualizados: {actualizados}\n"
            mensaje += f"   - Saltados: {saltados}"
            messagebox.showinfo("Resultado", mensaje)
            
        else:  # Insertar (BD vacía)
            for doc in datos_backup:
                if "_id" in doc:
                    doc["_id"] = ObjectId(doc["_id"])
                grupos.insert_one(doc)
            
            messagebox.showinfo("Éxito", f" Restauración completada: Se insertaron {len(datos_backup)} grupos")

    except json.JSONDecodeError:
        messagebox.showerror("Error", "El archivo no tiene un formato JSON válido")
    except Exception as e:
        messagebox.showerror("Error",f" Error durante la restauración: {str(e)}")