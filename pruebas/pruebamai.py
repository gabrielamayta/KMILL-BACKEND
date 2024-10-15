#Conexión con el servidor MySQL Server


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

from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

@app.route('/detalle_pedido/<int:id>')
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


@app.route('/detalle_pedidos/<int:id_producto>')
def detalle_pedidos_por_producto(id_producto):
    conexionMySQL = mysql.connector.connect(
        host='10.9.120.5',
        user='kmill',
        passwd='kmill111',
        db='kmill'
    )

    query = """
        SELECT * FROM Detalle_pedido
        WHERE id_producto = %s
    """
    db = conexionMySQL.cursor(dictionary=True)
    db.execute(query, (id_producto,))
    detalle_pedidos = list(db)

    db.close()
    conexionMySQL.close()

    return jsonify({'pedidos': detalle_pedidos})