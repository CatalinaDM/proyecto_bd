import csv
import json
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox
from database.conexion import grupos 

def obtener_datos():
    """Consulta todos los grupos de la base de datos."""
    try:
        return list(grupos.find()) # Retorna una lista de diccionarios
    except Exception as e:
        messagebox.showerror("Error", f"Error al consultar la BD: {e}")
        return []

def exportar_csv():
    """Exporta los datos de grupos a un archivo CSV."""
    datos = obtener_datos()
    if not datos: return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivo CSV", "*.csv")])
    if not file_path: return # El usuario canceló

    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            # Reemplaza 'cveGru' y 'nomGru' con los nombres de tus campos reales
            fieldnames = ['cveGru', 'nomGru'] 
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for doc in datos:
                # Crea un nuevo diccionario solo con los campos que quieres exportar
                fila = {field: doc.get(field, '') for field in fieldnames}
                writer.writerow(fila)
        messagebox.showinfo("Éxito", "Datos exportados a CSV correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar a CSV: {e}")

def exportar_json():
    """Exporta los datos de grupos a un archivo JSON."""
    datos = obtener_datos()
    if not datos: return

    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivo JSON", "*.json")])
    if not file_path: return # El usuario canceló

    try:
        # Pymongo devuelve objetos ObjectId que no son serializables por defecto en JSON.
        # Una forma sencilla es convertirlos a string.
        for doc in datos:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(datos, file, indent=4, ensure_ascii=False) # indent para que sea legible
        messagebox.showinfo("Éxito", "Datos exportados a JSON correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar a JSON: {e}")

def exportar_xml():
    """Exporta los datos de grupos a un archivo XML."""
    datos = obtener_datos()
    if not datos: return

    file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("Archivo XML", "*.xml")])
    if not file_path: return # El usuario canceló

    try:
        # Crea el elemento raíz
        root = ET.Element("Grupos")

        for doc in datos:
            # Crea un elemento para cada grupo
            grupo_element = ET.SubElement(root, "Grupo")
            
            # Añade subelementos para cada campo
            ET.SubElement(grupo_element, "Clave").text = str(doc.get('cveGru', ''))
            ET.SubElement(grupo_element, "Nombre").text = doc.get('nomGru', '')

        # Crea el árbol XML y guárdalo
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0) # Para que el XML sea legible (Python 3.9+)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        messagebox.showinfo("Éxito", "Datos exportados a XML correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar a XML: {e}")