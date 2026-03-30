import subprocess
import os
from tkinter import filedialog, messagebox
from database.conexion import grupos

def encontrar_mongorestore():
    """Busca mongorestore en ubicaciones comunes"""
    posibles_rutas = [
        r"C:\Program Files\MongoDB\Tools\100\bin\mongorestore.exe",
        r"C:\Program Files\MongoDB\Tools\110\bin\mongorestore.exe",
        r"C:\Program Files\MongoDB\Tools\120\bin\mongorestore.exe",
        r"C:\Program Files\MongoDB\Server\7.0\bin\mongorestore.exe",
        r"C:\Program Files\MongoDB\Server\6.0\bin\mongorestore.exe",
        r"C:\Program Files\MongoDB\Server\5.0\bin\mongorestore.exe",
    ]
    
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            return ruta
    
    try:
        subprocess.run(["mongorestore", "--version"], capture_output=True)
        return "mongorestore"
    except:
        return None

def buscar_archivo_grupo(ruta_inicial):
    """
    Busca recursivamente el archivo Grupo.bson
    """
    print(f" Buscando Grupo.bson en: {ruta_inicial}")
    
    # Verificar archivos en carpeta actual
    try:
        archivos = os.listdir(ruta_inicial)
        if 'Grupo.bson' in archivos:
            ruta_completa = os.path.join(ruta_inicial, 'Grupo.bson')
            print(f"Encontrado en: {ruta_completa}")
            return ruta_completa
    except:
        pass
    
    # Buscar en subcarpetas
    try:
        for item in os.listdir(ruta_inicial):
            ruta_completa = os.path.join(ruta_inicial, item)
            if os.path.isdir(ruta_completa):
                resultado = buscar_archivo_grupo(ruta_completa)
                if resultado:
                    return resultado
    except:
        pass
    
    return None

def restaurar_backup():
    """Restaura SOLO la colección Grupo desde su archivo .bson"""
    try:
        # 1. Buscar mongorestore
        mongorestore_path = encontrar_mongorestore()
        if not mongorestore_path:
            messagebox.showerror("Error", "No se encontró mongorestore.\nInstala MongoDB Tools")
            return
        
        # 2. Seleccionar carpeta de backup (la que contiene todo)
        ruta_backup = filedialog.askdirectory(
            title="Seleccionar carpeta de backup (donde está Grupo.bson)"
        )
        
        if not ruta_backup:
            return
        
        # 3. Buscar el archivo Grupo.bson (recursivamente)
        ruta_grupo_bson = buscar_archivo_grupo(ruta_backup)
        
        if not ruta_grupo_bson:
            messagebox.showerror(
                " Error",
                f"No se encontró el archivo 'Grupo.bson' en:\n{ruta_backup}\n\n"
                "Asegúrate de seleccionar la carpeta correcta."
            )
            return
        
        # 4. Verificar datos actuales de Grupo
        grupos_actuales = grupos.count_documents({})
        
        usar_drop = False
        if grupos_actuales > 0:
            respuesta = messagebox.askyesno(
                "Datos existentes",
                f"Actualmente hay {grupos_actuales} grupos en la base de datos.\n\n"
                "¿Deseas ELIMINAR los datos actuales antes de restaurar?\n"
                "• Sí: Eliminar datos existentes (--drop)\n"
                "• No: Hacer merge con los datos actuales"
            )
            usar_drop = respuesta
        
        # 5. Construir comando - restaurar desde archivo .bson
        comando = [
            mongorestore_path,
            "--db=BD_GrupoAlumno",
            "--collection=Grupo",
            ruta_grupo_bson  # Ruta directa al archivo .bson
        ]
        
        if usar_drop:
            comando.append("--drop")
            mensaje_accion = "reemplazando"
        else:
            mensaje_accion = "fusionando con"
        
        # 6. Ejecutar
        print(f"Ejecutando: {' '.join(comando)}")
        
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # 7. Verificar resultado
        if resultado.returncode == 0:
            # Extraer cuántos documentos se restauraron
            grupos_restaurados = 0
            for linea in resultado.stdout.split('\n'):
                if "document(s) restored" in linea.lower():
                    import re
                    match = re.search(r'(\d+)\s+document', linea)
                    if match:
                        grupos_restaurados = match.group(1)
                        break
            
            messagebox.showinfo(
                " Restauración exitosa",
                f"Colección 'Grupo' restaurada correctamente.\n\n"
                f" Grupos {mensaje_accion}: {grupos_restaurados}\n"
            )
        else:
            messagebox.showerror(
                "Error",
                f"Error al ejecutar mongorestore:\n\n{resultado.stderr}"
            )
            
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {str(e)}")



def restaurar_bd_completa():
    """Restaura la base de datos completa usando mongorestore"""
    
    # 1. Buscar mongorestore
    mongorestore_path = encontrar_mongorestore()
    if not mongorestore_path:
        messagebox.showerror("Error", "No se encontró mongorestore.\nInstala MongoDB Tools")
        return False
    
    # 2. Seleccionar carpeta de backup (la que contiene todo)
    ruta_backup = filedialog.askdirectory(
        title="Seleccionar carpeta de backup"
    )
    
    # Si el usuario cancela la selección
    if not ruta_backup:
        messagebox.showwarning("Cancelado", "No se seleccionó ninguna carpeta")
        return False
    
    # Validación 1: Verificar que la ruta existe
    if not os.path.exists(ruta_backup):
        messagebox.showerror("Error", f"La ruta '{ruta_backup}' no existe")
        return False
    
    # Validación 2: Verificar que la ruta tiene archivos .bson
    try:
        archivos_bson = [f for f in os.listdir(ruta_backup) if f.endswith('.bson')]
        if not archivos_bson:
            messagebox.showerror("Error", f"No se encontraron archivos .bson en '{ruta_backup}'")
            return False
    except PermissionError:
        messagebox.showerror("Error", f"No se tienen permisos para leer '{ruta_backup}'")
        return False
    
    # Preguntar confirmación
    confirmar = messagebox.askyesno(
        "Confirmar Restore", 
        f"¿Restaurar BD 'BD_GrupoAlumno' completa?\n\n"
        f"Si la base de datos actualemente contiene datos se eliminaran\n"
        f"Collections encontradas: {len(archivos_bson)}\n\n"
        f"¿Continuar?"
    )
    
    if not confirmar:
        messagebox.showinfo("Cancelado", "Restore cancelado por el usuario")
        return False
    
    # Ejecutar mongorestore
    try:
        # Comando correctamente formado
        comando = [
            mongorestore_path,
            "--drop",
            "--db", "BD_GrupoAlumno",
            ruta_backup
        ]
        
        # Ejecutar sin shell=True cuando usas lista
        resultado = subprocess.run(
            comando, 
            capture_output=True, 
            text=True,
            encoding='utf-8'
        )
        
        if resultado.returncode == 0:
            messagebox.showinfo(
                "Éxito", 
                f"Restore completado exitosamente para 'BD_GrupoAlumno'\n\n"
                f"Collections restauradas: {len(archivos_bson)}\n"
            )
            print(f"Resultado: {resultado.stdout}")
            return True
        else:
            messagebox.showerror(
                "Error en Restore",
                f"Código de error: {resultado.returncode}\n\n"
                f"Mensaje:\n{resultado.stderr}"
            )
            print(f"ERROR: {resultado.stderr}")
            return False
        
    except subprocess.SubprocessError as e:
        messagebox.showerror(
            "Error", 
            f"Error al ejecutar mongorestore:\n{str(e)}"
        )
        print(f"Error: {e}")
        return False
    except Exception as e:
        messagebox.showerror(
            "Error Inesperado",
            f"Ocurrió un error inesperado:\n{str(e)}"
        )
        print(f"Error inesperado: {e}")
        return False