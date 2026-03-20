import subprocess
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox
from database.conexion import grupos 

# --- CONFIGURACIÓN DE RUTAS ---
# Asegúrate de que esta ruta sea la correcta en tu equipo
RUTA_MONGOEXPORT = r"C:\Program Files\MongoDB\Tools\100\bin\mongoexport.exe"
NOMBRE_BD = "BD_GrupoAlumno" 
COLECCION = "Grupo"

def exportar_csv():
    """Exporta a CSV usando la herramienta nativa mongoexport."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv", 
        filetypes=[("Archivo CSV", "*.csv")],
        initialfile="grupos_export.csv"
    )
    if not file_path: return 

    try:
        # Comando: --db, --collection, --type=csv, --fields (columnas), --out
        comando = [
            RUTA_MONGOEXPORT,
            f"--db={NOMBRE_BD}",
            f"--collection={COLECCION}",
            "--type=csv",
            "--fields=cveGru,nomGru",
            f"--out={file_path}"
        ]
        
        # Ejecución (CREATE_NO_WINDOW = 0x08000000 para que no parpadee el CMD)
        subprocess.run(comando, check=True, creationflags=0x08000000)
        messagebox.showinfo("Éxito", f"Exportación CSV exitosa usando mongoexport.\nRuta: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar a CSV: {e}")

def exportar_json():
    """Exporta a JSON usando la herramienta nativa mongoexport."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json", 
        filetypes=[("Archivo JSON", "*.json")],
        initialfile="grupos_export.json"
    )
    if not file_path: return

    try:
        # Usamos --jsonArray para que el resultado sea una lista [{},{}] válida
        comando = [
            RUTA_MONGOEXPORT,
            f"--db={NOMBRE_BD}",
            f"--collection={COLECCION}",
            "--jsonArray",
            f"--out={file_path}"
        ]
        
        subprocess.run(comando, check=True, creationflags=0x08000000)
        messagebox.showinfo("Éxito", f"Exportación JSON exitosa usando mongoexport.\nRuta: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar a JSON: {e}")

def exportar_xml():
    """Exporta a XML usando Python (mongoexport no soporta este formato)."""
    try:
        datos = list(grupos.find())
        if not datos:
            messagebox.showwarning("Aviso", "La base de datos está vacía.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xml", 
            filetypes=[("Archivo XML", "*.xml")]
        )
        if not file_path: return

        root = ET.Element("Grupos")
        for doc in datos:
            grupo_element = ET.SubElement(root, "Grupo")
            ET.SubElement(grupo_element, "Clave").text = str(doc.get('cveGru', ''))
            ET.SubElement(grupo_element, "Nombre").text = doc.get('nomGru', '')

        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0) 
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        messagebox.showinfo("Éxito", "Exportación XML completada exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar el archivo XML: {e}")