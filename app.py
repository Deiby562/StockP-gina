from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import os

app = Flask(__name__)
ARCHIVO_CSV = "Inventarioproductos.csv"

def cargar_productos():
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
    with open(ARCHIVO_CSV, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo, delimiter=";")
        escritor.writerow(["Código", "Categoría", "Nombre", "Cantidad", "Precio"])
        for p in productos:
            escritor.writerow([p["codigo"], p["categoria"], p["nombre"], p["cantidad"], f"{p['precio']:.2f}"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listar', methods=['GET'])
def listar_productos():
    productos = cargar_productos()  
    return jsonify(productos)  

@app.route('/agregar', methods=['POST'])
def agregar():
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
    productos = [p for p in cargar_productos() if p['codigo'] != codigo]
    guardar_productos(productos)
    return redirect(url_for('index'))

@app.route('/modificar/<codigo>', methods=['POST'])
def modificar_cantidad(codigo):
    cantidad_nueva = int(request.form['cantidad'])
    productos = cargar_productos()
    for p in productos:
        if p['codigo'] == codigo:
            p['cantidad'] = cantidad_nueva
            break
    guardar_productos(productos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
