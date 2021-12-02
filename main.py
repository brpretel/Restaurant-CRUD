from tkinter import *
from tkinter import ttk
from connexion import *
import mysql.connector
import pywhatkit
from datetime import datetime

#Ventana Principal
ventana=Tk()
ventana.title("Software Administracion y Notificacion de Pedidos")
ventana.geometry("600x500")

db=DataBase()
##
modificar= False
turno=int()
nombre= StringVar()
apellido= StringVar()
telefono= StringVar()


#Marco Ventana Principal
marco= LabelFrame(ventana, text="Formulario de Gestion de Pedidos")
marco.place(x=50, y=50, width=500,height=400)

#Labels y Entry
lblTurno= Label(marco,text="Turno").grid(column=0,row=0,padx=5,pady=5)#Label Turno
txtTurno= Entry(marco,textvariable=turno)#Entrada Turno
#txtTurno.grid(column=1,row=0)#Posicion Turno

lblNombre= Label(marco,text="Nombre").grid(column=0,row=1,padx=5,pady=5)#Label Nombre
txtNombre= Entry(marco,textvariable=nombre)#Entrada Nombre
txtNombre.grid(column=1,row=1)#Posicion Nombre

lblApellido= Label(marco,text="Apellido").grid(column=2,row=0,padx=5,pady=5)#Label Apellido
txtApellido= Entry(marco,textvariable=apellido)#Entrada Apellido
txtApellido.grid(column=3,row=0)#Posicion Apellido

lblTelefono= Label(marco,text="Telefono").grid(column=2,row=1,padx=5,pady=5)#Label Telefono
txtTelefono= Entry(marco,textvariable=telefono)#Entrada Telefono
txtTelefono.grid(column=3,row=1)#Posicion Telefono

lblMensaje=Label(marco,text="Escribe aqui tu Mensaje:", fg="red")
lblMensaje.grid(column=0,row=2,columnspan=4)

#tabla de la lista de pedidos(turnos)
tvPedidos= ttk.Treeview(marco)
tvPedidos.grid(column=0,row=3,columnspan=4)
tvPedidos["columns"]=("Turno","Nombre","Apellido","Telefono")
tvPedidos.column("#0",width=0, stretch=NO)
tvPedidos.column("Turno",width=50, anchor=CENTER)
tvPedidos.column("Nombre",width=50, anchor=CENTER)
tvPedidos.column("Apellido",width=50, anchor=CENTER)
tvPedidos.column("Telefono",width=50, anchor=CENTER)
#Nombres Encabezados Tabla
tvPedidos.heading("#0",text="")
tvPedidos.heading("Turno",text="Turno",anchor=CENTER)
tvPedidos.heading("Nombre",text="Nombre",anchor=CENTER)
tvPedidos.heading("Apellido",text="Apellido",anchor=CENTER)
tvPedidos.heading("Telefono",text="Telefono",anchor=CENTER)
#Llamar evento
tvPedidos.bind("<<TreeViewSelect>>",seleccionar)

#Botones de Accion
btnEliminar= Button(marco,text="Eliminar", command=lambda:eliminar())
btnEliminar.grid(column=1,row=4)

btnNuevo= Button(marco,text="Guardar", command= lambda:nuevo())
btnNuevo.grid(column=2,row=4)

btnModificar= Button(marco,text="Seleccionar", command= lambda:actualizar())
btnModificar.grid(column=3,row=4)

btnEnviarWhatsapp= Button(marco,text="Enviar Whatsapp", command= lambda:whatsapp())
btnEnviarWhatsapp.grid(column=4,row=4)

#Funciones Botones

#Funciones
def seleccionar(event):
    turno =tvPedidos.selection()[0]
    if int(id)>0:
        turno.set(tvPedidos.item(turno,"values")[1])
        nombre.set(tvPedidos.item(nombre,"values")[2])
        apellido.set(tvPedidos.item(apellido,"values")[3])
        telefono.set(tvPedidos.item(telefono,"values")[4])
#Funcion Cambio Texto Boton
def modificarFalse():
    global modificar
    modificar=False
    tvPedidos.config(selectmode=NONE)
    btnNuevo.config(text="Guardar")
    btnModificar.config(text="Seleccionar")
    btnEliminar.config(state=DISABLE)
#Funcion cambia Texto Boton
def modificarTrue():
    global modificar
    modificar=True
    tvPedidos.config(selectmode=BROWSE)
    btnNuevo.config(text="Nuevo")
    btnModificar.config(text="Modificar")
    btnEliminar.config(state=NORMAL)
def validar():
    return len(turno.get()) and len(nombre.get()) and len(apellido.get()) and len(telefono.get())
def limpiar():
    turno.set("")
    nombre.set("")
    apellido.set("")
    telefono.set("")

def vaciar_tabla():
    filas= tvPedidos.get_children()
    for fila in filas:
        tvPedidos.delete(fila)
def llenar_tabla():
    vaciar_tabla()
    sql= "select * from restaurante"
    db.cursor.execute(sql)
    filas=db.cursor.fetchall()
    for fila in filas:
        turno=fila[0]
        tvPedidos.insert("", END,turno, text=turno, value= fila)

def eliminar():
    id= tvPedidos.selection()[0]
    if int(turno)>0:
        sql="delete from restaurante where turno="+turno
        db.cursor.execute(sql)
        db.connection.commit()
        tvPedidos.delete(turno)
        lblMensaje.config(text="Se ha eliminado el registro correctamente.")
    else:
        lblMensaje.config(text="Seleccione un registro para eliminar.")

def nuevo():
    if modificar==False:
        if validar():
            val=(turno.get(),nombre.get(),apellido.get(),telefono.get())
            sql="insert into restaurante (turno,nombre,apellido,telefono) values (%s,%s,%s,%s)"
            db.cursor.execute(sql,val)
            db.connection.commit()
            lblMensaje.config(text="Se ha generado un nuevo turno.", fg="green")
            llenar_tabla()
            limpiar()
        else:lblMensaje.config(text="los campos no deben estar vacios", fg="red")
    else:
        modificarFalse()

def actualizar():
    if modificar==True:
        if validar():
            turno=tvEstudiantes.select()[0]
            val=(turno.get(),nombre.get(),apellido.get(),telefono.get())
            sql="update restaurante set turno="%s", nombre="%s", apellido="%s",telefono="%s qwhere turno="+turno
            db.cursor.execute(sql,val)
            db.connection.commit()
            lblMensaje.config(text="Se ha actualizado el pedido correctamente.", fg="green")
            llenar_tabla()
            limpiar()
        else:lblMensaje.config(text="los campos no deben estar vacios", fg="red")
    else:
        modificarTrue()

def whatsapp():
    ext = "+57"
        now = datetime.now()
        hora = now.hour
        minuto = now.minute + 1
        numero= tvPedidos.get_children[4]
        mensaje = self.tel_field.get(), self.mess_field.get(1.0, END)
    
        try:
            pywhatkit.sendwhatmsg(ext + numero, mensaje,hora,minuto,8,True,)
            print("Mensaje Enviado")
        except:
            print("Ocurrio Un Error")







llenar_tabla()
ventana.mainloop()