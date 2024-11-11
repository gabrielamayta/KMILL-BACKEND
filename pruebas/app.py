import jwt
import datetime
from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS
#Conexión con el servidor MySQL Server

app = Flask(__name__)
CORS(app)

#@app.route('/Pedidos')
#def pedidos():
#    conexionMySQL = mysql.connector.connect(
#        host='10.9.120.5',
#        user='kmill',
#        passwd='kmill111',
#        db='kmill'
#    )
#    #Consulta SQL que ejecutaremos, en este caso un select
#    sqlSelect = """SELECT * FROM Pedido""" 
#    #Establecemos un db para la conexión con el servidor MySQL
#    db = conexionMySQL.cursor()
#    #A partir del db, ejecutamos la consulta SQL
#    db.execute(sqlSelect)
#    #Guardamos el resultado de la consulta en una variable
#    resultadoSQL = db.fetchall()
#
#    #Cerramos el db y la conexión con MySQL
#    db.close()
#    conexionMySQL.close()
#    return jsonify(resultadoSQL)



@app.route('/Pedido', methods = ('PUT',))
def detalle_pedido(id):
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    #Consulta 1
    qpedido = """SELECT id FROM Pedidos WHERE id = %s"""
    db = conexionMySQL.cursor(dictionary=True)
    db.execute(qpedido, (id,))
    nropedido = db.fetchone()['id']

    #Consulta 2
    qdetalle_pedido = """SELECT * FROM Detalle_pedido WHERE id = %s"""
    db.execute(qdetalle_pedido, (id,))
    detalle_pedido = list(db)

    #Cerramos el db y la conexión con MySQL
    db.close()
    conexionMySQL.close()
    
    result = {"pedido": nropedido, "detalle pedido": detalle_pedido }
    return jsonify(result)





# Mika codigo 






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







#jessica codigo







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


#@app.route('/producto/<int:id>') 
#def detalle_producto(id):
#    conexionMySQL = mysql.connector.connect(
#        host='10.9.120.5',
#        user='kmill',
#        passwd='kmill111',
#        db='kmill'
#    )
#    sqlSelect = """SELECT Nombre, Descripción, Precio, stock FROM Producto WHERE id = %s"""
#    cursor = conexionMySQL.cursor()
#    cursor.execute(sqlSelect, (id,))
#    resultadoSQL = cursor.fetchone()
#
#    cursor.close()
#    conexionMySQL.close()         
#    return jsonify(resultadoSQL)

# Resto de tu código...
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("Datos recibidos:", data)  # Para depuración

    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    telefono = data.get('telefono')
    password = data.get('password')

    if not all([nombre, apellido, email, telefono, password]):
        return jsonify({"message": "Faltan datos"}), 400

    # Determinar el rol basado en el dominio del correo
    if '@kmill.com' in email:
        rol_id = 1  # Admin
    elif '@gmail.com' in email:
        rol_id = 2  # Usuario
    else:
        return jsonify({"message": "Correo no válido para registro"}), 400

    # Conexión a la base de datos MySQL
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )

    try:
        cursor = conexionMySQL.cursor()

        # Insertar el usuario en la tabla Usuario
        sqlInsert = """INSERT INTO Usuario (Nombre, Apellido, Email, teléfono, Password) 
                       VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sqlInsert, (nombre, apellido, email, telefono, password))
        usuario_id = cursor.lastrowid  # Obtener el ID del nuevo usuario insertado

        # Insertar el rol en la tabla Usuario_rol
        sqlInsertRol = """INSERT INTO Usuario_rol (id_usuario, id_rol) 
                          VALUES (%s, %s)"""
        cursor.execute(sqlInsertRol, (usuario_id, rol_id))

        conexionMySQL.commit()  # Confirmar los cambios
        print(f"Rol {rol_id} insertado para el usuario {usuario_id}")
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
        return jsonify({"message": "Correo o contraseña faltantes"}), 400

    # Consultar el usuario por email
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )

    try:
        cursor = conexionMySQL.cursor(dictionary=True)

        # Buscar el usuario por email
        cursor.execute("SELECT * FROM Usuario WHERE Email = %s", (email,))
        usuario = cursor.fetchone()

        if usuario and usuario['Password'] == password:
            # Obtener el rol del usuario
            cursor.execute("""SELECT r.nombre_rol
                              FROM Rol r
                              JOIN Usuario_rol ur ON r.id = ur.id_rol
                              WHERE ur.id_usuario = %s""", (usuario['id'],))
            rol = cursor.fetchone()

            if rol:
                return jsonify({
                    "message": "Inicio de sesión exitoso",
                    "email": usuario['Email'],
                    "role": rol['nombre_rol']
                })
            else:
                return jsonify({"message": "No se encontró rol para este usuario"}), 404
        else:
            return jsonify({"message": "Correo o contraseña incorrectos"}), 401

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({"message": "Error en la base de datos", "error": str(err)}), 500
    finally:
        cursor.close()
        conexionMySQL.close()



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

 


 # codigo Gaby 




@app.route("/Usuario_rol/<int:id>")
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



#Codigo mai

@app.route('/productopedido')
def producto_pedido():
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    cursor = conexionMySQL.cursor(dictionary=True)
    sqlSelect = """SELECT id, Nombre, Descripcion, Precio, imagen FROM Producto"""
    cursor.execute(sqlSelect)
    productos = cursor.fetchall()
    
    cursor.close()
    conexionMySQL.close()
    return jsonify(productos)


#@app.route('/detalle_pedido/<int:id>')
#def detalle_pedido(id):
#    conexionMySQL = mysql.connector.connect(
#        host='10.9.120.5',
#        user='kmill',
#        passwd='kmill111',
#        db='kmill'
#    )
#    #Consulta 1
#    qpedido = """SELECT id FROM Pedidos WHERE id = %s"""
#    db = conexionMySQL.cursor(dictionary=True)
#    db.execute(qpedido, (id,))
#    nropedido = db.fetchone()['id']
#
#    #Consulta 2
#    qdetalle_pedido = """SELECT * FROM Detalle_pedido WHERE id = %s"""
#    db.execute(qdetalle_pedido, (id,))
#    detalle_pedido = list(db)
#
#    #Cerramos el db y la conexión con MySQL
#    db.close()
#    conexionMySQL.close()
#    
#    result = {"pedido": nropedido, "detalle pedido": detalle_pedido }
#    return jsonify(result)



@app.route('/detalle_pedidos')
def detalle_pedidos():
    page = request.args.get('page', 1, type=int)  # Obtener la página, por defecto 1
    per_page = 5  # Número de elementos por página

    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )

    # Consulta paginada
    qdetalle_pedidos = """
        SELECT * FROM Detalle_pedido
        LIMIT %(per_page)s OFFSET %(offset)s
    """
    db = conexionMySQL.cursor(dictionary=True)
    db.execute(qdetalle_pedidos, {'per_page': per_page, 'offset': (page - 1) * per_page})
    detalle_pedidos = list(db)

    # Cerramos el db y la conexión con MySQL
    db.close()
    conexionMySQL.close()

    return jsonify({'pedidos': detalle_pedidos})






# Codigo valen





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