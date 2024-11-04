from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Ruta para obtener el nombre de un producto por su ID
@app.route('/producto/<int:id>') 
def detalle_producto(id):
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    sqlSelect = """SELECT Nombre FROM Producto WHERE id = %s"""
    cursor = conexionMySQL.cursor()
    cursor.execute(sqlSelect, (id,))
    resultadoSQL = cursor.fetchone()

    cursor.close()
    conexionMySQL.close()
    
    if resultadoSQL:
        return jsonify({"titulo": resultadoSQL[0]})
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

# Ruta para obtener todos los productos
@app.route('/jsonproducto')
def producto():
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    cursor = conexionMySQL.cursor(dictionary=True)
    sqlSelect = """SELECT * FROM Producto"""
    cursor.execute(sqlSelect)
    productos = cursor.fetchall()
    
    cursor.close()
    conexionMySQL.close()
    return jsonify(productos)

# Ruta para obtener un producto y sus ingredientes
@app.route('/producto_ingrediente/<int:id>') 
def producto_ingrediente(id):
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    cursor = conexionMySQL.cursor()

    # Obtener el nombre del producto
    qProducto = """SELECT Nombre FROM Producto WHERE id = %s"""
    cursor.execute(qProducto, (id,))
    product = cursor.fetchone()

    # Obtener los ingredientes relacionados con el producto
    qIngrediente = """
        SELECT i.Nombre 
        FROM Ingrediente i
        INNER JOIN Ingredientes_Productos ip ON i.id = ip.id_Ingredientes
        WHERE ip.id_Producto = %s
    """
    cursor.execute(qIngrediente, (id,))
    ingredientes = cursor.fetchall()

    cursor.close()
    conexionMySQL.close()

    resultado = {
        "nombre_pro": product[0] if product else None,
        "ingredientes": [ingredient[0] for ingredient in ingredientes]
    }
    
    return jsonify(resultado)

# Ruta para borrar un producto por su ID
@app.route('/productoborrar/<int:id>', methods=['DELETE']) 
def borrar_producto(id):
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    sqlDelete = """DELETE FROM Producto WHERE id = %s"""
    cursor = conexionMySQL.cursor()
    cursor.execute(sqlDelete, (id,))
    conexionMySQL.commit()  # Confirmar los cambios
    
    cursor.close()
    conexionMySQL.close()
    return jsonify({"message": "Producto eliminado exitosamente"})

# Ruta para filtrar productos por nombre
@app.route('/filtroproducto/')
def filtro_producto():
    filtro = request.args.get('filtro', None)
    
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    cursor = conexionMySQL.cursor(dictionary=True)

    if filtro:
        query = 'SELECT * FROM Producto WHERE Nombre LIKE %s'
        cursor.execute(query, ('%' + filtro + '%',))
    else:
        query = 'SELECT * FROM Producto'
        cursor.execute(query)

    resultados = cursor.fetchall()
    cursor.close()
    conexionMySQL.close()
    
    return jsonify(resultados)

# Ruta para obtener el nombre de una categoría por su ID
@app.route('/categoria/<int:id>') 
def detalle_categoria(id):
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )

    sqlSelect = """SELECT Nombre FROM Categoria WHERE id = %s"""
    cursor = conexionMySQL.cursor()
    cursor.execute(sqlSelect, (id,))
    resultadoSQL = cursor.fetchone()

    cursor.close()
    conexionMySQL.close()
    return jsonify({"nombre_categoria": resultadoSQL[0]} if resultadoSQL else {"error": "Categoría no encontrada"})

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
