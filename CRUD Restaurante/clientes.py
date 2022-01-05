import mysql.connector

class Clientes:
    def __init__(self):
        self.conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="toor", 
        database="restaurante")

    def __str__(self):
        datos = self.consulta_cliente()
        aux=""
        for fila in datos:
            aux = aux + str(fila) + "\n"
        return aux
        
    def consulta_cliente(self):
        cur = self.conexion.cursor()
        cur.execute("SELECT * FROM clientes")
        datos = cur.fetchall()
        cur.close()
        return datos

    def buscar_cliente(self,Id):
        cur = self.conexion.cursor()
        sql= "SELECT * FROM clientes WHERE id = {}".format(Id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertar_cliente(self,nombre,telefono):
        cur = self.conexion.cursor()
        sql= """INSERT INTO clientes (nombre,telefono) VALUES ('{}','{}')""".format(nombre,telefono)
        cur.execute(sql)
        n = cur.rowcount
        self.conexion.commit()
        cur.close()
        return n

    def eliminar_cliente(self,id):
        cur = self.conexion.cursor()
        sql = """DELETE FROM clientes WHERE id="""+ id
        cur.execute(sql)
        n=cur.rowcount
        self.conexion.commit()
        cur.close()
        return n

    def actualizar_cliente(self,Id,nombre,telefono):
        cur = self.conexion.cursor()
        sql = """UPDATE clientes SET nombre='{}', telefono='{}' WHERE id={}""".format(nombre,telefono,Id)
        cur.execute(sql)
        n=cur.rowcount
        self.conexion.commit()
        cur.close()
        return n