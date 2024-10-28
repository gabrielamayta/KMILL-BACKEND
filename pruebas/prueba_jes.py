import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS  # Importa Flask-CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

##### Rutas; 
@app.route('/ingrediente/<int:id>')
def ingredient(id):
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )    
    sqlSelect = """SELECT Nombre,id FROM Ingrediente WHERE id = %s"""
    cursor = conexionMySQL.cursor(dictionary=True)
    cursor.execute(sqlSelect, (id,))
    resultadoSQL = cursor.fetchone()
    cursor.close()
    conexionMySQL.close()
    return jsonify(resultadoSQL)

@app.route('/ingrediente_producto/<int:id>', methods=['GET'])
def ingredientProduct(id):
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    
    nombre_ingrediente = request.args.get('nombre', default='', type=str)
    sqlSelect = """
    SELECT i.Nombre, ip.id_Ingredientes
    FROM Ingredientes_Productos ip
    JOIN Ingrediente i ON ip.id_Ingredientes = i.id
    WHERE ip.id_Producto = %s
    """
    
    if nombre_ingrediente:
        sqlSelect += " AND i.Nombre LIKE %s"
        params = (id, f'%{nombre_ingrediente}%')
    else:
        params = (id,)
    
    cursor = conexionMySQL.cursor(dictionary=True)
    cursor.execute(sqlSelect, params)
    resultadoSQL = cursor.fetchall()
    cursor.close()
    conexionMySQL.close()
    
    return jsonify(resultadoSQL)

# Resto de tu código...

if __name__ == '__main__':
    app.run(debug=True)
