import pandas as pd
import sqlite3
from flask import Flask, jsonify
import os

app = Flask(__name__)

def inicializar_bd():
    """
    Inicializa la base de datos leyendo un archivo Excel y creando una tabla SQL.
    """
    try:
        # Define la ruta del archivo Excel
        ruta_archivo = r'C:\Users\Rolando Gonzàlez\Desktop\tarea_3'
        
        # Verifica si el archivo existe
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo no se encontró en la ruta especificada: {ruta_archivo}")
        
        # Lee el archivo Excel
        df = pd.read_excel(ruta_archivo)
        
        # Conecta a la base de datos SQLite
        conn = sqlite3.connect('ventas.db')
        
        # Crea la tabla 'pedidos' a partir del DataFrame
        df.to_sql('pedidos', conn, if_exists='replace', index=False)
        
        conn.close()
        print("Base de datos inicializada exitosamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")

# Inicializa la base de datos al inicio
inicializar_bd()

def obtener_conexion_bd():
    """
    Establece y retorna una conexión a la base de datos.
    """
    return sqlite3.connect('ventas.db')

@app.route('/pedidos/<order_id>', methods=['GET'])
def obtener_pedido(order_id):
    """
    Maneja la solicitud GET para obtener un pedido específico.
    """
    conn = obtener_conexion_bd()
    try:
        # Ejecuta la consulta SQL para obtener el pedido
        resultado = conn.execute("SELECT * FROM pedidos WHERE [Order ID] = ?", (order_id,)).fetchone()
        
        if resultado:
            # Obtiene los nombres de las columnas
            columnas = [description[0] for description in conn.execute("SELECT * FROM pedidos LIMIT 1").description]
            # Convierte el resultado a un diccionario
            pedido = dict(zip(columnas, resultado))
            return jsonify(pedido)
        else:
            return jsonify({"error": "Pedido no encontrado"}), 404
    finally:
        conn.close()

@app.route('/cliente/<customer_id>', methods=['GET'])
def obtener_cliente(customer_id):
    """
    Maneja la solicitud GET para obtener pedidos de un cliente específico.
    """
    conn = obtener_conexion_bd()
    try:
        # Ejecuta la consulta SQL para obtener los pedidos del cliente
        resultados = conn.execute("SELECT * FROM pedidos WHERE [Customer ID] = ?", (customer_id,)).fetchall()
        
        if resultados:
            # Obtiene los nombres de las columnas
            columnas = [description[0] for description in conn.execute("SELECT * FROM pedidos LIMIT 1").description]
            # Convierte los resultados a una lista de diccionarios
            pedidos = [dict(zip(columnas, resultado)) for resultado in resultados]
            return jsonify(pedidos)
        else:
            return jsonify({"error": "Pedidos no encontrados"}), 404
    finally:
        conn.close()

if __name__ == '__main__':
    # Inicia la aplicación Flask
    app.run(debug=False, port=5000)
    
    
    
    
    
    