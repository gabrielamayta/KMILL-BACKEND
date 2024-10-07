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



@app.route('/jsonproducto')
def producto():
    sqlSelect = """SELECT * FROM Producto"""
    cursor = conexionMySQL.cursor()
    cursor.execute(sqlSelect)
    resultadoSQL = cursor.fetchone()
    cursor.close()
    conexionMySQL.close()
    return jsonify(resultadoSQL)

@app.route('/producto/<int:id>') 
def detalle_producto(id):
    sqlSelect = """SELECT Nombre, Descripción, Precio, stock FROM Producto WHERE id = %s"""
    cursor = conexionMySQL.cursor()
    cursor.execute(sqlSelect, (id,))
    resultadoSQL = cursor.fetchone()

    cursor.close()
    conexionMySQL.close()
    return jsonify(resultadoSQL)


@app.route('/categoria/<int:id>') 
def detalle_categoria(id):
    sqlSelect = """SELECT Nombre FROM Categoria WHERE id = %s"""
    cursor = conexionMySQL.cursor()
    cursor.execute(sqlSelect, (id,))
    resultadoSQL = cursor.fetchone()

    cursor.close()
    conexionMySQL.close()
    return jsonify(resultadoSQL)

@app.route('/producto_ingrediente/<int:id>') 
def producto_ingrediente(id):
    #consulta 1
    qProducto = """SELECT Nombre FROM Producto WHERE id = %s"""
    cursor = conexionMySQL.cursor()
    cursor.execute(qProducto, (id,))
    product = cursor.fetchone()
    
   # SELECT i.Nombre from Ingrediente i 
    #INNER join Ingredientes_Productos ip ON i.id = ip.id_Ingredientes
    #INNER JOIN Producto p ON ip.id_Producto = p.id
    #WHERE ip.id_Ingredientes = 3
    #consulta 2
    qIngrediente = """ SELECT Nombre FROM Ingrediente WHERE id = %s """
    cursor.execute(qIngrediente, (id,))
    ingrediente = cursor.fetchall()
    
    cursor.close()

    resul = {  "nombre_pro": product[0],  # Nombre del producto
            "ingredientes":  [ingredient[0] for ingredient in ingrediente] }
    return jsonify(resul)

#       "Producto": product,
            #"Ingredientes": ingrediente 