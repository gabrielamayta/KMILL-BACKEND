import mysql.connector

conexion = mysql.connector.connect(user='kmill', password='kmill111',
                                    host='10.9.120.5', 
                                    database='kmill')

print(conexion)


sqlSelect = """SELECT id, Nombre, stock, id_categoria
           FROM Producto
           ORDER BY id DESC
           LIMIT 2"""

cursor = conexion.cursor()

cursor.execute(sqlSelect)

resultadoSQL = cursor.fetchall()

cursor.close()
conexion.close()

print (resultadoSQL)


