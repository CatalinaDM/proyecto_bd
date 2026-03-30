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

# ============================================
# FUNCIONES PARA ALUMNO
# ============================================

def obtener_claves_existentes_alumno(coleccion="Alumno", db="BD_GrupoAlumno"):
    """Obtiene todas las claves existentes en la colección Alumno"""
    try:
        js_code = f'print(JSON.stringify(db.getSiblingDB("{db}").{coleccion}.find({{}}, {{"cveAlu": 1, "_id": 0}}).toArray()))'
        
        tmp_js = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
        tmp_js.write(js_code)
        tmp_js.close()
        
        try:
            comando = ["mongosh", "--quiet", tmp_js.name]
            resultado = subprocess.run(comando, capture_output=True, text=True)
            if resultado.returncode == 0 and resultado.stdout.strip():
                try:
                    # Buscar la línea que sea JSON válido
                    for linea in reversed(resultado.stdout.strip().splitlines()):
                        linea = linea.strip()
                        if linea.startswith("["):
                            datos = json.loads(linea)
                            claves = set(str(item.get("cveAlu")) for item in datos if "cveAlu" in item)
                            return claves
                except Exception as e:
                    print(f"DEBUG - error parseando claves: {e}")
                    return set()
            return set()
        finally:
            if os.path.exists(tmp_js.name):
                os.unlink(tmp_js.name)
    except Exception as e:
        print(f"Error obteniendo claves: {e}")
        return set()

def crear_indice_unico_alumno_si_no_existe(coleccion="Alumno", db="BD_GrupoAlumno"):
    """Crea índice único para cveAlu si no existe"""
    try:
        comando = [
            "mongosh", "--quiet", "--eval",
            f'db.getSiblingDB("{db}").{coleccion}.createIndex({{ "cveAlu": 1 }}, {{ unique: true, name: "unique_cveAlu" }})'
        ]
        subprocess.run(comando, capture_output=True, text=True)
        return True
    except:
        return False

def validar_grupo_existe(cveGru, db="BD_GrupoAlumno"):
    """Valida que el grupo exista en la colección Grupo"""
    try:
        js_code = f'print(JSON.stringify(db.getSiblingDB("{db}").Grupo.findOne({{ "cveGru": "{cveGru}" }})))'
        
        tmp_js = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
        tmp_js.write(js_code)
        tmp_js.close()
        
        try:
            comando = ["mongosh", "--quiet", tmp_js.name]
            resultado = subprocess.run(comando, capture_output=True, text=True)
            salida = resultado.stdout.strip()
            print(f"DEBUG validar_grupo '{cveGru}' returncode:{resultado.returncode} salida:[{salida[:100]}] stderr:[{resultado.stderr[:50]}]")
            
            if resultado.returncode != 0 or not salida:
                return False
            
            lineas = [l.strip() for l in salida.splitlines() if l.strip()]
            for linea in reversed(lineas):
                if linea == "null":
                    return False
                if linea.startswith("{"):
                    return True
            return False
        finally:
            if os.path.exists(tmp_js.name):
                os.unlink(tmp_js.name)
    except Exception as e:
        print(f"DEBUG validar_grupo exception: {e}")
        return False

def mostrar_ventana_duplicados_alumno(registros_duplicados, total_registros, grupos_invalidos=None, nombre_archivo=""):

    ventana = Toplevel()
    ventana.title("Validación de Alumnos")
    ventana.geometry("650x450")
    ventana.transient()
    ventana.grab_set()

    # ── Mensajes de resumen 
    frame_msg = Frame(ventana, padx=8, pady=5)
    frame_msg.pack(fill="x")

    if registros_duplicados:
        Label(
            frame_msg,
            text=f" Se encontraron {len(registros_duplicados)} alumnos con cveAlu que ya existe en BD:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

    if grupos_invalidos:
        Label(
            frame_msg,
            text=f" Se encontraron {len(grupos_invalidos)} alumnos con grupos que NO existen en BD:",
            font=("Arial", 10, "bold"),
            fg="red"
        ).pack(anchor="w", pady=(5, 0))

    Label(
        frame_msg,
        text=f"Total de registros en el archivo: {total_registros}",
        font=("Arial", 9)
    ).pack(anchor="w", pady=(5, 0))

    if nombre_archivo:
        Label(
            frame_msg,
            text=f"Archivo: {os.path.basename(nombre_archivo)}",
            font=("Arial", 8, "italic")
        ).pack(anchor="w")

    # ── Tabla 
    frame_lista = Frame(ventana, padx=5, pady=5)
    frame_lista.pack(fill="both", expand=False)

    columnas = ("cveAlu", "nomAlu", "edaAlu", "cveGru", "problema")
    tree = ttk.Treeview(frame_lista, columns=columnas, show="headings", height=5)

    tree.heading("cveAlu",   text="Clave Alumno")
    tree.heading("nomAlu",   text="Nombre")
    tree.heading("edaAlu",   text="Edad")
    tree.heading("cveGru",   text="Grupo")
    tree.heading("problema", text="Problema")

    tree.column("cveAlu",   width=80)
    tree.column("nomAlu",   width=180)
    tree.column("edaAlu",   width=50)
    tree.column("cveGru",   width=80)
    tree.column("problema", width=120)

    scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for reg in (registros_duplicados or []):
        tree.insert("", "end", values=(
            reg.get('cveAlu','N/A'), reg.get('nomAlu','N/A'),
            reg.get('edaAlu','N/A'), reg.get('cveGru','N/A'),
            "Clave duplicada"
        ))
    for reg in (grupos_invalidos or []):
        tree.insert("", "end", values=(
            reg.get('cveAlu','N/A'), reg.get('nomAlu','N/A'),
            reg.get('edaAlu','N/A'), reg.get('cveGru','N/A'),
            "Grupo no existe"
        ))

    # ── Opciones según caso
    frame_opciones = Frame(ventana, padx=10, pady=5)
    frame_opciones.pack(fill="x")

    Label(frame_opciones, text="¿Qué desea hacer?", font=("Arial", 9, "bold")).pack(anchor="w", pady=(0, 5))

    decision = StringVar(value="saltar")

    # CASO 1: duplicados Y grupos inválidos
    if registros_duplicados and grupos_invalidos:
        Radiobutton(
            frame_opciones,
            text="Actualizar alumnos duplicados y saltar los de grupo inválido",
            variable=decision, value="actualizar_y_saltar_grupos"
        ).pack(anchor="w", pady=2)

        Radiobutton(
            frame_opciones,
            text="Saltar TODOS los registros con problemas (solo importar los completamente válidos)",
            variable=decision, value="saltar"
        ).pack(anchor="w", pady=2)

    # CASO 2: solo duplicados
    elif registros_duplicados and not grupos_invalidos:
        Radiobutton(
            frame_opciones,
            text="Actualizar alumnos existentes (sobrescribir con datos del archivo)",
            variable=decision, value="actualizar"
        ).pack(anchor="w", pady=2)

        Radiobutton(
            frame_opciones,
            text="Saltar duplicados (solo insertar alumnos nuevos)",
            variable=decision, value="saltar"
        ).pack(anchor="w", pady=2)

    # CASO 3: solo grupos inválidos
    elif grupos_invalidos and not registros_duplicados:
        Radiobutton(
            frame_opciones,
            text="Saltar alumnos con grupo inválido (solo importar los válidos)",
            variable=decision, value="saltar"
        ).pack(anchor="w", pady=2)

        Radiobutton(
            frame_opciones,
            text="Corregir los grupos en el archivo y volver a importar",
            variable=decision, value="cancelar"
        ).pack(anchor="w", pady=2)

    # Siempre aparece cancelar
    Radiobutton(
        frame_opciones,
        text="Cancelar importación",
        variable=decision, value="cancelar"
    ).pack(anchor="w", pady=2)

    # ── Botones 
    frame_botones = Frame(ventana, padx=10, pady=10)
    frame_botones.pack(fill="x")

    resultado = [None]

    def aceptar():
        resultado[0] = decision.get()
        ventana.destroy()

    Button(frame_botones, text="Aceptar", command=aceptar,
           bg="#4CAF50", fg="white", width=12).pack(side="left", padx=5)
    Button(frame_botones, text="Cancelar",
           command=lambda: [resultado.__setitem__(0, "cancelar"), ventana.destroy()],
           bg="#f44336", fg="white", width=12).pack(side="left", padx=5)

    ventana.wait_window()
    return resultado[0]

# ============================================
# FUNCIONES DE LECTURA PARA ALUMNO
# ============================================

def leer_csv_alumno(archivo):
    """Lee CSV de alumnos"""
    registros = []
    claves_archivo = set()
    duplicados_internos = []
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for col in ['cveAlu', 'nomAlu', 'edaAlu', 'cveGru']:
                if col not in reader.fieldnames:
                    messagebox.showerror("Error", f"El CSV debe contener '{col}'")
                    return None, None, None
            for fila in reader:
                cve = fila.get('cveAlu', '').strip()
                if cve in claves_archivo:
                    duplicados_internos.append(fila)
                else:
                    claves_archivo.add(cve)
                    try:
                        registros.append({
                            'cveAlu': cve,
                            'nomAlu': fila.get('nomAlu', '').strip(),
                            'edaAlu': int(fila.get('edaAlu', 0)),
                            'cveGru': fila.get('cveGru', '').strip()
                        })
                    except ValueError:
                        messagebox.showerror("Error", f"Edad inválida para clave {cve}")
                        return None, None, None
        return registros, duplicados_internos, len(duplicados_internos) > 0
    except Exception as e:
        messagebox.showerror("Error", f"Error leyendo CSV: {e}")
        return None, None, None

def leer_json_alumno(archivo):
    """Lee JSON de alumnos"""
    registros = []
    claves_archivo = set()
    duplicados_internos = []
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            datos = json.load(file)
        if isinstance(datos, dict):
            datos = [datos]
        for documento in datos:
            if 'cveAlu' not in documento:
                continue
            cve = str(documento.get('cveAlu', '')).strip()
            if cve in claves_archivo:
                duplicados_internos.append(documento)
            else:
                claves_archivo.add(cve)
                registros.append({
                    'cveAlu': cve,
                    'nomAlu': documento.get('nomAlu', '').strip(),
                    'edaAlu': int(documento.get('edaAlu', 0)),
                    'cveGru': documento.get('cveGru', '').strip()
                })
        return registros, duplicados_internos, len(duplicados_internos) > 0
    except Exception as e:
        messagebox.showerror("Error", f"Error leyendo JSON: {e}")
        return None, None, None

def leer_xml_alumno(archivo):
    """Lee XML de alumnos"""
    registros = []
    claves_archivo = set()
    duplicados_internos = []

    def get_text(elem, tag):
        """Obtiene texto de una etiqueta de forma segura, probando variantes"""
        # Intentar búsqueda directa
        found = elem.find(tag)
        if found is not None and found.text and found.text.strip():
            return found.text.strip()
        # Intentar búsqueda case-insensitive recorriendo hijos
        for child in elem:
            if child.tag.strip().lower() == tag.lower():
                if child.text and child.text.strip():
                    return child.text.strip()
        return ""

    try:
        with open(archivo, 'r', encoding='utf-8-sig') as f:   # utf-8-sig elimina BOM si existe
            contenido = f.read()

        root = ET.fromstring(contenido)

        for alumno_elem in root.findall(".//Alumno"):
            cve    = get_text(alumno_elem, "Clave")
            nombre = get_text(alumno_elem, "Nombre")
            edad   = get_text(alumno_elem, "Edad")
            grupo  = get_text(alumno_elem, "Grupo")


            if not cve or not nombre:
                continue

            try:
                edad_int = int(edad) if edad else 0
            except ValueError:
                messagebox.showerror("Error", f"Edad inválida para clave {cve}")
                return None, None, None

            datos = {
                'cveAlu': cve,
                'nomAlu': nombre,
                'edaAlu': edad_int,
                'cveGru': grupo
            }

            if cve in claves_archivo:
                duplicados_internos.append(datos)
            else:
                claves_archivo.add(cve)
                registros.append(datos)

        return registros, duplicados_internos, len(duplicados_internos) > 0
    except Exception as e:
        messagebox.showerror("Error", f"Error leyendo XML: {e}")
        return None, None, None

def mostrar_resumen_importacion_alumno(resultado, formato, archivo_nombre):
    """Muestra resumen de importación de alumnos"""
    resumen = (
        f" IMPORTACIÓN DE ALUMNOS {formato} COMPLETADA\n\n"
        f"Resumen:\n"
        f"  • Alumnos insertados:   {resultado['insertados']}\n"
        f"  • Alumnos actualizados: {resultado['actualizados']}\n"
        f"  • Alumnos saltados:     {resultado['saltados']}\n"
        f"  • Errores:              {resultado['errores']}\n\n"
        f"Archivo: {os.path.basename(archivo_nombre)}\n"
        f"Total procesados: {resultado['total']}"
    )
    messagebox.showinfo(f"Resultado importación Alumnos {formato}", resumen)

# ============================================
# FUNCIÓN PRINCIPAL PARA ALUMNO
# ============================================

def importar_alumno_con_control(tipo_archivo):
    """Importa alumnos con control de duplicados y validación de grupos"""

    mongoimport = encontrar_mongoimport()
    if not mongoimport:
        messagebox.showerror("Error", "No se encontró mongoimport.\nInstala MongoDB Tools")
        return

    extensiones = {'csv': [("CSV","*.csv")], 'json': [("JSON","*.json")], 'xml': [("XML","*.xml")]}
    archivo = filedialog.askopenfilename(
        title=f"Seleccionar archivo de ALUMNOS {tipo_archivo.upper()}",
        filetypes=extensiones[tipo_archivo]
    )
    if not archivo:
        return

    lectores = {'csv': leer_csv_alumno, 'json': leer_json_alumno, 'xml': leer_xml_alumno}
    registros, duplicados_internos, hay_duplicados_internos = lectores[tipo_archivo](archivo)

    if registros is None:
        return
    if not registros:
        messagebox.showwarning("Aviso", "No se encontraron registros válidos en el archivo")
        return

    # Advertencia duplicados internos del archivo
    if hay_duplicados_internos:
        if not messagebox.askyesno(
            "Duplicados en archivo",
            f"El archivo contiene {len(duplicados_internos)} claves duplicadas.\n"
            "Solo se considerará el primer registro de cada clave dentro del archivo importado.\n\n"
            "¿Desea continuar?"
        ):
            return

    # Validar grupos en BD
    grupos_invalidos  = []
    registros_validos = []
    for reg in registros:
        if validar_grupo_existe(reg['cveGru']):
            registros_validos.append(reg)
        else:
            grupos_invalidos.append(reg)

    # Identificar duplicados con BD (solo sobre registros con grupo válido)
    claves_existentes    = obtener_claves_existentes_alumno()
    registros_nuevos     = [r for r in registros_validos if r['cveAlu'] not in claves_existentes]
    registros_duplicados = [r for r in registros_validos if r['cveAlu'] in claves_existentes]

    # ── Decidir qué hacer 
    registros_a_importar = []
    resumen_stats        = {}

    if registros_duplicados or grupos_invalidos:
        modo = mostrar_ventana_duplicados_alumno(
            registros_duplicados, len(registros), grupos_invalidos, archivo
        )

        if modo is None or modo == "cancelar":
            return

        # CASO 1-A: actualizar duplicados + saltar grupos inválidos
        elif modo == "actualizar_y_saltar_grupos":
            registros_a_importar = registros_validos       
            resumen_stats = {
                "insertados":   len(registros_nuevos),
                "actualizados": len(registros_duplicados),
                "saltados":     len(grupos_invalidos),
                "errores": 0,   "total": len(registros)
            }

        # CASO 2-A: actualizar todos los duplicados (no hay grupos inválidos)
        elif modo == "actualizar":
            registros_a_importar = registros_validos
            resumen_stats = {
                "insertados":   len(registros_nuevos),
                "actualizados": len(registros_duplicados),
                "saltados":     0,
                "errores": 0,   "total": len(registros)
            }

        # CASO 1-B / CASO 2-B / CASO 3-A: saltar problemáticos, solo insertar nuevos válidos
        elif modo == "saltar":
            registros_a_importar = registros_nuevos
            resumen_stats = {
                "insertados":   len(registros_nuevos),
                "actualizados": 0,
                "saltados":     len(registros_duplicados) + len(grupos_invalidos),
                "errores": 0,   "total": len(registros)
            }

        else:
            return

    else:
        # confirmar e insertar todo
        if not messagebox.askyesno(
            "Confirmar importación",
            f"Se encontraron {len(registros_nuevos)} alumnos nuevos para importar.\n"
            "¿Desea continuar?"
        ):
            return
        registros_a_importar = registros_nuevos
        resumen_stats = {
            "insertados": len(registros_nuevos),
            "actualizados": 0, "saltados": 0,
            "errores": 0, "total": len(registros)
        }

    if not registros_a_importar:
        messagebox.showinfo("Aviso", "No hay registros para importar con la opción seleccionada.")
        return

    # ── Crear archivo temporal y ejecutar mongoimport 
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
    json.dump(registros_a_importar, temp_file, indent=2, ensure_ascii=False)
    temp_file.close()

    crear_indice_unico_alumno_si_no_existe()

    comando = [
        mongoimport,
        "--db=BD_GrupoAlumno", "--collection=Alumno",
        "--type=json", "--jsonArray",
        f"--file={temp_file.name}",
        "--mode=upsert", "--upsertFields=cveAlu"
    ]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode == 0:
            mostrar_resumen_importacion_alumno(resumen_stats, tipo_archivo.upper(), archivo)
        else:
            messagebox.showerror("Error", f"Mongoimport falló:\n\n{resultado.stderr[:500]}")
    except Exception as e:
        messagebox.showerror("Error", f"Error ejecutando mongoimport: {e}")
    finally:
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

# ============================================
# FUNCIONES ESPECÍFICAS POR TIPO DE ARCHIVO
# ============================================

def importar_csv_alumno():
    importar_alumno_con_control('csv')

def importar_json_alumno():
    importar_alumno_con_control('json')

def importar_xml_alumno():
    importar_alumno_con_control('xml')