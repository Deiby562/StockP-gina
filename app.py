from flask import Flask, render_template, request, redirect, url_for
from inventario import Inventario, Producto

app = Flask(__name__)
inventario = Inventario()

@app.route("/")
def index():
    productos = inventario.obtener_productos()
    return render_template("index.html", productos=productos)

@app.route("/agregar", methods=["POST"])
def agregar_producto():
    codigo = request.form["codigo"]
    categoria = request.form["categoria"]
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    precio = request.form["precio"]

    nuevo_producto = Producto(codigo, categoria, nombre, cantidad, precio)
    inventario.agregar_producto(nuevo_producto)

    return redirect(url_for("index"))

@app.route("/buscar", methods=["POST"])
def buscar_producto():
    criterio = request.form["criterio"]
    productos_encontrados = inventario.buscar_producto(criterio)
    return render_template("index.html", productos=productos_encontrados)

@app.route("/eliminar/<codigo>")
def eliminar_producto(codigo):
    if inventario.eliminar_producto(codigo):
        mensaje = "Producto eliminado correctamente."
    else:
        mensaje = "Producto no encontrado."
    return redirect(url_for("index"))

@app.route("/modificar", methods=["POST"])
def modificar_cantidad():
    codigo = request.form["codigo"]
    cantidad_mod = request.form["cantidad_mod"]

    if inventario.modificar_cantidad(codigo, cantidad_mod):
        mensaje = "Cantidad modificada con éxito."
    else:
        mensaje = "Error al modificar cantidad."

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
