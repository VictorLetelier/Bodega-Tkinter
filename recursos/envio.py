import tkinter as tk
from tkinter import ttk
import mysql.connector

# Configura la conexión a la base de datos
conexion = mysql.connector.connect(
    host='localhost', user='root', password='', db='bodega'
)

# Crea una instancia de Tkinter
ventana = tk.Tk()
ventana.title("Registros")
ventana.geometry("400x300")
ventana.resizable(0, 0)
ventana.configure(width=20, bg="#5e5e5e")
ventana.eval('tk::PlaceWindow . center')

# Crea un frame para contener los labels
frame = tk.Frame(ventana, width=20, bg="#5e5e5e")
frame.pack(pady=20)

# Crea un scrollbar
scrollbar = ttk.Scrollbar(frame, orient="vertical")

# Crea un canvas dentro del frame
canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)

# Configura el scrollbar para que controle el canvas
scrollbar.config(command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Crea otro frame dentro del canvas para contener los labels
inner_frame = tk.Frame(canvas, bg="#5e5e5e")

# Asocia el inner_frame al canvas
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Función para cargar los registros desde la base de datos y mostrarlos en los labels
def cargar_registros():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM envio")
    registros = cursor.fetchall()

    for i, registro in enumerate(registros):
        id_envio = registro[0]
        fecha_envio = registro[1]
        fecha_entrega = registro[2]
        id_proveedor = registro[3]

        # Crea un label para mostrar los datos del registro
        label = tk.Label(
            inner_frame,
            text=f"ID Envio: {id_envio}\nFecha Envio: {fecha_envio}\nFecha Entrega: {fecha_entrega}\nID Proveedor: {id_proveedor}",
            font=("Arial", 12),
            anchor="w",
            justify="left",
            wraplength=350,
            width=50,
            bg="#464646",
            fg="white"
        )
        label.pack(padx=5, pady=10, anchor="w")
    conexion.close()

    # Actualiza la configuración del canvas cuando se agregan los labels
    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Llama a la función para cargar los registros
cargar_registros()

# Configura el desplazamiento de la rueda del ratón
def desplazar(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", desplazar)

# Ejecuta el bucle principal de Tkinter
ventana.mainloop()
