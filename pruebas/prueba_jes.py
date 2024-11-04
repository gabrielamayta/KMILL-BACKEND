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
###
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

#codigo copiado de mika

@app.route('/producto/<int:id>') 
def detalle_producto(id):
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    sqlSelect = """SELECT Nombre, Descripción, Precio, stock FROM Producto WHERE id = %s"""
    cursor = conexionMySQL.cursor()
    cursor.execute(sqlSelect, (id,))
    resultadoSQL = cursor.fetchone()

    cursor.close()
    conexionMySQL.close()         
    return jsonify(resultadoSQL)

# Resto de tu código...
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("Datos recibidos:", data)  # Para depuración

    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    telefono = data.get('telefono')  # Asegúrate de que este sea el nombre correcto
    password = data.get('password')

    if not all([nombre, apellido, email, telefono, password]):
        return jsonify({"message": "Faltan datos"}), 400

    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )

    sqlInsert = """INSERT INTO Usuario (Nombre, Apellido, Email, teléfono, Password) 
                   VALUES (%s, %s, %s, %s, %s)"""

    cursor = conexionMySQL.cursor()
    
    try:
        cursor.execute(sqlInsert, (nombre, apellido, email, telefono, password))
        conexionMySQL.commit()
        response = jsonify({"message": "Usuario registrado exitosamente"})
        response.status_code = 201
    except mysql.connector.Error as err:
        print(f"Error: {err}")  # Imprime el error específico
        conexionMySQL.rollback()
        response = jsonify({"message": "Error al registrar el usuario", "error": str(err)})
        response.status_code = 400
    finally:
        cursor.close()
        conexionMySQL.close()

    return response

##ruta de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Faltan datos"}), 400
    
    # Aquí debes verificar las credenciales en tu base de datos
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    cursor = conexionMySQL.cursor()
    cursor.execute("SELECT * FROM Usuario WHERE Email = %s AND Password = %s", (email, password))
    user = cursor.fetchone()

    cursor.close()
    conexionMySQL.close()

    if user:
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401



##ruta de precio
@app.route('/precio_producto/<int:id>')
def Precio(id):
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )    
    sqlSelect = """SELECT Precio FROM Producto WHERE id = %s"""
    cursor = conexionMySQL.cursor(dictionary=True)
    cursor.execute(sqlSelect, (id,))
    resultadoSQL = cursor.fetchone()
    cursor.close()
    conexionMySQL.close()
    return jsonify(resultadoSQL)


if __name__ == '__main__':
    app.run(debug=True)
##usuario ruta-register

