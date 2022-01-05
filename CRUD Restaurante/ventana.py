from tkinter import*
from tkinter import messagebox
from tkinter import ttk
from clientes import Clientes
import pywhatkit

class Ventana(Frame):

    usuario = Clientes()

    def __init__(self, master= None):
        super().__init__(master, width=800,height=450)
        self.master = master
        self.master.resizable(width=False, height=False)
        self.pack()
        self.create_widgets()
        self.llenarTabla()
        self.habilitar_cajas("disabled")
        self.habilitar_botonesOper("normal")
        self.habilitar_boton_Guardar_Cancelar("disabled")
        self.id =-1


    def habilitar_cajas(self,estado):
        self.txtNameCl.configure(state=estado)
        self.txttel.configure(state=estado)
        self.txtmess.configure(state=estado)

    def habilitar_botonesOper(self,estado):
        self.btnNuevo.configure(state=estado)
        self.btnModificar.configure(state=estado)
        self.btnEliminar.configure(state=estado)

    def habilitar_boton_Guardar_Cancelar(self,estado):
        self.btnGuardar.configure(state=estado)
        self.btnCancelar.configure(state=estado)

    def limpiar_cajas(self):
        self.txtNameCl.delete(0,END)
        self.txttel.delete(0,END)

    def limpiar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def llenarTabla(self):
        datos = self.usuario.consulta_cliente()
        for row in datos:
            self.tabla.insert("",END,text=row[0],values= (row[1],row[2]))
        
        if len(self.tabla.get_children()) > 0:
            self.tabla.selection_set(self.tabla.get_children()[0])

    def fNuevo(self):
        self.habilitar_cajas("normal")
        self.habilitar_botonesOper("disabled")
        self.habilitar_boton_Guardar_Cancelar("normal")
        self.limpiar_cajas()
        self.txtNameCl.focus()

    def fGuardar(self):
        data1,data2= self.txtNameCl.get(),self.txttel.get()
        
        if self.id == -1 and len(data2)== 10:
            try:
                int(data2)
                self.usuario.insertar_cliente(self.txtNameCl.get(),self.txttel.get())
                self.limpiar_tabla()
                self.llenarTabla()
                self.limpiar_cajas()
                self.habilitar_boton_Guardar_Cancelar("disabled")
                self.habilitar_botonesOper("normal")
                self.habilitar_cajas("disabled")
            except:
                messagebox.showwarning("ERROR","No se permiten letras en el telefono")
        elif data1 =="" or data2 == "":
            messagebox.showwarning("ERROR","No pueden existir campos vacios")
        elif len(data2) != 10:
            messagebox.showwarning("ERROR","Debes ingresar 10 digitos en el telefono")
        else:
            self.usuario.actualizar_cliente(self.id,self.txtNameCl.get(),self.txttel.get())
            messagebox.showinfo("Modificar","Elemento modificado correctamente")
            self.id = -1
            self.limpiar_tabla()
            self.llenarTabla()
            self.limpiar_cajas()
            self.habilitar_boton_Guardar_Cancelar("disabled")
            self.habilitar_botonesOper("normal")
            self.habilitar_cajas("disabled")
    
        
    def fModificar(self):
        selected = self.tabla.focus()
        clave = self.tabla.item(selected,"text")

        if clave == "":
            messagebox.showwarning("MODIFICAR","Debes seleccionar un contacto para Modificarlo")
        else:
            self.id = clave
            self.habilitar_cajas("normal")
            valores = self.tabla.item(selected,"values")
            self.limpiar_cajas()
            self.txtNameCl.insert(0,valores[0])
            self.txttel.insert(1,valores[1])
            self.habilitar_botonesOper("disabled")
            self.habilitar_boton_Guardar_Cancelar("normal")
            self.txtNameCl.focus()
            

    def fEliminar(self):
        selected = self.tabla.focus()
        clave = self.tabla.item(selected,"text")

        if clave == "":
            messagebox.showwarning("ELIMINAR","Debes seleccionar un contacto para borrar")
        else:
            valores = self.tabla.item(selected,"values")
            data = str(clave) + ", " + valores[0] + ", " + valores[1]
            r = messagebox.askquestion("Eliminar","¿Deseas eliminar el contacto seleccionado?\n"+ data)
            
            if r == messagebox.YES:
                n = self.usuario.eliminar_cliente(str(clave))
                if n == 1:
                    messagebox.showinfo("ELIMINAR","Contacto Eliminado Correctamente")
                    self.limpiar_tabla()
                    self.llenarTabla()
                else:
                    messagebox.showinfo("ELIMINAR","No fue posible eliminar el Contacto")
            

    def fCancelar(self):
        r = messagebox.askquestion("Cancelar","¿Estas seguro que deseas cancelar la operacion actual?")
        if r == messagebox.YES:
            self.limpiar_cajas()
            self.habilitar_boton_Guardar_Cancelar("disabled")
            self.habilitar_botonesOper("normal")
            self.habilitar_cajas("disabled")

    def enviar_whatsapp(self):
        ext = "+57"
        selected = self.tabla.focus()
        clave = self.tabla.item(selected,"text")

        if clave == "":
            messagebox.showinfo("ENVIAR","Debes Seleccionar un contacto para enviar el mensaje")
        else:
            numero = self.tabla.item(selected,"values")[1]
            numero_cliente = numero
            print(type(numero_cliente))
            try:
                
                pywhatkit.sendwhatmsg_instantly(ext + numero_cliente, "hola",8,True,1)
                print("Mensaje Enviado")
                n = self.usuario.eliminar_cliente(str(clave))
                if n == 1:
                    messagebox.showinfo("ELIMINAR","Mensaje Enviado")
                    self.limpiar_tabla()
                    self.llenarTabla()
                else:
                    messagebox.showinfo("ELIMINAR","No fue posible enviar el mensaje")
            
            except:
                
                print("Ocurrio Un Error")



    def create_widgets(self):
        frame1 = Frame(self.master,borderwidth=5,relief="groove")
        frame1.place(relx=0.03, rely=0.13, relwidth=0.15,relheight=0.7)
        self.btnNuevo = Button(frame1,text="Nuevo",font = ("Verdana", 10)  ,bg="grey",fg="white",command=self.fNuevo)
        self.btnNuevo.place(relx=0.11, rely=0.25,relwidth=0.7)
        self.btnModificar = Button(frame1,text="Modificar",font = ("Verdana", 10) ,bg="grey",fg="white",command=self.fModificar)
        self.btnModificar.place(relx=0.11, rely=0.40,relwidth=0.7)
        self.btnEliminar = Button(frame1,text="Eliminar",font = ("Verdana", 10) ,bg="grey",fg="white",command=self.fEliminar)
        self.btnEliminar.place(relx=0.11, rely=0.55,relwidth=0.7)
        self.btnEnviar = Button(frame1,text="Enviar",font = ("Verdana", 10) ,bg="grey",fg="white",command=self.enviar_whatsapp)
        self.btnEnviar.place(relx=0.11, rely=0.70,relwidth=0.7)

        frame2 = Frame(self.master,borderwidth=5,relief="groove")
        frame2.place(relx=0.17, rely=0.13, relwidth=0.8,relheight=0.7)
        lbl1 = Label(frame2,text="Nombre Cliente",font=("Verdana",11))
        lbl1.place(relx=0.1, rely=0.08)
        self.txtNameCl = Entry(frame2)
        self.txtNameCl.place(relx=0.1, rely=0.16) 
        lbl2 = Label(frame2,text="Telefono",font=("Verdana",11))
        lbl2.place(relx=0.14, rely=0.3)
        self.txttel = Entry(frame2)
        self.txttel.place(relx=0.1, rely=0.38) 
        lbl3 = Label(frame2,text="Mensaje",font=("Verdana",11))
        lbl3.place(relx=0.14, rely=0.50)
        self.txtmess = Text(frame2)
        self.txtmess.insert(0.1,"Su pedido esta listo. Dirigete a vaporetto para reclamarlo")
        self.txtmess.place(relx=0.06, rely=0.58,relwidth=0.28,relheight=0.23) 
        self.btnGuardar = Button(frame2,text="Guardar",command=self.fGuardar)
        self.btnGuardar.place(relx=0.11, rely=0.83) 
        self.btnCancelar = Button(frame2,text="Cancelar",command=self.fCancelar)
        self.btnCancelar.place(relx=0.2, rely=0.83) 

        frame3 = Frame(frame2, bg="yellow")
        frame3.place(relx=0.45,rely=0.1,relwidth=0.5,relheight=0.8)

        self.tabla = ttk.Treeview(frame3,columns=("col1","col2"))
        self.tabla.column("#0",width=60)
        self.tabla.column("col1",width=120,anchor=CENTER)
        self.tabla.column("col2",width=115,anchor=CENTER)
        self.tabla.heading("#0", text="Turno", anchor=CENTER)
        self.tabla.heading("col1", text="Nombre Cliente", anchor=CENTER)
        self.tabla.heading("col2", text="Telefono", anchor=CENTER)
        self.tabla.pack(side=LEFT,fill=Y)
        self.tabla["selectmode"] = "browse"

        sb = Scrollbar(frame3,orient=VERTICAL)
        sb.pack(side=RIGHT,fill=Y)
        self.tabla.config(yscrollcommand=sb.set)
        sb.config(command=self.tabla.yview)
    
        
    def whatsapp(self):
        ext = "+57"
        selected = self.tabla.focus()
        clave = self.tabla.item(selected,"text")

        if clave == "":
            messagebox.showinfo("ENVIAR","Debes Seleccionar un contacto para enviar el mensaje")
        else:
            numero = self.tabla.item(selected,"values")[1]
            numero_cliente = numero
            try:
                
                pywhatkit.sendwhatmsg_instantly(ext + numero_cliente, "hola",8,True,1)
                print("Mensaje Enviado")
                self.fEliminar()
            except:
                
                print("Ocurrio Un Error")
