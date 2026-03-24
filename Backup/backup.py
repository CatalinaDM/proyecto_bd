import subprocess
import os
from datetime import datetime
from tkinter import filedialog, messagebox

# Configuración de rutas (Ajusta la ruta a donde tengas instalado MongoDB Tools)
RUTA_MONGODUMP = r"C:\Program Files\MongoDB\Tools\100\bin\mongodump.exe"
NOMBRE_BD = "BD_GrupoAlumno"

def realizar_backup():
    """Genera un respaldo nativo .bson usando mongodump."""
    try:
        # 1. Pedir al usuario que seleccione una CARPETA de destino
        # mongodump crea una estructura de carpetas, por lo que pedimos directorio
        directorio_destino = filedialog.askdirectory(
            title="Seleccionar carpeta para guardar el Backup nativo"
        )

        if not directorio_destino:
            return

        # 2. Preparar el nombre de la subcarpeta con la fecha
        fecha_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ruta_final_backup = os.path.join(directorio_destino, f"backup_{NOMBRE_BD}_{fecha_str}")

        # 3. Construir el comando para mongodump
        # --db: nombre de la base de datos
        # --out: carpeta de salida
        comando = [
            RUTA_MONGODUMP,
            f"--db={NOMBRE_BD}",
            f"--out={ruta_final_backup}"
        ]

        # 4. Ejecutar el comando
        # check=True lanzará una excepción si el comando falla
        # creationflags=subprocess.CREATE_NO_WINDOW evita que se abra una ventana negra de CMD
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True, creationflags=0x08000000)

        messagebox.showinfo("Éxito", f"Backup nativo (.bson) creado correctamente en:\n{ruta_final_backup}")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error de mongodump", f"No se pudo completar el respaldo nativo.\nVerifica que la ruta de las Tools sea correcta.\n\nError: {e.stderr}")
    except Exception as e:
        messagebox.showerror("Error de Backup", f"Ocurrió un error inesperado: {e}")