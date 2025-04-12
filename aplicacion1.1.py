import tkinter as tk
from tkinter import ttk
import mysql.connector
from ttkthemes import ThemedStyle
from tkinter import messagebox
import sys
import json
import hashlib
import subprocess
import os

def mostrar_mensaje(titulo, mensaje):
    ventana = tk.Tk()
    ventana.withdraw()
    messagebox.showerror(titulo, mensaje)
    ventana.destroy()


def verificar_conexion_bd():
    try:
        # Configurar los parámetros de conexión
        host = "localhost"
        user = "root"
        password = ""
        database = "bodega"

        # Intentar establecer la conexión
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Verificar si la conexión fue exitosa
        if conexion.is_connected():
            conexion.close()
            return True
        else:
            mostrar_mensaje("Error de conexión", "No se pudo establecer conexión con la base de datos.")
            return False

    except mysql.connector.Error as error:
        mostrar_mensaje("Error de conexión", "Error al conectar a la base de datos: " + str(error))
        return False


# Llamar a la función de verificación de conexión al inicio del código
if verificar_conexion_bd():
    # Continuar con el resto del código...
    print("Conexión exitosa. Continuando con el resto del código.")
else:
    # Salir del programa o realizar otras acciones si la conexión falla
    print("No se pudo conectar a la base de datos. El programa se cerrará.")
    sys.exit()


    

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, compatible con PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        # Si se ejecuta desde un ejecutable generado por PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Si se ejecuta desde el código fuente Python
        return os.path.join(os.path.abspath("."), relative_path)


ruta_datos_json = resource_path('recursos/datos.json')
ruta_crud = resource_path('recursos/crud.py')
ruta_grafico = resource_path('recursos/grafico.py')
ruta_logo = resource_path('recursos/logo.ico')
ruta_registro = resource_path('recursos/registro.py')
ruta_envio = resource_path('recursos/envio.py')


class LoginWindow:
    def __init__(self):
        # Crear ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Inicio de sesión")
        self.ventana.configure(bg="black")
        self.ventana.resizable(0, 0)
        self.ventana.overrideredirect(True)
        self.ventana.geometry("320x300")
        self.ventana.eval('tk::PlaceWindow . center')

        # Establecer tema personalizado
        style = ThemedStyle(self.ventana)
        style.set_theme("equilux")
        
        # Personalizar el estilo de los botones
        style = ttk.Style(self.ventana)
        # Establecer estilo para los botones
        style.configure('TButton', font=('Arial', 12), width=20, foreground='white', background='black')

        # Crear frame para los elementos
        self.frame = ttk.Frame(self.ventana)
        self.frame.pack(expand="True")

        # Crear etiquetas y campo desplegable
        usuario_label = tk.Label(self.frame, text="Usuario:", font=('Arial', 16), bg="#464646",fg="white")
        usuario_label.grid(row=0, column=0, sticky="e")

        self.usuario_var = tk.StringVar()
        usuario_options = self.get_usernames()  # Obtener nombres de usuario desde JSON
        self.usuario_dropdown = tk.OptionMenu(self.frame, self.usuario_var, *usuario_options)
        self.usuario_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.usuario_dropdown.configure(bg="#464646",foreground="white")

        contraseña_label = tk.Label(self.frame, text="Contraseña:", font=('Arial', 14), bg="#464646",fg="white")
        contraseña_label.grid(row=1, column=0, sticky="e")

        self.entry_contraseña = tk.Entry(self.frame, show="*", font=('Arial', 12), width=20)
        self.entry_contraseña.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.mensaje_label = tk.Label(self.frame, text="", font=('Arial', 12))
        self.mensaje_label.grid(row=2, columnspan=2, padx=10, pady=10)
        self.mensaje_label.configure(bg="#464646")

        # Botón de inicio de sesión
        boton_login = ttk.Button(self.frame, text="Iniciar sesión", command=self.login, style='TButton')
        boton_login.grid(row=3, columnspan=2, padx=10, pady=10)
        
        # Botón de cambiar contraseña
        boton_cambiar_contraseña = ttk.Button(self.frame, text="Cambiar contraseña", command=self.abrir_ventana_cambio, style='TButton')
        boton_cambiar_contraseña.grid(row=4, columnspan=2, padx=10, pady=10)

        #boton de cerrar
        boton_cerrar = ttk.Button(self.frame, text="Cerrar", command=self.cerrar_aplicacion, style='TButton')
        boton_cerrar.grid(row=5, columnspan=2, padx=10, pady=10)

    def cerrar_aplicacion(self):
        self.ventana.destroy()
            

        self.ventana.mainloop()

    def get_usernames(self):
        # Cargar nombres de usuario desde el archivo JSON
        with open(ruta_datos_json) as file:
            data = json.load(file)
        return list(data.keys())

    def login(self):
        username = self.usuario_var.get()
        password = self.entry_contraseña.get()

        # Cargar los datos del usuario desde el archivo JSON
        with open(ruta_datos_json) as file:
            data = json.load(file)

        # Verificar si el nombre de usuario existe y verificar la contraseña
        if username in data:
            stored_password = data[username]
            if self.verificar_contraseña(password, stored_password):
                self.mensaje_label.config(text="Credenciales correctas", foreground='green')
                self.ventana.withdraw()  # Ocultar la ventana de inicio de sesión
                self.ventana_principal = MainWindow(admin=(username == "Administrador"))
            else:
                self.mensaje_label.config(text="Credenciales incorrectas", foreground='red', background="#464646")
        else:
            self.mensaje_label.config(text="Usuario no encontrado", foreground='red', background="#464646")

    def verificar_contraseña(self, password, stored_password):
        # Hashear la contraseña ingresada y compararla con la contraseña almacenada
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password == stored_password
    def abrir_ventana_cambio(self):
        # Crear una nueva ventana para el cambio de contraseña
        ventana_cambio = tk.Toplevel(self.ventana)
        ventana_cambio.title("Cambiar contraseña")
        ventana_cambio.iconbitmap(ruta_logo)
        ventana_cambio.configure(bg="#464646")
        ventana_cambio.resizable(0, 0)

        # Crear etiquetas y campos de usuario, contraseña anterior y nueva
        usuario_label = tk.Label(ventana_cambio, text="Usuario:", font=('Arial', 14), bg="#464646",fg="white")
        usuario_label.grid(row=0, column=0, sticky="e")
        self.usuario_var_cambio = tk.StringVar()
        usuario_options = self.get_usernames()  # Obtener nombres de usuario desde JSON
        self.usuario_dropdown_cambio = tk.OptionMenu(ventana_cambio, self.usuario_var_cambio, *usuario_options)
        self.usuario_dropdown_cambio.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.usuario_dropdown_cambio.configure(bg="#464646",foreground="white")

        contraseña_anterior_label = tk.Label(ventana_cambio, text="Contraseña anterior:", font=('Arial', 14), bg="#464646",fg="white")
        contraseña_anterior_label.grid(row=1, column=0, sticky="e")

        self.entry_contraseña_anterior = tk.Entry(ventana_cambio, show="*", font=('Arial', 12), width=20)
        self.entry_contraseña_anterior.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        contraseña_nueva_label = tk.Label(ventana_cambio, text="Contraseña nueva:", font=('Arial', 14), bg="#464646",fg="white")
        contraseña_nueva_label.grid(row=2, column=0, sticky="e")

        self.entry_contraseña_nueva = tk.Entry(ventana_cambio, show="*", font=('Arial', 12), width=20)
        self.entry_contraseña_nueva.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.mensaje_cambio_label = tk.Label(ventana_cambio, text="", font=('Arial', 12),bg="#464646")
        self.mensaje_cambio_label.grid(row=3, columnspan=2, padx=10, pady=10)

        # Botón de confirmar cambio de contraseña
        boton_confirmar_cambio = ttk.Button(ventana_cambio, text="Confirmar cambio", command=lambda: self.confirmar_cambio(ventana_cambio), style='TButton')
        boton_confirmar_cambio.grid(row=4, columnspan=2, padx=10, pady=10)



    def confirmar_cambio(self, ventana_cambio):
        username = self.usuario_var_cambio.get()
        old_password = self.entry_contraseña_anterior.get()
        new_password = self.entry_contraseña_nueva.get()

        # Cargar los datos del usuario desde el archivo JSON
        with open(ruta_datos_json) as file:
            data = json.load(file)

        # Verificar si el nombre de usuario existe
        if username in data:
            stored_password = data[username]
            # Verificar si la contraseña anterior coincide
            if self.verificar_contraseña(old_password, stored_password):
                # Hashear la nueva contraseña
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

                # Actualizar la contraseña en el archivo JSON
                data[username] = hashed_password

                # Guardar los datos actualizados en el archivo JSON
                with open(ruta_datos_json, 'w') as file:
                    json.dump(data, file)
                ventana_cambio.destroy()
            else:
                # Mostrar mensaje de contraseña incorrecta
                self.mensaje_cambio_label.config(text="Contraseña incorrecta", fg='red',bg="#464646")
        else:
            # Mostrar mensaje de usuario no encontrado
            self.mensaje_cambio_label.config(text="Usuario no encontrado", fg='red',bg="#464646")

    def cerrar_aplicacion(self):
        self.ventana.destroy()


class MainWindow:
    def __init__(self, admin=False):
        self.admin = admin
        # Conexión a la base de datos
        self.conn = mysql.connector.connect(host='localhost', user='root', password='', db='bodega')
        self.cursor = self.conn.cursor()

        # Crear ventana principal
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("Bodega")  # cambiar titulo a "Bodega"
        self.ventana_principal.iconbitmap(ruta_logo)  # establecer icono
        # self.ventana_principal.geometry("1500x700")  # Tamaño personalizado para la ventana principal
        self.ventana_principal.geometry(f"{self.ventana_principal.winfo_screenwidth()}x{self.ventana_principal.winfo_screenheight()}")  # Ajustar tamaño de la ventana principal al tamaño de la pantalla
        self.ventana_principal.attributes('-fullscreen', True)
        self.ventana_principal.configure(bg="#464646")

        # Configurar estilo de los botones
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 16))  # Cambiar el tamaño de fuente a 16

        # Crear lista de botones
        self.crear_botones()

        #----------------------------------------------- menu de productos
        # Crear marco para el menú de botones
        self.frame_botones = tk.Frame(self.ventana_principal, width=100, bg="gray")
        self.frame_botones.pack(side=tk.TOP, fill=tk.X)

        # Crear canvas para el marco de productos
        canvas = tk.Canvas(self.ventana_principal, bg="#464646")
        canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Crear scrollbar vertical
        scrollbar = ttk.Scrollbar(self.ventana_principal, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.LEFT,fill=tk.Y)

        # Configurar el canvas para usar el scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Crear botón para realizar la búsqueda
        boton_buscar = tk.Button(self.frame_botones, text="Buscar", command=self.buscar_producto, width=20,font=("Helvetica", 15))
        boton_buscar.pack(pady=5,padx=20,side="left")

        # Crear campo de entrada para el buscador
        self.buscador_entry = tk.Entry(self.frame_botones,font=("Helvetica", 15))
        self.buscador_entry.pack(pady=5,padx=20,side="left")

        boton_restablecer = tk.Button(self.frame_botones, text="Restablecer", command=self.restablecer_menu, width=20,font=("Helvetica", 15))
        boton_restablecer.pack(pady=5,padx=20,side="left")

        # Crear marco para mostrar los productos dentro del canvas

        self.frame_productos = tk.Frame(canvas, bg="#5e5e5e",padx=70, pady=20,width=100)
        

        canvas.create_window((0, 0), window=self.frame_productos,width=1640)
        

        # Obtener los productos desde la base de datos con su stock total
        query = "SELECT p.Id_Producto, p.Nombre_Producto, p.Marca_Producto, p.Detalles_Producto, p.Precio_Producto, s.Cantidad_Total " \
                "FROM producto p " \
                "JOIN stock_total s ON p.Id_Producto = s.Id_Producto " \
                "WHERE p.Id_Producto <> 7"
        self.cursor.execute(query)
        productos = self.cursor.fetchall()

        # Mostrar los productos en el marco
        for producto in productos:
            id_producto = producto[0]
            nombre = producto[1]
            marca = producto[2]
            detalles = producto[3]
            precio = producto[4]
            stock_total = producto[5]

            frame_producto = tk.Frame(self.frame_productos, bd=1, relief=tk.SOLID)
            frame_producto.pack(padx=5, pady=5, fill=tk.X)

            label_id = tk.Label(frame_producto, text=f"ID: {id_producto}",font=("Helvetica", 15))
            label_id.pack(anchor=tk.NW)

            label_nombre = tk.Label(frame_producto, text=f"Nombre: {nombre}",font=("Helvetica", 15))
            label_nombre.pack(anchor=tk.NW)

            label_marca = tk.Label(frame_producto, text=f"Marca: {marca}",font=("Helvetica", 15))
            label_marca.pack(anchor=tk.NW)

            label_detalles = tk.Label(frame_producto, text=f"{detalles}",font=("Helvetica", 15))
            label_detalles.pack()

            label_precio = tk.Label(frame_producto, text=f"Precio: {precio}",font=("Helvetica", 15))
            label_precio.pack(anchor=tk.SE)

            label_stock_total = tk.Label(frame_producto, text=f"Stock Total: {stock_total}",font=("Helvetica", 15))
            label_stock_total.pack(anchor=tk.SE)
        self.conn.close()
        #----------------------------------------------- menu de productos

        self.ventana_principal.mainloop()

    def crear_botones(self):
        # Frame para los botones
        self.frame_botones = tk.Frame(self.ventana_principal,padx=20, pady=20)
        self.frame_botones.pack(side=tk.LEFT,anchor=tk.NW, padx=10, pady=10, fill=tk.BOTH) 
        self.frame_botones.configure(bg="#575757")

        if self.admin:
            # Botones para el administrador

            boton_admin3 = tk.Button(self.frame_botones, text="registro", command=self.acceder_registro, width=20,font=("Helvetica", 15))
            boton_admin3.pack(pady=20)

            boton_admin5 = tk.Button(self.frame_botones, text="envio", command=self.ver_envio, width=20,font=("Helvetica", 15))
            boton_admin5.pack(pady=20)

            boton_admin4 = tk.Button(self.frame_botones, text="grafico", command=self.ver_grafico, width=20,font=("Helvetica", 15))
            boton_admin4.pack(pady=20)

        else:
            pass

        boton_admin1 = tk.Button(self.frame_botones, text="modificacion de datos", command=self.crud, width=20,font=("Helvetica", 15))
        boton_admin1.pack(pady=20)

        # Botón de cerrar
        boton_cerrar = tk.Button(self.frame_botones, text="Cerrar",command=self.cerrar_aplicacion, width=20,font=("Helvetica", 15))
        boton_cerrar.pack(pady=20)

    def buscar_producto(self):
        # Obtener el texto ingresado en el campo de búsqueda
        texto_busqueda = self.buscador_entry.get()

        # Limpiar el marco de productos antes de realizar la búsqueda
        for widget in self.frame_productos.winfo_children():
            widget.destroy()

        # Realizar la búsqueda en la base de datos usando el texto ingresado

        self.conn = mysql.connector.connect(host='localhost', user='root', password='', db='bodega')
        self.cursor = self.conn.cursor()

        query = "SELECT p.Id_Producto, p.Nombre_Producto, p.Marca_Producto, p.Detalles_Producto, p.Precio_Producto, s.Cantidad_Total " \
                "FROM producto p " \
                "JOIN stock_total s ON p.Id_Producto = s.Id_Producto " \
                "WHERE p.Nombre_Producto LIKE '%{}%'".format(texto_busqueda)
        self.cursor.execute(query)
        productos = self.cursor.fetchall()

        # Mostrar los productos encontrados en el marco
        for producto in productos:
            id_producto = producto[0]
            nombre = producto[1]
            marca = producto[2]
            detalles = producto[3]
            precio = producto[4]
            stock_total = producto[5]

            frame_producto = tk.Frame(self.frame_productos, bd=1, relief=tk.SOLID)
            frame_producto.pack(padx=5, pady=5, fill=tk.X)

            label_id = tk.Label(frame_producto, text=f"ID: {id_producto}",font=("Helvetica", 15))
            label_id.pack(anchor=tk.NW)

            label_nombre = tk.Label(frame_producto, text=f"Nombre: {nombre}",font=("Helvetica", 15))
            label_nombre.pack(anchor=tk.NW)

            label_marca = tk.Label(frame_producto, text=f"Marca: {marca}",font=("Helvetica", 15))
            label_marca.pack(anchor=tk.NW)

            label_detalles = tk.Label(frame_producto, text=f"{detalles}",font=("Helvetica", 15))
            label_detalles.pack()

            label_precio = tk.Label(frame_producto, text=f"Precio: {precio}",font=("Helvetica", 15))
            label_precio.pack(anchor=tk.SE)

            label_stock_total = tk.Label(frame_producto, text=f"Stock Total: {stock_total}",font=("Helvetica", 15))
            label_stock_total.pack(anchor=tk.SE)
        self.conn.close()
    
    
    #funciones a realizar<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def ver_envio(self):
        subprocess.run(["python",ruta_envio])
    def crud(self):
        subprocess.run(["python",ruta_crud])
    def acceder_registro(self):
        subprocess.run(["python",ruta_registro])
    def ver_grafico(self):
        subprocess.run(["python", ruta_grafico])
    def restablecer_menu(self):
        # Limpiar el campo de búsqueda
        self.buscador_entry.delete(0, tk.END)

        # Limpiar el marco de productos
        for widget in self.frame_productos.winfo_children():
            widget.destroy()

        # Volver a mostrar todos los productos en el marco

        self.conn = mysql.connector.connect(host='localhost', user='root', password='', db='bodega')
        self.cursor = self.conn.cursor()

        query = "SELECT p.Id_Producto, p.Nombre_Producto, p.Marca_Producto, p.Detalles_Producto, p.Precio_Producto, s.Cantidad_Total " \
                "FROM producto p " \
                "JOIN stock_total s ON p.Id_Producto = s.Id_Producto"
        self.cursor.execute(query)
        productos = self.cursor.fetchall()

        for producto in productos:
            id_producto = producto[0]
            nombre = producto[1]
            marca = producto[2]
            detalles = producto[3]
            precio = producto[4]
            stock_total = producto[5]

            frame_producto = tk.Frame(self.frame_productos, bd=1, relief=tk.SOLID)
            frame_producto.pack(padx=5, pady=5, fill=tk.X)

            label_id = tk.Label(frame_producto, text=f"ID: {id_producto}",font=("Helvetica", 15))
            label_id.pack(anchor=tk.NW)

            label_nombre = tk.Label(frame_producto, text=f"Nombre: {nombre}",font=("Helvetica", 15))
            label_nombre.pack(anchor=tk.NW)

            label_marca = tk.Label(frame_producto, text=f"Marca: {marca}",font=("Helvetica", 15))
            label_marca.pack(anchor=tk.NW)

            label_detalles = tk.Label(frame_producto, text=f"{detalles}",font=("Helvetica", 15))
            label_detalles.pack()

            label_precio = tk.Label(frame_producto, text=f"Precio: {precio}",font=("Helvetica", 15))
            label_precio.pack(anchor=tk.SE)

            label_stock_total = tk.Label(frame_producto, text=f"Stock Total: {stock_total}",font=("Helvetica", 15))
            label_stock_total.pack(anchor=tk.SE)
        self.conn.close()
    #funciones a realizar<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def cerrar_aplicacion(self):
        self.ventana_principal.destroy()
        sys.exit(0)

def cerrar_ventana_principal():
    if hasattr(app, 'ventana_principal'):
        app.cerrar_aplicacion()
        


app = LoginWindow()
app.ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana_principal)  # Asignar el método de cierre a la ventana principal
app.ventana.mainloop()