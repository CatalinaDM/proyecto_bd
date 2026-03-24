import subprocess
import os
import json
import xml.etree.ElementTree as ET
import tempfile
import csv
from tkinter import filedialog, messagebox, Toplevel, Label, Frame, Button, StringVar, Radiobutton, ttk

def encontrar_mongoimport():
    """Busca mongoimport en ubicaciones comunes"""
    posibles_rutas = [
        r"C:\Program Files\MongoDB\Tools\100\bin\mongoimport.exe",
        r"C:\Program Files\MongoDB\Tools\110\bin\mongoimport.exe",
        r"C:\Program Files\MongoDB\Tools\120\bin\mongoimport.exe",
        r"C:\Program Files\MongoDB\Server\7.0\bin\mongoimport.exe",
        r"C:\Program Files\MongoDB\Server\6.0\bin\mongoimport.exe",
        r"C:\Program Files\MongoDB\Server\5.0\bin\mongoimport.exe",
    ]
    
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            return ruta
    
    try:
        subprocess.run(["mongoimport", "--version"], capture_output=True)
        return "mongoimport"
    except:
        return None

def obtener_claves_existentes(coleccion="Grupo", db="BD_GrupoAlumno"):
    """Obtiene todas las claves existentes en la colección usando mongosh"""
    try:
        comando = [
            "mongosh",
            "--quiet",
            "--eval",
            f'db.getSiblingDB("{db}").{coleccion}.find({{}}, {{"cveGru": 1, "_id": 0}}).toArray()'
        ]
        
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode == 0 and resultado.stdout.strip():
            try:
                datos = json.loads(resultado.stdout.strip())
                return set(item.get("cveGru") for item in datos if "cveGru" in item)
            except:
                return set()
        return set()
    except:
        return set()

def crear_indice_unico_si_no_existe(coleccion="Grupo", db="BD_GrupoAlumno"):
    """Intenta crear un índice único para cveGru si no existe"""
    try:
        comando = [
            "mongosh",
            "--quiet",
            "--eval",
            f'db.getSiblingDB("{db}").{coleccion}.createIndex({{ "cveGru": 1 }}, {{ unique: true, name: "unique_cveGru" }})'
        ]
        subprocess.run(comando, capture_output=True, text=True)
        return True
    except:
        return False

# ============================================
# VENTANA DE DUPLICADOS (adaptada del primer código)
# ============================================
def mostrar_ventana_duplicados(registros_duplicados, total_registros, nombre_archivo=""):
    """
    Muestra una ventana con la lista de registros duplicados
    Retorna: 'actualizar', 'saltar' o 'cancelar'
    """
    ventana = Toplevel()
    ventana.title("Registros Duplicados Encontrados")
    ventana.geometry("550x450")
    ventana.transient()
    ventana.grab_set()
    
    # Frame para el mensaje
    frame_msg = Frame(ventana, padx=8, pady=5)
    frame_msg.pack(fill="x")
    
    Label(
        frame_msg, 
        text=f"Se encontraron {len(registros_duplicados)} registros con claves que ya existen:",
        font=("Arial", 10, "bold")
    ).pack(anchor="w")
    
    Label(
        frame_msg,
        text=f"Total de registros en el archivo: {total_registros}",
        font=("Arial", 9)
    ).pack(anchor="w")
    
    if nombre_archivo:
        Label(
            frame_msg,
            text=f"Archivo: {os.path.basename(nombre_archivo)}",
            font=("Arial", 8, "italic")
        ).pack(anchor="w")
    
    # Frame para la lista (con scroll)
    frame_lista = Frame(ventana, padx=5, pady=5)
    frame_lista.pack(fill="both", expand=True)
    
    # Crear TreeView para mostrar los duplicados
    columnas = ("Clave (cveGru)", "Nombre")
    tree = ttk.Treeview(frame_lista, columns=columnas, show="headings", height=8)
    
    # Definir encabezados
    tree.heading("Clave (cveGru)", text="Clave del Grupo")
    tree.heading("Nombre", text="Nombre del Grupo")
    
    # Ajustar anchos
    tree.column("Clave (cveGru)", width=150)
    tree.column("Nombre", width=350)
    
    # Agregar scrollbar
    scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Empaquetar
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Insertar datos duplicados
    for reg in registros_duplicados:
        tree.insert("", "end", values=(reg.get('cveGru', 'N/A'), reg.get('nomGru', 'N/A')))
    
    # Frame para opciones
    frame_opciones = Frame(ventana, padx=10, pady=10)
    frame_opciones.pack(fill="x")
    
    Label(
        frame_opciones,
        text="¿Qué desea hacer con estos registros?",
        font=("Arial", 9, "bold")
    ).pack(anchor="w", pady=(0, 5))
    
    # Variable para guardar la decisión
    decision = StringVar(value="saltar")  # "saltar" por defecto
    
    # Botones de opción
    rb_actualizar = Radiobutton(
        frame_opciones, 
        text="Actualizar los existentes (sobrescribir con datos del archivo)",
        variable=decision, 
        value="actualizar"
    )
    rb_actualizar.pack(anchor="w", pady=2)
    
    rb_saltar = Radiobutton(
        frame_opciones, 
        text="Saltar duplicados (solo insertar registros nuevos)",
        variable=decision, 
        value="saltar"
    )
    rb_saltar.pack(anchor="w", pady=2)
    
    rb_cancelar = Radiobutton(
        frame_opciones, 
        text="Cancelar importación",
        variable=decision, 
        value="cancelar"
    )
    rb_cancelar.pack(anchor="w", pady=2)
    
    # Frame para botones de acción
    frame_botones = Frame(ventana, padx=10, pady=10)
    frame_botones.pack(fill="x")
    
    resultado = [None]
    
    def aceptar():
        resultado[0] = decision.get()
        ventana.destroy()
    
    def cancelar():
        resultado[0] = "cancelar"
        ventana.destroy()
    
    Button(
        frame_botones, 
        text="Aceptar", 
        command=aceptar,
        bg="#4CAF50", 
        fg="white",
        width=12
    ).pack(side="left", padx=5)
    
    Button(
        frame_botones, 
        text="Cancelar", 
        command=cancelar,
        bg="#f44336", 
        fg="white",
        width=12
    ).pack(side="left", padx=5)
    
    # Esperar a que se cierre la ventana
    ventana.wait_window()
    
    return resultado[0]

def mostrar_resumen_importacion(resultado, formato, archivo_nombre):
    """Muestra un resumen detallado de la importación"""
    resumen = (
        f" IMPORTACIÓN {formato} COMPLETADA\n\n"
        f" Resumen:\n"
        f"   • Registros insertados: {resultado['insertados']}\n"
        f"   • Registros actualizados: {resultado['actualizados']}\n"
        f"   • Registros saltados: {resultado['saltados']}\n"
        f"   • Errores: {resultado['errores']}\n\n"
        f"Archivo: {os.path.basename(archivo_nombre)}\n"
        f"Total procesados: {resultado['total']}"
    )
    
    messagebox.showinfo(f"Resultado importación {formato}", resumen)

# ============================================
# FUNCIONES DE LECTURA DE ARCHIVOS
# ============================================

def leer_csv_con_duplicados(archivo):
    """Lee archivo CSV y detecta duplicados internos y contra BD"""
    registros = []
    claves_archivo = set()
    duplicados_internos = []
    
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            if 'cveGru' not in reader.fieldnames or 'nomGru' not in reader.fieldnames:
                messagebox.showerror("Error", "El CSV debe contener 'cveGru' y 'nomGru'")
                return None, None, None
            
            for fila in reader:
                cve = fila.get('cveGru', '').strip()
                if cve in claves_archivo:
                    duplicados_internos.append(fila)
                else:
                    claves_archivo.add(cve)
                    registros.append({
                        'cveGru': cve,
                        'nomGru': fila.get('nomGru', '').strip()
                    })
            
            return registros, duplicados_internos, len(duplicados_internos) > 0
    except Exception as e:
        messagebox.showerror("Error", f"Error leyendo CSV: {e}")
        return None, None, None

def leer_json_con_duplicados(archivo):
    """Lee archivo JSON y detecta duplicados internos y contra BD"""
    registros = []
    claves_archivo = set()
    duplicados_internos = []
    
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            datos = json.load(file)
            
            if isinstance(datos, dict):
                datos = [datos]
            
            for documento in datos:
                if 'cveGru' not in documento or 'nomGru' not in documento:
                    continue
                
                cve = str(documento.get('cveGru', '')).strip()
                if cve in claves_archivo:
                    duplicados_internos.append(documento)
                else:
                    claves_archivo.add(cve)
                    registros.append({
                        'cveGru': cve,
                        'nomGru': documento.get('nomGru', '').strip()
                    })
            
            return registros, duplicados_internos, len(duplicados_internos) > 0
    except Exception as e:
        messagebox.showerror("Error", f"Error leyendo JSON: {e}")
        return None, None, None

def leer_xml_con_duplicados(archivo):
    """Lee archivo XML y detecta duplicados internos y contra BD"""
    registros = []
    claves_archivo = set()
    duplicados_internos = []
    
    try:
        tree = ET.parse(archivo)
        root = tree.getroot()
        
        for grupo_elem in root.findall(".//Grupo"):
            clave_elem = grupo_elem.find("Clave")
            nombre_elem = grupo_elem.find("Nombre")
            
            if clave_elem is not None and clave_elem.text and nombre_elem is not None and nombre_elem.text:
                cve = clave_elem.text.strip()
                
                if cve in claves_archivo:
                    duplicados_internos.append({
                        'cveGru': cve,
                        'nomGru': nombre_elem.text.strip()
                    })
                else:
                    claves_archivo.add(cve)
                    registros.append({
                        'cveGru': cve,
                        'nomGru': nombre_elem.text.strip()
                    })
        
        return registros, duplicados_internos, len(duplicados_internos) > 0
    except Exception as e:
        messagebox.showerror("Error", f"Error leyendo XML: {e}")
        return None, None, None

# ============================================
# FUNCIÓN PRINCIPAL DE IMPORTACIÓN
# ============================================

def importar_con_control_duplicados(tipo_archivo):
    """
    Función genérica para importar cualquier tipo de archivo
    con control de duplicados
    """
    mongoimport = encontrar_mongoimport()
    if not mongoimport:
        messagebox.showerror("Error", "No se encontró mongoimport.\nInstala MongoDB Tools")
        return
    
    # Seleccionar archivo según tipo
    extensiones = {
        'csv': [("CSV", "*.csv")],
        'json': [("JSON", "*.json")],
        'xml': [("XML", "*.xml")]
    }
    
    archivo = filedialog.askopenfilename(
        title=f"Seleccionar archivo {tipo_archivo.upper()}", 
        filetypes=extensiones[tipo_archivo]
    )
    if not archivo:
        return
    
    # Leer archivo según tipo
    lectores = {
        'csv': leer_csv_con_duplicados,
        'json': leer_json_con_duplicados,
        'xml': leer_xml_con_duplicados
    }
    
    registros, duplicados_internos, hay_duplicados_internos = lectores[tipo_archivo](archivo)
    
    if registros is None:
        return
    
    if not registros:
        messagebox.showwarning("Aviso", "No se encontraron registros válidos en el archivo")
        return
    
    # Mostrar advertencia si hay duplicados internos
    if hay_duplicados_internos:
        if not messagebox.askyesno(
            "Duplicados en archivo",
            f"El archivo contiene {len(duplicados_internos)} claves duplicadas.\n"
            "Solo se considerará la primera ocurrencia de cada clave.\n\n"
            "¿Desea continuar?"
        ):
            return
    
    # Obtener claves existentes en BD
    claves_existentes = obtener_claves_existentes()
    
    # Identificar duplicados contra BD
    registros_nuevos = []
    registros_duplicados_bd = []
    
    for reg in registros:
        if reg['cveGru'] in claves_existentes:
            registros_duplicados_bd.append(reg)
        else:
            registros_nuevos.append(reg)
    
    # Si hay duplicados, mostrar ventana de opciones
    modo_importacion = "insertar_nuevos"
    
    if registros_duplicados_bd:
        modo = mostrar_ventana_duplicados(registros_duplicados_bd, len(registros), archivo)
        
        if modo == "cancelar":
            return
        elif modo == "actualizar":
            modo_importacion = "actualizar_todos"
        elif modo == "saltar":
            modo_importacion = "saltar_duplicados"
    else:
        # No hay duplicados, preguntar confirmación
        if not messagebox.askyesno(
            "Confirmar importación",
            f"Se encontraron {len(registros)} registros nuevos para importar.\n"
            "¿Desea continuar?"
        ):
            return
    
    # ============================================
    # EJECUTAR IMPORTACIÓN CON MONGOIMPORT
    # ============================================
    
    # Crear archivo temporal con los registros a importar
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
    
    if modo_importacion == "saltar_duplicados":
        # Solo importar registros nuevos
        json.dump(registros_nuevos, temp_file, indent=2, ensure_ascii=False)
        total_procesar = len(registros_nuevos)
    else:
        # Importar todos (para actualizar o insertar nuevos)
        json.dump(registros, temp_file, indent=2, ensure_ascii=False)
        total_procesar = len(registros)
    
    temp_file.close()
    
    # Intentar crear índice único (no afecta si ya existe)
    crear_indice_unico_si_no_existe()
    
    # Preparar comando mongoimport
    comando_base = [
        mongoimport,
        "--db=BD_GrupoAlumno",
        "--collection=Grupo",
        "--type=json",
        "--jsonArray",
        f"--file={temp_file.name}",
         "--mode=upsert",
         "--upsertFields=cveGru"
    ]
    
    if modo_importacion == "actualizar_todos":
        # Usar upsert para actualizar existentes e insertar nuevos
        comando = comando_base + ["--mode", "upsert", "--upsertFields", "cveGru"]
    else:
        # Para insertar nuevos o saltar duplicados:
        # Si hay duplicados y elegimos saltar, ya filtramos los nuevos
        # Usamos --stopOnError para evitar que un error detenga todo
        comando = comando_base + ["--stopOnError"]
    
    # Ejecutar comando
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        # Analizar resultado
        if resultado.returncode == 0:
            # Éxito - calcular estadísticas
            if modo_importacion == "saltar_duplicados":
                insertados = len(registros_nuevos)
                actualizados = 0
                saltados = len(registros_duplicados_bd)
            elif modo_importacion == "actualizar_todos":
                # No sabemos exactamente cuántos se actualizaron vs insertaron
                # Pero podemos estimar basado en duplicados previos
                insertados = len(registros_nuevos)
                actualizados = len(registros_duplicados_bd)
                saltados = 0
            else:  # insertar_nuevos (no había duplicados)
                insertados = len(registros)
                actualizados = 0
                saltados = 0
            
            resumen = {
                "insertados": insertados,
                "actualizados": actualizados,
                "saltados": saltados,
                "errores": 0,
                "total": len(registros)
            }
            
            mostrar_resumen_importacion(resumen, tipo_archivo.upper(), archivo)
            
        else:
            # Hubo error - mostrar y dar opción de reintentar
            error_msg = resultado.stderr
            messagebox.showerror(
                "Error en importación", 
                f"Mongoimport falló:\n\n{error_msg[:500]}" + 
                ("..." if len(error_msg) > 500 else "")
            )
            
            # Preguntar si quiere reintentar con otro método
            if messagebox.askyesno("Reintentar", "¿Desea reintentar la importación de forma manual?"):
                # Aquí podrías implementar un método alternativo
                pass
    
    except Exception as e:
        messagebox.showerror("Error", f"Error ejecutando mongoimport: {e}")
    
    finally:
        # Limpiar archivo temporal
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

# ============================================
# FUNCIONES ESPECÍFICAS PARA CADA TIPO
# ============================================

def importar_csv():
    """Importa CSV con control de duplicados"""
    importar_con_control_duplicados('csv')

def importar_json():
    """Importa JSON con control de duplicados"""
    importar_con_control_duplicados('json')

def importar_xml():
    """Importa XML con control de duplicados"""
    importar_con_control_duplicados('xml')