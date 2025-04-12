import matplotlib.pyplot as plt
import mysql.connector
from tkinter import Tk, Frame, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def conex():
    myconn = None
    try:
        myconn = mysql.connector.connect(host="localhost", user="root", password="", database="bodega")
        return myconn
    except mysql.connector.Error as error:
        if myconn:
            myconn.rollback()
        print("Error al establecer la conexión a la base de datos: {}".format(error))
        raise


def Grafica(connection, año, mes, consola):

    if mes == "Sin Especificar":

        if consola == "Sin Especificar":
            cur = connection.cursor()
            cur.execute("""
            select Sum(Cantidad_Enviada), Monthname(Fecha_Envio)
            from envio join stock_enviado using (Id_Envio) 
            where YEAR(Fecha_Envio) = """ + str(año) + """
            group by Monthname(Fecha_Envio) 
            order by Fecha_Envio;""")
            result = cur.fetchall()
            
        else:
            cur = connection.cursor()
            cur.execute("""
            select Sum(Cantidad_Enviada), Monthname(Fecha_Envio), Nombre_Producto
            from envio join stock_enviado using (Id_Envio) 
            join stock_total using (Id_Stock_Total)
            join producto using (Id_Producto)
            where YEAR(Fecha_Envio) = """ + str(año) + """
            AND Nombre_Producto = '""" + str(consola) + """'
            group by Monthname(Fecha_Envio)
            order by Fecha_Envio;""")
            result = cur.fetchall()

    else:
        if consola == 'Sin Especificar':
            cur = connection.cursor()
            cur.execute("""
            select Cantidad_Enviada, Day(Fecha_Envio), Nombre_Producto
            from envio join stock_enviado using (Id_Envio) 
            join stock_total using (Id_Stock_Total)
            join producto using (Id_Producto)
            where YEAR(Fecha_Envio) = """ + str(año) + """
            AND Monthname(Fecha_Envio) = '""" + str(mes) + """'
            group by Day(Fecha_Envio)
            order by Fecha_Envio;""")
            result = cur.fetchall()
            
        else:
            cur = connection.cursor()
            cur.execute("""
            select Sum(Cantidad_Enviada), Day(Fecha_Envio), Nombre_Producto
            from envio join stock_enviado using (Id_Envio) 
            join stock_total using (Id_Stock_Total)
            join producto using (Id_Producto)
            where YEAR(Fecha_Envio) = """ + str(año) + """
            AND Monthname(Fecha_Envio) = '""" + str(mes) + """'
            AND Nombre_Producto = '""" + str(consola) + """'
            group by Day(Fecha_Envio)
            order by Fecha_Envio;""")
            result = cur.fetchall()
    
    connection.close()
    return result

root = Tk()
root.geometry("990x500")
root.wm_title('Stock Enviado')
root.minsize(width=950, height=325)
frame = Frame(root)
frame.grid(column=0, row=0, sticky='nsew')

listaaño = ["2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"]

listames = ["Sin Especificar", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre",
            "Octubre", "Noviembre", "Diciembre"]

listaconsola = ["Sin Especificar", "PlayStation 5", "PlayStation 4", "Nintendo Switch",
                "Nintendo Switch OLED", "Xbox Series X", "Xbox Series S"]

Añolabel = ttk.Label(frame, text='Año:')
Añolabel.grid(column=0, row=1, padx=5, pady=5)

Meslabel = ttk.Label(frame, text='Mes:')
Meslabel.grid(column=1, row=1, padx=5, pady=5)

Consolalabel = ttk.Label(frame, text='Consola:')
Consolalabel.grid(column=2, row=1, padx=5, pady=5)

Año = ttk.Combobox(frame, values = listaaño)
Año.set(listaaño[0])
Año.grid(column=0, row=2, padx=5, pady=5)

Mes = ttk.Combobox(frame, values = listames)
Mes.set(listames[0])
Mes.grid(column=1, row=2, padx=5, pady=5)

Consola = ttk.Combobox(frame, values = listaconsola)
Consola.set(listaconsola[0])
Consola.grid(column=2, row=2, padx=5, pady=5)

fig, axs = plt.subplots(dpi=80, figsize=(13, 4), sharey=True)
fig.suptitle('Stock Enviado')

x=[]
y=[]
resultado = Grafica(conex(), Año.get(), Mes.get(), Consola.get())
for row in resultado:
    x.append(row[1])
    y.append(row[0])

for n in range(0, len(x)):
    if x[n] == 'January':
        x[n] = 'Enero'
    if x[n] == 'February':
        x[n] = 'Febrero'
    if x[n] == 'March':
        x[n] = 'Marzo'
    if x[n] == 'April':
        x[n] = 'Abril'
    if x[n] == 'May':
        x[n] = 'Mayo'
    if x[n] == 'June':
        x[n] = 'Junio'
    if x[n] == 'July':
        x[n] = 'Julio'
    if x[n] == 'August':
        x[n] = 'Agosto'
    if x[n] == 'September':
        x[n] = 'Septiembre'
    if x[n] == 'October':
        x[n] = 'Octubre'
    if x[n] == 'November':
        x[n] = 'Noviembre'
    if x[n] == 'December':
        x[n] = 'Diciembre'

axs.bar(x, y)

canvas = FigureCanvasTkAgg(fig, master = frame)
canvas.draw()
canvas.get_tk_widget().grid(column=0, row=0, columnspan=4)

def Actualizar():
    fig.clear()
    x2=[]
    y2=[]
    z=[]
    z2=[]
    month = Mes.get()
    if month == 'Enero':
        month = 'January'
    if month == 'Febrero':
        month = 'February'
    if month == 'Marzo':
        month = 'March'
    if month == 'Abril':
        month = 'April'
    if month == 'Mayo':
        month = 'May'
    if month == 'Junio':
        month = 'June'
    if month == 'Julio':
        month = 'July'
    if month == 'Agosto':
        month = 'August'
    if month == 'Septiembre':
        month = 'September'
    if month == 'Octubre':
        month = 'October'
    if month == 'Noviembre':
        month = 'November'
    if month == 'Diciembre':
        month = 'December'

    resultado2 = Grafica(conex(), Año.get(), month, Consola.get())
    for row in resultado2:
        try:
            x2.append(row[1])
            y2.append(row[0])
            z.append(row[2])
        except:
            z=[]

    if z != []:
        for n in range(0, len(z)):
            if z[n] == 'PlayStation 5':
                z2.append('skyblue')
            if z[n] == 'PlayStation 4':
                z2.append('black')
            if z[n] == 'Nintendo Switch':
                z2.append('red')
            if z[n] == 'Nintendo Switch OLED' :
                z2.append('blue')
            if z[n] == 'Xbox Series S':
                z2.append('green')
            if z[n] == 'Xbox Series X':
                z2.append('gray')

    for n in range(0, len(z)):
        for m in range(0, len(z)):
            if n != m:
                if z[n] == z[m]:
                    z[n] ='_'+z[n]

    for n in range(0, len(x2)):
        if x2[n] == 'January':
            x2[n] = 'Enero'
        if x2[n] == 'February':
            x2[n] = 'Febrero'
        if x2[n] == 'March':
            x2[n] = 'Marzo'
        if x2[n] == 'April':
            x2[n] = 'Abril'
        if x2[n] == 'May':
            x2[n] = 'Mayo'
        if x2[n] == 'June':
            x2[n] = 'Junio'
        if x2[n] == 'July':
            x2[n] = 'Julio'
        if x2[n] == 'August':
            x2[n] = 'Agosto'
        if x2[n] == 'September':
            x2[n] = 'Septiembre'
        if x2[n] == 'October':
            x2[n] = 'Octubre'
        if x2[n] == 'November':
            x2[n] = 'Noviembre'
        if x2[n] == 'December':
            x2[n] = 'Diciembre'

    fig2, axs2 = plt.subplots(dpi=80, figsize=(13, 4), sharey=True)
    fig2.suptitle('Stock Enviado')
    
    if z2 != []:
        axs2.bar(x2, y2, color = z2, label = z)
        axs2.legend(title='Consolas:')
        if month != 'Sin Especificar':
            axs2.set_xlim([0, 31])
    
    else:
        axs2.bar(x2, y2)

    canvas = FigureCanvasTkAgg(fig2, master = frame)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=0, columnspan=4)

Botón = ttk.Button(frame, text='Generar Gráfico', command=Actualizar)
Botón.grid(column = 3, row = 2, padx = 5, pady = 5)

root.mainloop()