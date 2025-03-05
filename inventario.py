import os
import csv
import json

class Producto:
    def __init__(self, codigo, categoria, nombre, cantidad, precio):
        self.codigo = str(codigo).strip()
        self.categoria = str(categoria).strip()
        self.nombre = str(nombre).strip()
        self.cantidad = self._convertir_entero(cantidad)
        self.precio = self._convertir_float(precio)

    def __str__(self):
        return (f"Código: {self.codigo}\n"
                f"Nombre: {self.nombre}\n"
                f"Categoría: {self.categoria}\n"
                f"Cantidad: {self.cantidad} unidades\n"
                f"Precio: ${self.precio:.3f}")

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "categoria": self.categoria,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def _convertir_entero(valor):
        try:
            return int(valor)
        except ValueError:
            return 0

    @staticmethod
    def _convertir_float(valor):
        try:
            return float(str(valor).replace(",", ".").strip())
        except ValueError:
            return 0.0


class Inventario:
    def __init__(self, archivo_csv="Inventarioproductos.csv"):
        self.archivo_csv = archivo_csv
        self.productos = {}
        self.cargar_desde_csv()

    def agregar_producto(self, producto):
        self.productos[producto.codigo] = producto
        self.guardar_en_csv()

    def buscar_producto(self, criterio):
        criterio = criterio.strip().lower()
        resultados = [
            p for p in self.productos.values()
            if (p.codigo.lower() == criterio or
                criterio in p.nombre.lower() or 
                criterio in p.categoria.lower())
        ]
        if resultados:
            print("\n✅ Productos encontrados:\n")
            for producto in resultados:
                print(producto)
                print("\n" + "-" * 50 + "\n")
        else:
            print("⚠️ Producto no encontrado.")

    def listar_productos(self):
        if not self.productos:
            print("⚠️ No hay productos en el inventario.")
            return
        
        print("\n📦 Inventario de Productos:\n")
        print(f"{'Código':<10}{'Categoría':<15}{'Nombre':<20}{'Cantidad':<10}{'Precio':<10}")
        print("-" * 65)

        for producto in self.productos.values():
            print(f"{producto.codigo:<10}{producto.categoria:<15}{producto.nombre:<20}{producto.cantidad:<10}{producto.precio:<10.2f}")

    def eliminar_producto(self, codigo):
        if codigo in self.productos:
            del self.productos[codigo]
            self.guardar_en_csv()
            return True
        return False

    def obtener_productos(self):
        return [p.to_dict() for p in self.productos.values()]

    def modificar_cantidad(self, codigo, cantidad_mod):
        if codigo in self.productos:
            cantidad_mod = Producto._convertir_entero(cantidad_mod)
            if cantidad_mod == 0:
                return False

            nueva_cantidad = self.productos[codigo].cantidad + cantidad_mod

            if nueva_cantidad < 0:
                return False

            self.productos[codigo].cantidad = nueva_cantidad
            self.guardar_en_csv()
            return True
        return False

    def modificar_precio(self, codigo, nuevo_precio):
        if codigo in self.productos:
            nuevo_precio = Producto._convertir_float(nuevo_precio)
            if nuevo_precio <= 0:
                return False
            self.productos[codigo].precio = nuevo_precio
            self.guardar_en_csv()
            return True
        return False

    def cargar_desde_csv(self):
        if not os.path.exists(self.archivo_csv):
            print("⚠️ Archivo CSV no encontrado. Se creará uno nuevo.")
            return
        try:
            with open(self.archivo_csv, mode="r", encoding="utf-8") as archivo:
                print("📂 Cargando CSV...")  
                print("Productos antes de cargar:", len(self.productos))  
                lector = csv.reader(archivo, delimiter=";")
                next(lector, None)
                for linea in lector:
                    if len(linea) == 5:
                        codigo, categoria, nombre, cantidad, precio = linea
                        self.productos[codigo] = Producto(codigo, categoria, nombre, cantidad, precio)
                print("Productos cargados:", len(self.productos))
        except Exception as e:
            print(f"❌ Error al cargar el CSV: {e}")

    def guardar_en_csv(self):
        try:
            with open(self.archivo_csv, mode="w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo, delimiter=";")
                escritor.writerow(["Código", "Categoría", "Nombre", "Cantidad", "Precio"])
                for producto in sorted(self.productos.values(), key=lambda x: x.codigo):
                    escritor.writerow([producto.codigo, producto.categoria, producto.nombre, producto.cantidad, f"{producto.precio:.3f}"])
        except Exception as e:
            print(f"❌ Error al guardar el CSV: {e}")
