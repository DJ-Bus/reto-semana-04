#!/usr/bin/env python3
"""Sistema de Inventario Modular — punto de entrada principal.

Lee un inventario desde CSV, detecta productos con stock bajo
y genera un reporte ordenado por urgencia. Básicamente, el chismoso
que le dice al gerente qué falta en la bodega.

Uso:
    python main.py
"""

from models.producto import Producto
from utils.validators import validar_producto
from utils.io import leer_inventario, escribir_reporte

# Aquí viven los archivos de entrada y salida, no los muevas o todo explota
ARCHIVO_INVENTARIO = "data/inventario.csv"
ARCHIVO_REPORTE = "outputs/reporte_inventario.csv"


def crear_productos(datos_raw: list[dict]) -> list[Producto]:
    """Toma los diccionarios crudos del CSV y los convierte en objetos Producto.

    Si un registro viene mal (precio raro, stock negativo, etc),
    lo ignora con un mensaje de advertencia en vez de tronar todo.

    Args:
        datos_raw: Lista de diccionarios con datos en texto plano.

    Returns:
        Lista de Productos que pasaron la validación sin problemas.
    """
    productos = []
    for datos in datos_raw:
        es_valido, error = validar_producto(
            datos.get("sku"),
            datos.get("nombre"),
            datos.get("categoria"),
            datos.get("precio"),
            datos.get("stock"),
            datos.get("stock_minimo"),
        )
        if not es_valido:
            print(f"Advertencia: Ignorando registro invalido - {error}")
            continue

        producto = Producto(
            sku=datos["sku"],
            nombre=datos["nombre"],
            categoria=datos["categoria"],
            precio=float(datos["precio"]),
            stock=int(datos["stock"]),
            stock_minimo=int(datos["stock_minimo"]),
        )
        productos.append(producto)

    return productos


def filtrar_necesitan_reorden(productos: list[Producto]) -> list[Producto]:
    """Separa los productos que andan escasos de stock.

    Args:
        productos: Todos los productos del inventario.

    Returns:
        Solo los que tienen stock por debajo del mínimo (los urgentes).
    """
    return [p for p in productos if p.necesita_reorden()]


def ordenar_por_faltantes(productos: list[Producto]) -> list[Producto]:
    """Ordena por unidades faltantes de mayor a menor.

    Los que necesitan más unidades van primero, para que el
    departamento de compras sepa qué pedir con más urgencia.

    Args:
        productos: Productos que necesitan reorden.

    Returns:
        La misma lista pero ordenada (el más urgente primero).
    """
    return sorted(productos, key=lambda p: p.unidades_faltantes(), reverse=True)


def main() -> None:
    """Orquesta todo el flujo: leer, validar, filtrar, ordenar y reportar."""
    print("=" * 50)
    print("SISTEMA DE INVENTARIO - Reporte de Reorden")
    print("=" * 50)

    # 1. Leer el CSV con los datos crudos
    print(f"\nLeyendo inventario de: {ARCHIVO_INVENTARIO}")
    datos_raw = leer_inventario(ARCHIVO_INVENTARIO)
    print(f"Registros leidos: {len(datos_raw)}")

    # 2. Convertir a objetos Producto (los inválidos se ignoran solitos)
    productos = crear_productos(datos_raw)
    print(f"Productos validos: {len(productos)}")

    # 3. Filtrar los que andan cortos de stock
    necesitan_reorden = filtrar_necesitan_reorden(productos)
    print(f"Productos que necesitan reorden: {len(necesitan_reorden)}")

    # 4. Ordenar por urgencia (más faltantes primero)
    necesitan_reorden = ordenar_por_faltantes(necesitan_reorden)

    # 5. Mostrar el reporte en consola
    print("\n" + "-" * 50)
    print("PRODUCTOS QUE NECESITAN REORDEN:")
    print("-" * 50)
    for p in necesitan_reorden:
        print(p)

    # 6. Guardar el reporte en CSV
    escribir_reporte(necesitan_reorden, ARCHIVO_REPORTE)
    print(f"\nReporte guardado en: {ARCHIVO_REPORTE}")

    print("\n" + "=" * 50)
    print("Proceso completado exitosamente")
    print("=" * 50)


if __name__ == "__main__":
    main()