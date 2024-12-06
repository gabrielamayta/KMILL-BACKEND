import jwt
import datetime
from flask import Flask, jsonify, request, render_template, redirect, url_for
import mysql.connector
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
import os

# Configuración de la aplicación
app = Flask(__name__)
CORS(app)

# Variables de entorno para la base de datos
db_host = os.getenv("DB_HOST", "10.9.120.5")
db_user = os.getenv("DB_USER", "kmill")
db_password = os.getenv("DB_PASSWORD", "kmill111")
db_name = os.getenv("DB_NAME", "kmill")

# Función para obtener la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        passwd=db_password,
        db=db_name
    )

# Función para cerrar la conexión
def close_db_connection(cursor, connection):
    cursor.close()
    connection.close()

# Ruta para obtener el detalle del pedido
@app.route('/Pedido/<int:id>', methods=['PUT'])
def detalle_pedido(id):
    try:
        conexionMySQL = get_db_connection()
        cursor = conexionMySQL.cursor(dictionary=True)

        # Consulta 1
        qpedido = """SELECT id FROM Pedidos WHERE id = %s"""
        cursor.execute(qpedido, (id,))
        nropedido = cursor.fetchone()

        if not nropedido:
            return jsonify({"error": "Pedido no encontrado"}), 404

        # Consulta 2
        qdetalle_pedido = """SELECT * FROM Detalle_pedido WHERE id = %s"""
        cursor.execute(qdetalle_pedido, (id,))
        detalle_pedido = cursor.fetchall()

        close_db_connection(cursor, conexionMySQL)

        result = {"pedido": nropedido['id'], "detalle_pedido": detalle_pedido}
        return jsonify(result)

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error en la base de datos: {err}"}), 500

# Ruta para obtener el detalle de un producto
@app.route('/producto/<int:id>')
def detalle_producto(id):
    try:
        conexionMySQL = get_db_connection()
        cursor = conexionMySQL.cursor()

        sqlSelect = """SELECT Nombre FROM Producto WHERE id = %s"""
        cursor.execute(sqlSelect, (id,))
        resultadoSQL = cursor.fetchone()

        close_db_connection(cursor, conexionMySQL)

        if resultadoSQL:
            return jsonify({"titulo": resultadoSQL[0]})
        else:
            return jsonify({"error": "Producto no encontrado"}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error en la base de datos: {err}"}), 500

# Ruta para obtener todos los productos en formato JSON
@app.route('/api/producto')
def obtener_productos_json():
    try:
        conexionMySQL = get_db_connection()
        cursor = conexionMySQL.cursor(dictionary=True)

        sqlSelect = """SELECT * FROM Producto"""
        cursor.execute(sqlSelect)
        productos = cursor.fetchall()

        close_db_connection(cursor, conexionMySQL)
        return jsonify(productos)

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error en la base de datos: {err}"}), 500

# Ruta para mostrar los productos en una plantilla HTML
@app.route('/producto')
def obtener_productos_html():
    try:
        conexionMySQL = get_db_connection()
        cursor = conexionMySQL.cursor(dictionary=True)

        sqlSelect = """SELECT * FROM Producto"""
        cursor.execute(sqlSelect)
        productos = cursor.fetchall()

        close_db_connection(cursor, conexionMySQL)
        return render_template('lista_productos.html', productos=productos)

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error en la base de datos: {err}"}), 500

# Ruta para obtener los ingredientes de un producto
@app.route('/ingredientes/<int:id>')
def producto_ingredientes(id):
    try:
        conexionMySQL = get_db_connection()
        cursor = conexionMySQL.cursor(dictionary=True)

        # Obtener los ingredientes del producto con el id
        qIngre = """
        SELECT i.Nombre, p.id as IdPro 
        FROM Ingrediente i
        JOIN Ingredientes_Productos ip ON ip.id_Ingredientes = i.id
        JOIN Producto p ON ip.id_Producto = p.id
        WHERE p.id = %s
        """
        cursor.execute(qIngre, (id,))
        ingredientes = cursor.fetchall()

        qNombre = """
        SELECT Nombre 
        FROM Producto
        WHERE id = %s
        """
        cursor.execute(qNombre, (id,))
        producto = cursor.fetchone()

        close_db_connection(cursor, conexionMySQL)

        if ingredientes:
            return render_template('ingredientes_producto.html', prod=producto, ing=ingredientes)
        else:
            return "No se encontraron ingredientes para este producto", 404

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error en la base de datos: {err}"}), 500

# Ruta para borrar un ingrediente
@app.route('/borrar_ingrediente/<int:id>', methods=['POST'])
def borrar_ingrediente(id):
    try:
        conexionMySQL = get_db_connection()
        cursor = conexionMySQL.cursor()

        # Eliminar el ingrediente de la tabla Ingrediente
        sqlDelete = """DELETE FROM Ingrediente WHERE id = %s"""
        cursor.execute(sqlDelete, (id,))
        conexionMySQL.commit()  # Confirmar la eliminación

        close_db_connection(cursor, conexionMySQL)

        # Redirigir a la lista de ingredientes después de borrar
        return redirect(url_for('obtener_ingredientes'))

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error en la base de datos: {err}"}), 500

# Ruta para editar un ingrediente
@app.route('/editar_ingrediente/<int:id>', methods=['GET', 'POST'])
def editar_ingrediente(id):
    if request.method == 'POST':
        # Obtener los nuevos valores del formulario
        nuevo_nombre = request.form['nombre']

        try:
            conexionMySQL = get_db_connection()
            cursor = conexionMySQL.cursor()

            # Actualizar el nombre del ingrediente en la base de datos
            sqlUpdate = """UPDATE Ingrediente SET Nombre = %s WHERE id = %s"""
            cursor.execute(sqlUpdate, (nuevo_nombre, id))
            conexionMySQL.commit()  # Confirmar la actualización

            close_db_connection(cursor, conexionMySQL)

            # Redirigir a la lista de ingredientes después de editar
            return redirect(url_for('obtener_ingredientes'))

        except mysql.connector.Error as err:
            return jsonify({"error": f"Error en la base de datos: {err}"}), 500
    else:
        try:
            conexionMySQL = get_db_connection()
            cursor = conexionMySQL.cursor(dictionary=True)

            # Obtener el ingrediente que se va a editar
            sqlSelect = """SELECT id, Nombre FROM Ingrediente WHERE id = %s"""
            cursor.execute(sqlSelect, (id,))
            ingrediente = cursor.fetchone()

            close_db_connection(cursor, conexionMySQL)

            if ingrediente:
                return render_template('editar_ingrediente.html', ingrediente=ingrediente)
            else:
                return jsonify({"error": "Ingrediente no encontrado"}), 404

        except mysql.connector.Error as err:
            return jsonify({"error": f"Error en la base de datos: {err}"}), 500

# Ruta para obtener todos los ingredientes y mostrarlos en una plantilla HTML
@app.route('/ingredientes', methods=['GET'])
def obtener_ingredientes():
    try:
        conexionMySQL = get_db_connection()
        cursor = conexionMySQL.cursor(dictionary=True)

        # Consulta para obtener todos los ingredientes
        sqlSelect = """SELECT id, Nombre FROM Ingrediente"""
        cursor.execute(sqlSelect)
        ingredientes = cursor.fetchall()

        close_db_connection(cursor, conexionMySQL)
        
        # Verificar que se obtuvieron los ingredientes
        print(ingredientes)  # Para verificar que los datos se obtienen correctamente

        # Renderizamos la plantilla 'ingredientes.html' y pasamos los ingredientes a ella
        return render_template('ingredientes.html', ing=ingredientes)

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error en la base de datos: {err}"}), 500

# Ruta para mostrar el formulario para agregar un ingrediente
@app.route('/agregar_ingrediente', methods=['GET'])
def agregar_ingrediente_form():
    return render_template('agregar_ingrediente.html')

# Ruta para manejar el formulario y agregar un ingrediente a la base de datos
@app.route('/agregar_ingrediente', methods=['POST'])
def agregar_ingrediente():
    nombre = request.form.get('nombre')

    if not nombre:
        return jsonify({"error": "El nombre del ingrediente es obligatorio"}), 400

    try:
        conexionMySQL = get_db_connection()
        cursor = conexionMySQL.cursor()

        # Insertar el nuevo ingrediente en la base de datos
        sqlInsert = """INSERT INTO Ingrediente (Nombre) VALUES (%s)"""
        cursor.execute(sqlInsert, (nombre,))
        conexionMySQL.commit()  # Confirmar la inserción

        close_db_connection(cursor, conexionMySQL)

        # Redirigir a la lista de ingredientes después de agregarlo
        return redirect(url_for('obtener_ingredientes'))

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error al agregar el ingrediente: {err}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
