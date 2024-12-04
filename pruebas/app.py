import jwt
import datetime
from flask import Flask, jsonify, request, render_template
import mysql.connector
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
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

# ruta para obtener todos los productos en formato JSON
@app.route('/api/producto')
def obtener_productos_json():
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


# ruta para mostrar los productos en una plantilla HTML
@app.route('/producto')
def obtener_productos_html():
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
    return render_template('lista_productos.html', productos=productos)



@app.route('/ingredientes/<int:id>')
def producto_ingredientes(id):
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    cursor = conexionMySQL.cursor(dictionary=True)
    
    # Obtener los ingredientes del producto con el id
    qIngre = """
    SELECT i.Nombre 
    FROM Ingrediente i
    JOIN producto_ingrediente pi ON pi.ingrediente_id = i.id
    WHERE pi.producto_id = %s
    """
    cursor.execute(qIngre, (id,))
    ingredientes = cursor.fetchall()
    

    # Obtener información del producto (opcional)
    qProducto = "SELECT Nombre FROM Producto WHERE id = %s"
    cursor.execute(qProducto, (id,))
    producto = cursor.fetchone()

    cursor.close()
    conexionMySQL.close()

    # Pasar los datos al template
    return render_template('detalle_produc.html', ing=ingredientes, producto=producto)









@app.route('/ingredientes') 
def lista_ingredientes():
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    cursor = conexionMySQL.cursor(dictionary=True)

    # Obtener el nombre del producto
    qIngre = """SELECT Nombre FROM Ingrediente"""
    cursor.execute(qIngre)
    ingredient = cursor.fetchall()
    print(ingredient)
    
    cursor.close()
    conexionMySQL.close()
    return render_template('ingredientes.html', ing=ingredient)

if __name__ == '__main__':
    app.run(debug=True)








# Ruta para obtener un producto y sus ingredientes
@app.route('/api/producto_ingrediente/<int:id>') 
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
@app.route('/ingredientes', methods=['GET'])
def obtener_ingredientes():
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )

    try:
        cursor = conexionMySQL.cursor(dictionary=True)
        sqlSelect = """SELECT id, Nombre FROM Ingrediente"""
        cursor.execute(sqlSelect)
        ingredientes = cursor.fetchall()

        return jsonify({"ingredientes": ingredientes})
    except mysql.connector.Error as err:
        return jsonify({"message": "Error al obtener los ingredientes", "error": str(err)}), 500
    finally:
        cursor.close()
        conexionMySQL.close()

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
        # calculo el hash del password
        password=generate_password_hash(password)

        # Insertar el usuario en la tabla Usuario
        sqlInsert = """INSERT INTO Usuario (Nombre, Apellido, Email, teléfono, Password) 
                       VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sqlInsert, (nombre, apellido,  email, telefono, password))
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

        if usuario and check_password_hash(usuario['Password'], password):
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

##ruta de modificar productos
@app.route('/productoActualizar/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    # Conexión a la base de datos MySQL
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )

    data = request.get_json()  # Obtener los datos enviados en el cuerpo de la solicitud

    # Asegurarse de que los datos necesarios estén presentes
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')

    if not nombre or not descripcion or not precio:
        return jsonify({"message": "Faltan datos necesarios"}), 400

    try:
        cursor = conexionMySQL.cursor()

        # Consulta para actualizar el producto
        sqlUpdate = """UPDATE Producto 
                       SET Nombre = %s, Descripcion = %s, Precio = %s
                       WHERE id = %s"""
        cursor.execute(sqlUpdate, (nombre, descripcion, precio, id))

        conexionMySQL.commit()  # Confirmar los cambios
        cursor.close()
        conexionMySQL.close()

        return jsonify({"message": "Producto actualizado exitosamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"message": "Error al actualizar el producto", "error": str(err)}), 500
@app.route('/producto/agregar', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    id_categoria = data.get('id_categoria')
    imagen = data.get('imagen')
    ingredientes_seleccionados = data.get('ingredientes')  # Ingredientes seleccionados

    # Verificar que todos los datos necesarios están presentes
    if not all([nombre, descripcion, precio, id_categoria, imagen, ingredientes_seleccionados]):
        return jsonify({"message": "Faltan datos"}), 400

    # Conexión a la base de datos MySQL
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )

    try:
        cursor = conexionMySQL.cursor()

        # Insertar el nuevo producto
        sqlInsert = """
            INSERT INTO Producto (Nombre, Descripcion, Precio, id_categoria, Imagen)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sqlInsert, (nombre, descripcion, precio, id_categoria, imagen))

        # Obtener el ID del nuevo producto insertado
        id_Producto = cursor.lastrowid

        # Insertar los ingredientes seleccionados en la tabla de relación Ingredientes_Productos
        for id_ingrediente in ingredientes_seleccionados:
            sqlInsertIngrediente = """
                INSERT INTO Ingredientes_Productos (id_Producto, id_ingredientes)
                VALUES (%s, %s)
            """
            cursor.execute(sqlInsertIngrediente, (id_Producto, id_ingrediente))

        conexionMySQL.commit()  # Confirmar cambios
        return jsonify({"message": "Producto y sus ingredientes agregados exitosamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"message": "Error al agregar el producto", "error": str(err)}), 500
    finally:
        cursor.close()
        conexionMySQL.close()

##ruta de eliminar producto
@app.route('/productoEliminar/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    # Conexión a la base de datos MySQL
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )

    try:
        cursor = conexionMySQL.cursor()

        # Verificar si el producto existe en la base de datos
        sqlSelect = """SELECT * FROM Producto WHERE id = %s"""
        cursor.execute(sqlSelect, (id,))
        producto = cursor.fetchone()

        if not producto:
            return jsonify({"message": "Producto no encontrado"}), 404

        # Primero, eliminamos los registros dependientes en Ingredientes_Productos
        sqlDeleteIngredientesProductos = """DELETE FROM Ingredientes_Productos WHERE id_Producto = %s"""
        cursor.execute(sqlDeleteIngredientesProductos, (id,))
        
        
        # Eliminar el producto de la base de datos
        sqlDelete = """DELETE FROM Producto WHERE id = %s"""
        cursor.execute(sqlDelete, (id,))
        conexionMySQL.commit()  # Confirmar los cambios

        # Responder con un mensaje de éxito
        return jsonify({"message": "Producto eliminado exitosamente"}), 200
    except mysql.connector.Error as err:
        # Si hay un error, devolver mensaje adecuado
        return jsonify({"message": "Error al eliminar el producto", "error": str(err)}), 500
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






#Codigo maiLEN





@app.route('/cookiepedido')
def cookie_pedido():
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    cursor = conexionMySQL.cursor(dictionary=True)
    sqlSelect = """SELECT id, Nombre, Descripcion, Precio, imagen FROM Producto WHERE Nombre LIKE 'Cookie%'"""
    cursor.execute(sqlSelect)
    cookies = cursor.fetchall()
    
    cursor.close()
    conexionMySQL.close()
    return jsonify(cookies)


@app.route('/alfajorpedido')
def alfajor_pedido():
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    cursor = conexionMySQL.cursor(dictionary=True)
    sqlSelect = """SELECT id, Nombre, Descripcion, Precio, imagen FROM Producto WHERE Nombre LIKE 'Alfajor%'"""
    cursor.execute(sqlSelect)
    alfajores = cursor.fetchall()
    
    cursor.close()
    conexionMySQL.close()
    return jsonify(alfajores)


@app.route('/cupcakepedido')
def cupcake_pedido():
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )
    cursor = conexionMySQL.cursor(dictionary=True)
    sqlSelect = """SELECT id, Nombre, Descripcion, Precio, imagen FROM Producto WHERE Nombre LIKE 'Cupcake%'"""
    cursor.execute(sqlSelect)
    cupcakes = cursor.fetchall()
    
    cursor.close()
    conexionMySQL.close()
    return jsonify(cupcakes)

###############################################################################################################


@app.route('/pedidos', methods=['POST'])
def pedidos():
    
    data = request.get_json()
    print("Datos recibidos:", data)  

    estado = data.get('estado')
    usuario = data.get('usuario')
    fecha = data.get('fecha')
    metodopago = data.get('metodopago')
    ####################################
    productos_pedido = data.get('productos')


    if not all([productos_pedido, estado, usuario, fecha, metodopago]):
        return jsonify({"message": "Faltan datos"}), 400

    # Conexión a la base de datos MySQL
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )

    try:
        cursor = conexionMySQL.cursor()

        sqlInsert = """INSERT INTO Pedidos (estado, id_Usuario_rol, fecha_pedido, forma_pago) 
                       VALUES (%s, %s, %s, %s)"""
        cursor.execute(sqlInsert, (estado, usuario, fecha, metodopago))
        pedido_id = cursor.lastrowid  # Obtener el ID del nuevo pedido

        for p in productos_pedido:
            producto = p.get('producto')
            cantidad = p.get('cantidad')
            precio = p.get('precio')
            sqlInsertRol = """INSERT INTO Detalle_pedido (id_pedidos, id_producto, cantidad, precio_unitario) 
                            VALUES (%s, %s, %s, %s)"""
            cursor.execute(sqlInsertRol, (pedido_id, producto, cantidad, precio))

        conexionMySQL.commit()  # Confirmar los cambios
        print(f"Detalle pedido {id} insertado para el pedido {pedido_id}")
        response = jsonify({"message": "Pedido procesado exitosamente"})
        response.status_code = 201
    except mysql.connector.Error as err:
        print(f"Error: {err}")  # Imprime el error específico
        conexionMySQL.rollback()
        response = jsonify({"message": "Error al procesar el pedido", "error": str(err)})
        response.status_code = 400
    finally:
        cursor.close()
        conexionMySQL.close()

    return response

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


#@app.route('/detalle_pedidos')
#def detalle_pedidos():
#    page = request.args.get('page', 1, type=int)  # Obtener la página, por defecto 1
#    per_page = 5  # Número de elementos por página
#
#    conexionMySQL = mysql.connector.connect(
#        host='10.9.120.5',
#        user='kmill',
#        passwd='kmill111',
#        db='kmill'
#    )
#
#    # Consulta paginada
#    qdetalle_pedidos = """
#        SELECT * FROM Detalle_pedido
#        LIMIT %(per_page)s OFFSET %(offset)s
#    """
#    db = conexionMySQL.cursor(dictionary=True)
#    db.execute(qdetalle_pedidos, {'per_page': per_page, 'offset': (page - 1) * per_page})
#    detalle_pedidos = list(db)
#
#    # Cerramos el db y la conexión con MySQL
#    db.close()
#    conexionMySQL.close()
#
#    return jsonify({'pedidos': detalle_pedidos})






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





