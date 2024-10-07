import mysql.connector
from flask import Flask, jsonify
import requests 

app = Flask(__name__)
#####Rutas; 
@app.route('/ingrediente/<int:id>')
def ingredient(id):
#Conexión con el servidor MySQL Server
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )    
    #Consulta SQL que ejecutaremos, en este caso un select
    sqlSelect = """SELECT Nombre,id FROM Ingrediente WHERE id = %s"""
    #Establecemos un cursor para la conexión con el servidor MySQL
    cursor = conexionMySQL.cursor(dictionary=True)
    #A partir del cursor, ejecutamos la consulta SQL
    cursor.execute(sqlSelect,(id,))
    #Guardamos el resultado de la consulta en una variable
    resultadoSQL = cursor.fetchone()

    #Cerramos el cursor y la conexión con MySQL
    cursor.close()
    conexionMySQL.close()
    return jsonify(resultadoSQL)


@app.route('/ingrediente_producto/<int:id>')
def ingredientProduct(id):
#Conexión con el servidor MySQL Server
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )    
    #Consulta SQL que ejecutaremos, en este caso un select
    sqlSelect = """SELECT id_Producto,id_Ingredientes,id FROM Ingredientes_Productos WHERE id = %s"""
    #Establecemos un cursor para la conexión con el servidor MySQL
    cursor = conexionMySQL.cursor(dictionary=True)
    #A partir del cursor, ejecutamos la consulta SQL
    cursor.execute(sqlSelect,(id,))
    #Guardamos el resultado de la consulta en una variable
    resultadoSQL = cursor.fetchone()

    #Cerramos el cursor y la conexión con MySQL
    cursor.close()
    conexionMySQL.close()
    return jsonify(resultadoSQL)
print("??")
print(app.url_map)
###Detalle-Rutas
###metodos
###put
#
#@app.route("/ingrediente",methods=('PUT',))
#def agregar_ingrediente():
#    nombre = request.json["nombre"]
#    conexionMySQL = mysql.connector.connect(
#        host='10.9.120.5',
#        user='kmill',
#        passwd='kmill111',
#        db='kmill'
#    )    
#    sqlInsert = """INSERT INTO Ingrediente(name) VALUES (?)"""
#
#