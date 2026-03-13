import csv
import json
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox, ttk 
from database.conexion import grupos 
from bson import ObjectId  # Para manejar IDs si es necesario

# ============================================
# FUNCIONES DE IMPORTACIÓN CON VENTANA (CSV, JSON, XML)
# ============================================

def importar_csv():
    """Importa CSV con ventana de duplicados"""
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivo CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )
    if not file_path:
        return
    
    try:
        registros_archivo = []
        registros_duplicados = []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            if 'cveGru' not in reader.fieldnames or 'nomGru' not in reader.fieldnames:
                messagebox.showerror(
                    "Error", 
                    "El archivo CSV debe contener las columnas 'cveGru' y 'nomGru'"
                )
                return
            
            for fila in reader:
                registros_archivo.append(fila)
                if grupos.find_one({"cveGru": fila['cveGru']}):
                    registros_duplicados.append(fila)
        
        # Determinar modo de importación
        modo = determinar_modo_importacion(registros_duplicados, len(registros_archivo))
        if not modo:
            return
        
        # Ejecutar importación
        resultado = ejecutar_importacion(registros_archivo, registros_duplicados, modo)
        
        # Mostrar resumen
        mostrar_resumen(resultado, "CSV", registros_duplicados)
        
    except Exception as e:
        messagebox.showerror("Error", f"Error durante la importación CSV: {e}")

def importar_json():
    """Importa JSON con ventana de duplicados"""
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivo JSON", "*.json"), ("Todos los archivos", "*.*")]
    )
    if not file_path:
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            datos = json.load(file)
            
            if isinstance(datos, dict):
                datos = [datos]
            
            registros_archivo = []
            registros_duplicados = []
            
            for documento in datos:
                # Limpiar _id si existe
                if '_id' in documento:
                    del documento['_id']
                
                # Validar campos requeridos
                if 'cveGru' not in documento or 'nomGru' not in documento:
                    continue
                
                registros_archivo.append(documento)
                if grupos.find_one({"cveGru": documento['cveGru']}):
                    registros_duplicados.append(documento)
        
        # Determinar modo de importación
        modo = determinar_modo_importacion(registros_duplicados, len(registros_archivo))
        if not modo:
            return
        
        # Ejecutar importación
        resultado = ejecutar_importacion(registros_archivo, registros_duplicados, modo)
        
        # Mostrar resumen
        mostrar_resumen(resultado, "JSON", registros_duplicados)
        
    except json.JSONDecodeError:
        messagebox.showerror("Error", "El archivo JSON no tiene un formato válido")
    except Exception as e:
        messagebox.showerror("Error", f"Error durante la importación JSON: {e}")

def importar_xml():
    """Importa XML con ventana de duplicados"""
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivo XML", "*.xml"), ("Todos los archivos", "*.*")]
    )
    if not file_path:
        return
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        registros_archivo = []
        registros_duplicados = []
        
        # Buscar elementos Grupo
        for grupo_elem in root.findall(".//Grupo"):
            clave_elem = grupo_elem.find("Clave")
            nombre_elem = grupo_elem.find("Nombre")
            
            if clave_elem is not None and nombre_elem is not None:
                if clave_elem.text and nombre_elem.text:
                    registro = {
                        'cveGru': clave_elem.text,
                        'nomGru': nombre_elem.text
                    }
                    registros_archivo.append(registro)
                    if grupos.find_one({"cveGru": clave_elem.text}):
                        registros_duplicados.append(registro)
        
        if not registros_archivo:
            messagebox.showwarning("Aviso", "No se encontraron registros válidos en el archivo XML")
            return
        
        # Determinar modo de importación
        modo = determinar_modo_importacion(registros_duplicados, len(registros_archivo))
        if not modo:
            return
        
        # Ejecutar importación
        resultado = ejecutar_importacion(registros_archivo, registros_duplicados, modo)
        
        # Mostrar resumen
        mostrar_resumen(resultado, "XML", registros_duplicados)
        
    except ET.ParseError:
        messagebox.showerror("Error", "El archivo XML no tiene un formato válido")
    except Exception as e:
        messagebox.showerror("Error", f"Error durante la importación XML: {e}")

# ============================================
# VENTANA DE DUPLICADOS IMPORTAR
# ============================================
def mostrar_ventana_duplicados(registros_duplicados, total_registros):
    """
    Muestra una ventana con la lista de registros duplicados
    Retorna: 'actualizar', 'saltar' o 'cancelar'
    """
    ventana = tk.Toplevel()
    ventana.title("Registros Duplicados Encontrados")
    ventana.geometry("450x400")
    ventana.transient()
    ventana.grab_set()
    
    # Frame para el mensaje
    frame_msg = tk.Frame(ventana, padx=8, pady=5)
    frame_msg.pack(fill="x")
    
    tk.Label(
        frame_msg, 
        text=f"Se encontraron {len(registros_duplicados)} registros que ya existen en la BD:",
        font=("Arial", 10, "bold")
    ).pack(anchor="w")
    
    tk.Label(
        frame_msg,
        text=f"Total de registros en el archivo: {total_registros}",
        font=("Arial", 9)
    ).pack(anchor="w")
    
    # Frame para la lista (con scroll)
    frame_lista = tk.Frame(ventana, padx=5, pady=5)
    frame_lista.pack(fill="both", expand=True)
    
    # Crear TreeView para mostrar los duplicados
    columnas = ("Clave", "Nombre")
    tree = ttk.Treeview(frame_lista, columns=columnas, show="headings", height=4)
    
    # Definir encabezados
    tree.heading("Clave", text="Clave del Grupo")
    tree.heading("Nombre", text="Nombre del Grupo")
    
    # Ajustar anchos
    tree.column("Clave", width=120)
    tree.column("Nombre", width=380)
    
    # Agregar scrollbar
    scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Empaquetar
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Insertar datos duplicados
    for reg in registros_duplicados:
        tree.insert("", "end", values=(reg['cveGru'], reg['nomGru']))
    
    # Frame para opciones
    frame_opciones = tk.Frame(ventana, padx=10, pady=10)
    frame_opciones.pack(fill="x")
    
    tk.Label(
        frame_opciones,
        text="¿Qué desea hacer con estos registros?",
        font=("Arial", 9, "bold")
    ).pack(anchor="w", pady=(0, 5))
    
    # Variable para guardar la decisión
    decision = tk.StringVar(value="")
    
    # Botones de opción
    rb_actualizar = tk.Radiobutton(
        frame_opciones, 
        text="Actualizar los existentes (sobrescribir con datos del archivo)",
        variable=decision, 
        value="actualizar"
    )
    rb_actualizar.pack(anchor="w", pady=2)
    
    rb_saltar = tk.Radiobutton(
        frame_opciones, 
        text="Saltar duplicados (solo insertar registros nuevos)",
        variable=decision, 
        value="saltar"
    )
    rb_saltar.pack(anchor="w", pady=2)
    
    rb_cancelar = tk.Radiobutton(
        frame_opciones, 
        text="Cancelar importación",
        variable=decision, 
        value="cancelar"
    )
    rb_cancelar.pack(anchor="w", pady=2)
    
    # Seleccionar "Saltar" por defecto (más seguro)
    rb_saltar.select()
    
    # Frame para botones de acción
    frame_botones = tk.Frame(ventana, padx=10, pady=10)
    frame_botones.pack(fill="x")
    
    resultado = [False]
    
    def aceptar():
        resultado[0] = decision.get()
        ventana.destroy()
    
    def cancelar():
        resultado[0] = "cancelar"
        ventana.destroy()
    
    tk.Button(
        frame_botones, 
        text="Aceptar", 
        command=aceptar,
        bg="#4CAF50", 
        fg="white",
        width=10
    ).pack(side="left", padx=5)
    
    tk.Button(
        frame_botones, 
        text="Cancelar", 
        command=cancelar,
        bg="#f44336", 
        fg="white",
        width=10
    ).pack(side="left", padx=5)
    
    # Esperar a que se cierre la ventana
    ventana.wait_window()
    
    return resultado[0]

# ============================================
# FUNCIONES AUXILIARES PARA IMPORTACIÓN
# ============================================

def determinar_modo_importacion(registros_duplicados, total_registros):
    """
    Determina el modo de importación basado en los duplicados
    Retorna: 'actualizar', 'saltar', 'insertar' o None
    """
    if registros_duplicados:
        # Mostrar ventana con duplicados
        modo = mostrar_ventana_duplicados(registros_duplicados, total_registros)
        return modo if modo != "cancelar" else None
    else:
        # No hay duplicados, preguntar confirmación
        respuesta = messagebox.askyesno(
            "Confirmar importación",
            f"Se encontraron {total_registros} registros nuevos para importar.\n"
            "¿Desea continuar?"
        )
        return "insertar" if respuesta else None

def ejecutar_importacion(registros_archivo, registros_duplicados, modo):
    """
    Ejecuta la importación según el modo elegido
    Retorna diccionario con resultados
    """
    insertados = 0
    actualizados = 0
    saltados = 0
    errores = 0
    
    for fila in registros_archivo:
        try:
            existe = grupos.find_one({"cveGru": fila['cveGru']})
            
            if existe:
                if modo == "actualizar":
                    grupos.update_one(
                        {"cveGru": fila['cveGru']},
                        {"$set": {"nomGru": fila['nomGru']}}
                    )
                    actualizados += 1
                else:  # modo == "saltar"
                    saltados += 1
            else:
                grupos.insert_one({
                    "cveGru": fila['cveGru'],
                    "nomGru": fila['nomGru']
                })
                insertados += 1
                
        except Exception as e:
            errores += 1
            print(f"Error con registro {fila.get('cveGru', 'Unknown')}: {e}")
    
    return {
        "insertados": insertados,
        "actualizados": actualizados,
        "saltados": saltados,
        "errores": errores,
        "total": len(registros_archivo)
    }

def mostrar_resumen(resultado, formato, registros_duplicados):
    """
    Muestra un resumen detallado de la importación
    """
    resumen = (
        f" IMPORTACIÓN {formato} COMPLETADA\n\n"
        f" Registros insertados: {resultado['insertados']}\n"
        f" Registros actualizados: {resultado['actualizados']}\n"
        f" Registros saltados: {resultado['saltados']}\n"
        f" Errores: {resultado['errores']}\n\n"
        f" Total procesados: {resultado['total']}"
    )
    
    if registros_duplicados:
        resumen += f" Registros duplicados encontrados:\n"
        # Mostrar hasta 15 duplicados para no saturar
        for i, dup in enumerate(registros_duplicados[:15], 1):
            resumen += f"  {i}. {dup['cveGru']} - {dup['nomGru']}\n"
        if len(registros_duplicados) > 15:
            resumen += f"  ... y {len(registros_duplicados) - 15} más"
    
    messagebox.showinfo(f"Resultado importación {formato}", resumen)