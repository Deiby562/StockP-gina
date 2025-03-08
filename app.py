from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import os

app = Flask(__name__)
ARCHIVO_CSV = "Inventarioproductos.csv"

def cargar_productos():
    """
    Carga los productos desde el archivo CSV y los devuelve como una lista de diccionarios.
    """
    productos = []
    if os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode="r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo, delimiter=";")
            next(lector, None)  # Saltar la cabecera
            for linea in lector:
                if len(linea) == 5:
                    codigo, categoria, nombre, cantidad, precio = linea
                    productos.append({
                        "codigo": codigo,
                        "categoria": categoria,
                        "nombre": nombre,
                        "cantidad": int(cantidad),
                        "precio": float(precio)
                    })
    return productos

def guardar_productos(productos):
    """
    Guarda la lista de productos en el archivo CSV.
    """
    with open(ARCHIVO_CSV, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo, delimiter=";")
        escritor.writerow(["Código", "Categoría", "Nombre", "Cantidad", "Precio"])
        for p in productos:
            escritor.writerow([p["codigo"], p["categoria"], p["nombre"], p["cantidad"], f"{p['precio']:.2f}"])

@app.route('/')
def index():
    """
    Ruta principal que renderiza la página de inicio.
    """
    return render_template('index.html')

@app.route('/listar', methods=['GET'])
def listar_productos():
    """
    Devuelve la lista de productos en formato JSON.
    """
    productos = cargar_productos()  
    return jsonify(productos)  

@app.route('/agregar', methods=['POST'])
def agregar():
    """
    Agrega un nuevo producto al inventario y actualiza el archivo CSV.
    """
    codigo = request.form['codigo']
    categoria = request.form['categoria']
    nombre = request.form['nombre']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    
    productos = cargar_productos()
    productos.append({"codigo": codigo, "categoria": categoria, "nombre": nombre, "cantidad": cantidad, "precio": precio})
    guardar_productos(productos)
    
    return redirect(url_for('index'))

@app.route('/eliminar/<codigo>', methods=['POST'])
def eliminar_producto(codigo):
    """
    Elimina un producto del inventario según su código y actualiza el archivo CSV.
    """
    productos = [p for p in cargar_productos() if p['codigo'] != codigo]
    guardar_productos(productos)
    return redirect(url_for('index'))

@app.route('/modificar', methods=['POST'])
def modificar_cantidad():
    """
    Modifica la cantidad de un producto en el inventario y actualiza el CSV.
    """
    data = request.json
    codigo = data.get("codigo")
    cantidad_mod = int(data.get("cantidad"))
    
    productos = cargar_productos()
    for p in productos:
        if p['codigo'] == codigo:
            nueva_cantidad = p['cantidad'] + cantidad_mod
            if nueva_cantidad >= 0:
                p['cantidad'] = nueva_cantidad
                guardar_productos(productos)
                return jsonify({"success": True, "message": "Cantidad modificada exitosamente"})
            else:
                return jsonify({"success": False, "message": "Cantidad insuficiente"}), 400
    
    return jsonify({"success": False, "message": "Producto no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
