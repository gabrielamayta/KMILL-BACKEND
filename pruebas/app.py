from flask import Flask, jsonify
import mysql.connector

#Conexión con el servidor MySQL Server
conexionMySQL = mysql.connector.connect(
    host='10.9.120.5',
    user='kmill',
    passwd='kmill111',
    db='kmill'
)

app = Flask(__name__)


@app.route('/Roles')
def roles():
    #Consulta SQL que ejecutaremos, en este caso un select
    sqlSelect = """SELECT * FROM Rol"""
    #Establecemos un cursor para la conexión con el servidor MySQL
    cursor = conexionMySQL.cursor()
    #A partir del cursor, ejecutamos la consulta SQL
    cursor.execute(sqlSelect)
    #Guardamos el resultado de la consulta en una variable
    resultadoSQL = cursor.fetchall()

    #Cerramos el cursor y la conexión con MySQL
    cursor.close()
    conexionMySQL.close()
    return jsonify(resultadoSQL)

