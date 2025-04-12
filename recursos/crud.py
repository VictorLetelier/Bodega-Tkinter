import tkinter as tk
import mysql.connector
from datetime import date

# Conexión a la base de datos
db = mysql.connector.connect(
host='localhost', user='root', password='', db='bodega'
)

# Variables globales
id_selector = None
nombre_entry = None
marca_entry = None
precio_entry = None
detalles_entry=None
stock_entry = None
nuevo_id_entry = None
nuevo_nombre_entry = None
nueva_marca_entry = None
nuevo_precio_entry = None
nuevo_stock_entry = None
eliminar_id_selector = None
nuevo_detalles_entry= None
id_empleado_entry = None

def obtener_ultimo_id():
    
    cursor=db.cursor()
    consulta = "SELECT MAX(Id_Registro) FROM registro"
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    ultimo_id = resultado[0] if resultado[0] else 0
    return ultimo_id + 1


# Función para cargar la información de un producto seleccionado
def cargar_producto():
    id_producto = id_selector.get()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM producto WHERE Id_Producto = %s", (id_producto,))
    producto = cursor.fetchone()
    if producto:
        nombre_entry.delete(0, tk.END)
        nombre_entry.insert(tk.END, producto[1])
        marca_entry.delete(0, tk.END)
        marca_entry.insert(tk.END, producto[2])
        detalles_entry.delete(0, tk.END)
        detalles_entry.insert(tk.END, producto[3])
        precio_entry.delete(0, tk.END)
        precio_entry.insert(tk.END, producto[4])
        stock_entry.delete(0, tk.END)
        stock_entry.insert(tk.END, obtener_stock(id_producto))
        # Continuar con los demás campos

# Función para actualizar un producto
def actualizar_producto():
    id_empleado = id_empleado_entry.get()
    if not id_empleado:
        return  # Si el campo está vacío, salimos de la función sin hacer nada
    
    fecha_actual = date.today().strftime('%Y-%m-%d')
    id_registro = obtener_ultimo_id()
    id_producto = id_selector.get()
    nuevo_nombre = nombre_entry.get()
    nueva_marca = marca_entry.get()
    nuevo_precio = precio_entry.get()
    nuevos_detalles = detalles_entry.get()
    nuevo_stock = stock_entry.get()
    # Obtener los valores de los demás campos
    registro_eventos = f"se modifico nombre: {nuevo_nombre}, marca: {nueva_marca}, detalles: {nuevos_detalles}, precio: {nuevo_precio}, id producto:{id_producto}"
    cursor = db.cursor()
    cursor.execute("UPDATE producto SET Nombre_Producto = %s, Marca_Producto = %s, Detalles_Producto = %s, Precio_Producto = %s WHERE Id_Producto = %s", (nuevo_nombre, nueva_marca, nuevos_detalles, nuevo_precio, id_producto))
    db.commit()

    consulta = "INSERT INTO registro (Id_Registro, Fecha_Registro, Registro_Eventos, Id_Empleado, Id_Producto) VALUES (%s, %s, %s, %s, %s)"
    valores = (id_registro, fecha_actual, registro_eventos, id_empleado, 7)
    cursor.execute(consulta, valores)
    
    db.commit()
    actualizar_stock(id_producto, nuevo_stock)
    

# Función para eliminar un producto
def eliminar_producto():
    id_empleado = id_empleado_entry.get()
    if not id_empleado:
        return  # Si el campo está vacío, salimos de la función sin hacer nada
    
    id_producto = id_selector.get()
    fecha_actual = date.today().strftime('%Y-%m-%d')
    id_registro = obtener_ultimo_id()
    nuevo_nombre = nombre_entry.get()
    nueva_marca = marca_entry.get()
    nuevo_precio = precio_entry.get()
    nuevos_detalles = detalles_entry.get()
    nuevo_stock = stock_entry.get()

    registro_eventos = f"se eliminó: {nuevo_nombre}, marca: {nueva_marca}, detalles: {nuevos_detalles}, precio: {nuevo_precio}, id producto:{id_producto}, nuevo stock: {nuevo_stock}"

    # Obtener la fecha actual
    fecha_actual = date.today().strftime('%Y-%m-%d')

    # Obtener el nuevo ID de registro
    id_registro = obtener_ultimo_id()

    # nombre_producto = nuevo_nombre_entry.get()
    # Eliminar registros relacionados en la tabla stock_total
    cursor = db.cursor()
    cursor.execute("DELETE FROM stock_total WHERE Id_Producto = %s", (id_producto,))
    db.commit()

    # Eliminar el producto en la tabla producto
    cursor.execute("DELETE FROM producto WHERE Id_Producto = %s", (id_producto,))
    db.commit()

    consulta = "INSERT INTO registro (Id_Registro, Fecha_Registro, Registro_Eventos, Id_Empleado, Id_Producto) VALUES (%s, %s, %s, %s, %s)"
    valores = (id_registro, fecha_actual, registro_eventos, id_empleado, 7)  # 0 si no tienes el ID de producto específico
    cursor.execute(consulta, valores)

    #messagebox.showinfo("Eliminar Producto", "El producto ha sido eliminado con éxito.")


# Funciones para operaciones relacionadas con la tabla "stock_total"
def obtener_stock(id_producto):
    cursor = db.cursor()
    cursor.execute("SELECT Cantidad_Total FROM stock_total WHERE Id_Producto = %s", (id_producto,))
    stock = cursor.fetchone()
    if stock:
        return stock[0]
    else:
        return 0

def actualizar_stock(id_producto, nuevo_stock):
    cursor = db.cursor()
    cursor.execute("UPDATE stock_total SET Cantidad_Total = %s WHERE Id_Producto = %s", (nuevo_stock, id_producto))
    db.commit()

def insertar_stock(id_producto, nuevo_stock):
    cursor = db.cursor()
    cursor.execute("INSERT INTO stock_total (Id_Producto, Cantidad_Total) VALUES (%s, %s)", (id_producto, nuevo_stock))
    db.commit()

def eliminar_stock(id_producto):
    cursor = db.cursor()
    cursor.execute("DELETE FROM stock_total WHERE Id_Producto = %s", (id_producto,))
    db.commit()

# Función para abrir la ventana de carga
def abrir_ventana_carga():
    ventana_carga = tk.Toplevel(ventana_principal)
    ventana_carga.title("Cargar Producto")
    ventana_carga.resizable(0, 0)
    ventana_carga.configure(bg="dark gray")

    global id_selector
    id_selector_label = tk.Label(ventana_carga, text="Seleccione un ID:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    id_selector_label.pack()
    id_selector = tk.Entry(ventana_carga, width=20, font=("Helvetica",15),bg="gray",fg="white")
    id_selector.pack()

    cargar_button = tk.Button(ventana_carga, text="Actualizar", command=cargar_producto, width=20, font=("Helvetica",15),bg="light gray",fg="black")
    cargar_button.pack()

    global id_empleado_entry
    id_empleado_label = tk.Label(ventana_carga, text="ID Empleado:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    id_empleado_label.pack()
    id_empleado_entry = tk.Entry(ventana_carga, width=20, font=("Helvetica",15),bg="gray",fg="white")
    id_empleado_entry.pack()

    global nombre_entry
    nombre_label = tk.Label(ventana_carga, text="Nombre:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    nombre_label.pack()
    nombre_entry = tk.Entry(ventana_carga, width=20, font=("Helvetica",15),bg="gray",fg="white")
    nombre_entry.pack()

    global marca_entry
    marca_label = tk.Label(ventana_carga, text="Marca:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    marca_label.pack()
    marca_entry = tk.Entry(ventana_carga, width=20, font=("Helvetica",15),bg="gray",fg="white")
    marca_entry.pack()

    global precio_entry
    precio_label = tk.Label(ventana_carga, text="Precio:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    precio_label.pack()
    precio_entry = tk.Entry(ventana_carga, width=20, font=("Helvetica",15),bg="gray",fg="white")
    precio_entry.pack()

    global detalles_entry
    detalles_label = tk.Label(ventana_carga, text="Detalles:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    detalles_label.pack()
    detalles_entry = tk.Entry(ventana_carga, width=20, font=("Helvetica",15),bg="gray",fg="white")
    detalles_entry.pack()

    global stock_entry
    stock_label = tk.Label(ventana_carga, text="Stock:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    stock_label.pack()
    stock_entry = tk.Entry(ventana_carga, width=20, font=("Helvetica",15),bg="gray",fg="white")
    stock_entry.pack()

    actualizar_button = tk.Button(ventana_carga, text="Actualizar", command=lambda: [actualizar_producto(),ventana_carga.destroy()], width=20, font=("Helvetica",15),bg="light gray",fg="black")
    actualizar_button.pack()

# Función para abrir la ventana de agregar
def abrir_ventana_agregar():
    ventana_agregar = tk.Toplevel(ventana_principal)
    ventana_agregar.title("Agregar Producto")
    ventana_agregar.resizable(0, 0)
    ventana_agregar.configure(bg="dark gray")

    # Obtener el último ID insertado en la base de datos
    cursor = db.cursor()
    cursor.execute("SELECT MAX(Id_Producto) FROM producto")
    last_id = cursor.fetchone()[0]

    # Incrementar el último ID en 1 para el nuevo producto
    nuevo_id = last_id + 1

    # Crear y configurar la etiqueta y el campo de entrada para el ID
    nuevo_id_label = tk.Label(ventana_agregar, text="ID:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    nuevo_id_label.pack()

    global nuevo_id_entry
    nuevo_id_entry = tk.Entry(ventana_agregar)
    nuevo_id_entry.insert(0, nuevo_id)  # Insertar el nuevo ID en el campo de entrada
    nuevo_id_entry.pack()
    nuevo_id_entry.configure(state='readonly', width=20, font=("Helvetica",15),bg="gray",fg="black")  # Hacer el campo de entrada de solo lectura

    global nuevo_nombre_entry
    nuevo_nombre_label = tk.Label(ventana_agregar, text="Nombre:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    nuevo_nombre_label.pack()
    nuevo_nombre_entry = tk.Entry(ventana_agregar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    nuevo_nombre_entry.pack()

    global nueva_marca_entry
    nueva_marca_label = tk.Label(ventana_agregar, text="Marca:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    nueva_marca_label.pack()
    nueva_marca_entry = tk.Entry(ventana_agregar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    nueva_marca_entry.pack()

    global nuevo_precio_entry
    nuevo_precio_label = tk.Label(ventana_agregar, text="Precio:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    nuevo_precio_label.pack()
    nuevo_precio_entry = tk.Entry(ventana_agregar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    nuevo_precio_entry.pack()

    global nuevo_detalles_entry
    nuevo_detalles_label = tk.Label(ventana_agregar, text="Detalles:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    nuevo_detalles_label.pack()
    nuevo_detalles_entry = tk.Entry(ventana_agregar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    nuevo_detalles_entry.pack()

    global nuevo_stock_entry
    nuevo_stock_label = tk.Label(ventana_agregar, text="Stock:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    nuevo_stock_label.pack()
    nuevo_stock_entry = tk.Entry(ventana_agregar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    nuevo_stock_entry.pack()

    global id_empleado_entry
    id_empleado_label = tk.Label(ventana_agregar, text="ID Empleado:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    id_empleado_label.pack()
    id_empleado_entry = tk.Entry(ventana_agregar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    id_empleado_entry.pack()

    # Función para agregar un nuevo producto
    def agregar_producto():
        cursor = db.cursor()

        id_empleado = id_empleado_entry.get()
        if not id_empleado:
            return
        nuevo_id = nuevo_id_entry.get()
        nuevo_nombre = nuevo_nombre_entry.get()
        nueva_marca = nueva_marca_entry.get()
        nuevo_precio = nuevo_precio_entry.get()
        nuevos_detalles = nuevo_detalles_entry.get()
        nuevo_stock = nuevo_stock_entry.get()

        # Obtener los valores de los demás campos

        registro_eventos = f"se agrego un nuevo producto: {nuevo_nombre}, marca: {nueva_marca}, detalles: {nuevos_detalles}, precio: {nuevo_precio}, id producto:{nuevo_id}, nuevo stock, {nuevo_stock}"
        fecha_actual = date.today().strftime('%Y-%m-%d')
        id_registro = obtener_ultimo_id()


        # Insertar el nuevo producto en la base de datos
        cursor.execute("INSERT INTO producto (Id_Producto, Nombre_Producto, Marca_Producto, Detalles_Producto, Precio_Producto) VALUES (%s, %s, %s, %s, %s)", (nuevo_id, nuevo_nombre, nueva_marca, nuevos_detalles, nuevo_precio))
        db.commit()
        consulta = "INSERT INTO registro (Id_Registro, Fecha_Registro, Registro_Eventos, Id_Empleado, Id_Producto) VALUES (%s, %s, %s, %s, %s)"
        valores = (id_registro, fecha_actual, registro_eventos, id_empleado, 7)  # 0 si no tienes el ID de producto específico aún
        cursor.execute(consulta, valores)
        
        db.commit()
        # db.commit()
        insertar_stock(nuevo_id_entry.get(), nuevo_stock)

        # Limpiar los campos de entrada
        nuevo_id_entry.delete(0, tk.END)
        nuevo_nombre_entry.delete(0, tk.END)
        nueva_marca_entry.delete(0, tk.END)
        nuevo_precio_entry.delete(0, tk.END)
        nuevo_detalles_entry.delete(0,tk.END)
        nuevo_stock_entry.delete(0, tk.END)

        # Actualizar el campo ID con el nuevo valor
        nuevo_id = int(nuevo_id_entry.get()) + 1
        nuevo_id_entry.delete(0, tk.END)
        nuevo_id_entry.insert(0, nuevo_id)

    agregar_button = tk.Button(ventana_agregar, text="Agregar", command=lambda: [agregar_producto(),ventana_agregar.destroy()], width=20, font=("Helvetica",15),bg="light gray",fg="black")
    agregar_button.pack()





# Función para abrir la ventana de eliminar
def abrir_ventana_eliminar():
    ventana_eliminar = tk.Toplevel(ventana_principal)
    ventana_eliminar.title("Eliminar Producto")
    ventana_eliminar.configure(bg="light gray")
    ventana_eliminar.resizable(0, 0)

    global id_selector
    id_selector_label = tk.Label(ventana_eliminar, text="Seleccione un ID:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    id_selector_label.pack()
    id_selector = tk.Entry(ventana_eliminar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    id_selector.pack()

    cargar_button = tk.Button(ventana_eliminar, text="Actualizar", command=cargar_producto, width=20, font=("Helvetica",15),bg="light gray",fg="black")
    cargar_button.pack()

    global id_empleado_entry
    id_empleado_label = tk.Label(ventana_eliminar, text="ID Empleado:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    id_empleado_label.pack()
    id_empleado_entry = tk.Entry(ventana_eliminar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    id_empleado_entry.pack()

    global nombre_entry
    nombre_label = tk.Label(ventana_eliminar, text="Nombre:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    nombre_label.pack()
    nombre_entry = tk.Entry(ventana_eliminar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    nombre_entry.pack()

    global marca_entry
    marca_label = tk.Label(ventana_eliminar, text="Marca:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    marca_label.pack()
    marca_entry = tk.Entry(ventana_eliminar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    marca_entry.pack()

    global precio_entry
    precio_label = tk.Label(ventana_eliminar, text="Precio:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    precio_label.pack()
    precio_entry = tk.Entry(ventana_eliminar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    precio_entry.pack()

    global detalles_entry
    detalles_label = tk.Label(ventana_eliminar, text="Detalles:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    detalles_label.pack()
    detalles_entry = tk.Entry(ventana_eliminar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    detalles_entry.pack()

    global stock_entry
    stock_label = tk.Label(ventana_eliminar, text="Stock:", width=20, font=("Helvetica",15),bg="gray",fg="white")
    stock_label.pack()
    stock_entry = tk.Entry(ventana_eliminar, width=20, font=("Helvetica",15),bg="gray",fg="white")
    stock_entry.pack()


    eliminar_button = tk.Button(ventana_eliminar, text="Eliminar", command= lambda:[eliminar_producto(),ventana_eliminar.destroy()], width=20, font=("Helvetica",15),bg="light gray",fg="black")
    eliminar_button.pack()

def cerrar_todas_las_pestanas():
    # Obtener todas las ventanas secundarias abiertas
    ventanas_secundarias = ventana_principal.winfo_children()

    # Cerrar todas las ventanas secundarias
    for ventana in ventanas_secundarias:
        if isinstance(ventana, tk.Toplevel):
            ventana.destroy()

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.eval('tk::PlaceWindow . center')
ventana_principal.geometry("350x310")
ventana_principal.title("Modificacion de datos")
ventana_principal.configure(bg="dark gray")
ventana_principal.resizable(0, 0)

# Botones principales
cargar_button = tk.Button(ventana_principal, text="Cargar Producto", command=abrir_ventana_carga, width=20, font=("Helvetica",20),bg="gray",fg="white")
cargar_button.pack(padx=5,pady=10)

agregar_button = tk.Button(ventana_principal, text="Agregar Producto", command=abrir_ventana_agregar, width=20, font=("Helvetica",20),bg="gray",fg="white")
agregar_button.pack(padx=5,pady=10)

eliminar_button = tk.Button(ventana_principal, text="Eliminar Producto", command=abrir_ventana_eliminar, width=20, font=("Helvetica",20),bg="gray",fg="white")
eliminar_button.pack(padx=5,pady=10)

boton_cerrar_pestanas = tk.Button(ventana_principal, text="Cerrar", command=lambda:[cerrar_todas_las_pestanas(),ventana_principal.destroy()], width=20, font=("Helvetica",20),bg="gray",fg="white")
boton_cerrar_pestanas.pack(padx=5,pady=10)

# Iniciar el bucle principal de la ventana
ventana_principal.mainloop()
