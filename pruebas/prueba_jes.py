import mysql.connector
from flask import Flask, jsonify, request
import requests 

app = Flask(__name__)
#####Rutas; 
@app.route('/ingrediente/<int:id>')
def ingredient(id):
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

#--------/Filtrado/---------
@app.route('/ingrediente_producto/<int:id>', methods=['GET'])
def ingredientProduct(id):
    # Conexión con el servidor MySQL
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    
    # Obtener el parámetro de búsqueda si se proporciona
    nombre_ingrediente = request.args.get('nombre', default='', type=str)

    # Consulta SQL para obtener los ingredientes de un producto específico
    sqlSelect = """
    SELECT i.Nombre, ip.id_Ingredientes
    FROM Ingredientes_Productos ip
    JOIN Ingrediente i ON ip.id_Ingredientes = i.id
    WHERE ip.id_Producto = %s
    """
    
    # Agregar condición de filtrado si se proporciona un nombre
    if nombre_ingrediente:
        sqlSelect += " AND i.Nombre LIKE %s"
        params = (id, f'%{nombre_ingrediente}%')
    else:
        params = (id,)
    
    # Establecemos un cursor para la conexión con el servidor MySQL
    cursor = conexionMySQL.cursor(dictionary=True)
    
    # Ejecutamos la consulta SQL
    cursor.execute(sqlSelect, params)
    
    # Guardamos el resultado de la consulta en una variable
    resultadoSQL = cursor.fetchall()
    
    # Cerramos el cursor y la conexión con MySQL
    cursor.close()
    conexionMySQL.close()
    
    return jsonify(resultadoSQL)



print("??")
print(app.url_map)
#me falta hacer los methodos -- tengo que fijarme bien este codigo que  encontre

#@app.route('/ingrediente/<int:id>', methods=['DELETE'])
#def delete_ingredient(id):
#    # Conexión con el servidor MySQL
#    conexionMySQL = mysql.connector.connect(
#        host='10.9.120.5',
#        user='kmill',
#        passwd='kmill111',
#        db='kmill'
#    )
#    
#    # Consulta SQL para eliminar un ingrediente por su ID
#    sqlDelete = """DELETE FROM Ingrediente WHERE id = %s"""
#    
#    try:
#        # Establecemos un cursor para la conexión con el servidor MySQL
#        cursor = conexionMySQL.cursor()
#        
#        # Ejecutamos la consulta SQL
#        cursor.execute(sqlDelete, (id,))
#        
#        # Confirmamos los cambios en la base de datos
#        conexionMySQL.commit()
#        
#        # Verificamos si se eliminó algún registro
#        if cursor.rowcount == 0:
#            return jsonify({"message": "Ingrediente no encontrado"}), 404
#        
#        return jsonify({"message": "Ingrediente eliminado exitosamente"}), 200
#    except mysql.connector.Error as err:
#        return jsonify({"error": str(err)}), 500
#    finally:
#        # Cerramos el cursor y la conexión con MySQL
#        cursor.close()
#        conexionMySQL.close()
#