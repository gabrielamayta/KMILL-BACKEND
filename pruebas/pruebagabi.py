import mysql.connector
from flask import Flask,jsonify

#Conexión con el servidor MySQL Server

app = Flask(__name__)
#@app.route("/Usuario_rol/<int:id>")
 
def Usua_rol(id): 
#Consulta SQL que ejecutaremos, en este caso un select
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    sqlSelect = """SELECT id, id_usuario, id_rol FROM Usuario_rol WHERE id = %s """
    #Establecemos un cursor para la conexión con el servidor MySQL
    cursor = conexionMySQL.cursor(dictionary=True)
    #A partir del cursor, ejecutamos la consulta SQL
    cursor.execute(sqlSelect,(id,))
    #Guardamos el resultado de la consulta en una variable
    resultadoSQL = cursor.fetchone()
    
    #Cerramos el cursor y la conexión con MySQL
    cursor.close()
    conexionMySQL.close()
    
    #Mostramos el resultado por pantalla
    return jsonify(resultadoSQL)
print("??")

print(app.url_map)