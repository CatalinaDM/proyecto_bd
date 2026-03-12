import tkinter as tk
from tkinter import messagebox
from Grupo.eliminar_grupo import eliminar_grupo, eliminar_todos_grupos


def eliminar():
    clave = entry_clave.get()
    eliminar_grupo(clave)
    messagebox.showinfo("Eliminar", "Grupo eliminado correctamente")


def eliminar_todos():
    confirmar = messagebox.askyesno(
        "Confirmación",
        "¿Estás seguro de eliminar TODOS los grupos?"
    )

    if confirmar:
        eliminar_todos_grupos()
        messagebox.showinfo("Eliminar", "Todos los grupos fueron eliminados")


ventana = tk.Tk()
ventana.title("Eliminar Grupo")
ventana.geometry("300x200")

tk.Label(ventana, text="Clave del Grupo").pack()

entry_clave = tk.Entry(ventana)
entry_clave.pack()

tk.Button(ventana, text="Eliminar grupo", command=eliminar).pack(pady=10)

tk.Button(ventana, text="Eliminar TODOS", command=eliminar_todos).pack()

ventana.mainloop()