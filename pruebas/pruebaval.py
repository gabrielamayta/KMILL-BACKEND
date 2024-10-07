import mysql.connector
from flask import Flask,jsonify 



app = Flask(__name__)
@app.route('/Rol/<int:id>')
def Roles(id):

    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )

    sqlSelect = """SELECT nombre_rol, id FROM Rol WHERE id = %s """

    #Establecemos un cursor para la conexión con el servidor MySQL
    cursor = conexionMySQL.cursor(dictionary=True)

    #A partir del cursor, ejecutamos la consulta SQL
    cursor.execute(sqlSelect, (id,))

    #Guardamos el resultado de la consulta en una variable
    resultadoSQL = cursor.fetchone()

    #Cerramos el cursor y la conexión con MySQL
    cursor.close()
    conexionMySQL.close()
    return jsonify(resultadoSQL)

print(app.url_map)