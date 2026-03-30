import subprocess
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox

import json
from database.conexion import db 

import os
import shutil

def encontrar_mongoexport():
    """Busca mongoexport en el PATH o en rutas comunes de Windows."""
    # 1. Intentar buscarlo en las Variables de Entorno (PATH)
    ruta_en_path = shutil.which("mongoexport")
    if ruta_en_path:
        return ruta_en_path

    # 2. Rutas manuales comunes (Server y Tools)
    posibles_rutas = [
        r"C:\Program Files\MongoDB\Tools\100\bin\mongoexport.exe",
        r"C:\Program Files\MongoDB\Tools\110\bin\mongoexport.exe",
        r"C:\Program Files\MongoDB\Tools\120\bin\mongoexport.exe",
        r"C:\Program Files\MongoDB\Server\7.0\bin\mongoexport.exe",
        r"C:\Program Files\MongoDB\Server\6.0\bin\mongoexport.exe",
        r"C:\Program Files\MongoDB\Server\5.0\bin\mongoexport.exe",
        r"C:\Program Files\MongoDB\Server\4.4\bin\mongoexport.exe"
    ]
    
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            return ruta
            
    return None

RUTA_MONGOEXPORT = encontrar_mongoexport()
NOMBRE_BD = "BD_GrupoAlumno" 

def exportar_csv(coleccion, campos, nombre_sugerido):
    """Exporta a CSV cualquier colección."""
    if RUTA_MONGOEXPORT is None:
        messagebox.showerror("Error de Sistema", 
            "Asegúrate de tener instaladas las MongoDB Database Tools.")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv", 
        filetypes=[("Archivo CSV", "*.csv")],
        initialfile=f"{nombre_sugerido}.csv"
    )
    if not file_path: return 

    try:
        comando = [
            RUTA_MONGOEXPORT,
            f"--db={NOMBRE_BD}",
            f"--collection={coleccion}",
            "--type=csv",
            f"--fields={campos}", # Ejemplo: "cveAlu,nomAlu"
            f"--out={file_path}"
        ]
        subprocess.run(comando, check=True, creationflags=0x08000000)
        messagebox.showinfo("Éxito", "Exportación CSV exitosa.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar: {e}")

def exportar_json(coleccion, nombre_sugerido):
    """Exporta a JSON cualquier colección."""
    if RUTA_MONGOEXPORT is None:
        messagebox.showerror("Error de Sistema", 
            "Asegúrate de tener instaladas las MongoDB Database Tools.")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json", 
        filetypes=[("Archivo JSON", "*.json")],
        initialfile=f"{nombre_sugerido}.json"
    )
    if not file_path: return

    try:
        comando = [
            RUTA_MONGOEXPORT,
            f"--db={NOMBRE_BD}",
            f"--collection={coleccion}",
            "--jsonArray",
            f"--out={file_path}"
        ]
        subprocess.run(comando, check=True, creationflags=0x08000000)
        messagebox.showinfo("Éxito", "Exportación JSON exitosa.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar: {e}")

def exportar_xml(coleccion, tag_raiz, tag_hijo, mapeo_campos, nombre_sugerido="exportacion"):
    """
    Exporta a XML usando mongoexport como motor de extracción de datos.
    """
    # 1. VERIFICACIÓN DE LA HERRAMIENTA (Ahora sí es obligatoria)
    if RUTA_MONGOEXPORT is None:
        messagebox.showerror("Error de Sistema", "Se requiere mongoexport para esta operación.")
        return

    try:
        # 2. USAMOS MONGOEXPORT PARA TRAER LOS DATOS EN FORMATO JSON
        # No creamos un archivo, capturamos la salida en una variable (stdout)
        comando = [
            RUTA_MONGOEXPORT,
            f"--db={NOMBRE_BD}",
            f"--collection={coleccion}",
            "--jsonArray",
            "--quiet" # Para que no ensucie la salida con logs
        ]
        
        resultado = subprocess.run(comando, capture_output=True, text=True, encoding='utf-8', creationflags=0x08000000)
        
        if resultado.returncode != 0:
            raise Exception(f"Error en mongoexport: {resultado.stderr}")

        datos = json.loads(resultado.stdout) # Convertimos el texto de mongo a lista de Python
        
        if not datos:
            messagebox.showwarning("Aviso", "No hay datos para exportar.")
            return

        # 3. SELECCIÓN DE RUTA PARA GUARDAR
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xml", 
            filetypes=[("Archivo XML", "*.xml")],
            initialfile=f"{nombre_sugerido}.xml"
        )
        if not file_path: return

        # 4. CONSTRUCCIÓN DEL XML (Igual que antes, pero con datos de mongoexport)
        root = ET.Element(tag_raiz)
        for doc in datos:
            elemento = ET.SubElement(root, tag_hijo)
            for campo_bd, etiqueta in mapeo_campos.items():
                ET.SubElement(elemento, etiqueta).text = str(doc.get(campo_bd, ''))

        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0) 
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        
        messagebox.showinfo("Éxito", "Exportación XML exitosa.")

    except Exception as e:
        messagebox.showerror("Error", f"Fallo al usar mongoexport para XML: {e}")