import mysql.connector
 
#Conexión con el servidor MySQL Server
conexionMySQL = mysql.connector.connect(
    host='10.9.120.5',
    user='kmill',
    passwd='kmill111',
    db='kmill'
)
 
#Consulta SQL que ejecutaremos, en este caso un select
sqlSelect = """SELECT id, id_usuario, id_rol
           FROM Usuario_rol
           ORDER BY id DESC
          """
#Establecemos un cursor para la conexión con el servidor MySQL
cursor = conexionMySQL.cursor()
#A partir del cursor, ejecutamos la consulta SQL
cursor.execute(sqlSelect)
#Guardamos el resultado de la consulta en una variable
resultadoSQL = cursor.fetchall()
 
#Cerramos el cursor y la conexión con MySQL
cursor.close()
conexionMySQL.close()
 
#Mostramos el resultado por pantalla
print (resultadoSQL)