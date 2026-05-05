#!/usr/bin/env python3
"""Sistema de Inventario Modular — punto de entrada principal.

Lee un inventario desde un CSV, identifica los productos que necesitan
reorden (stock < stock_minimo) y genera un reporte ordenado por unidades
faltantes de forma descendente.

Uso:
    python main.py
"""

from models.producto import Producto
from utils.validators import validar_producto
from utils.io import leer_inventario, escribir_reporte

# ─── Rutas de archivos ────────────────────────────────────────────────────────
ARCHIVO_INVENTARIO = "data/inventario.csv"
ARCHIVO_REPORTE = "outputs/reporte_inventario.csv"


def crear_productos(datos_raw: list[dict]) -> list[Producto]:
    """Convierte una lista de diccionarios crudos en objetos Producto.

    Los registros invalidos se omiten mostrando un mensaje de advertencia.

    Args:
        datos_raw: Lista de diccionarios con datos de productos en texto plano.

    Returns:
        Lista de objetos Producto validos.
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
    """Retorna solo los productos cuyo stock esta por debajo del minimo.

    Args:
        productos: Lista completa de objetos Producto.

    Returns:
        Lista filtrada de productos que necesitan reorden.
    """
    return [p for p in productos if p.necesita_reorden()]


def ordenar_por_faltantes(productos: list[Producto]) -> list[Producto]:
    """Ordena los productos por unidades faltantes de forma descendente.

    Args:
        productos: Lista de productos que necesitan reorden.

    Returns:
        Lista ordenada (mayor faltante primero).
    """
    return sorted(productos, key=lambda p: p.unidades_faltantes(), reverse=True)


def main() -> None:
    """Orquesta la ejecucion completa del sistema de inventario."""
    print("=" * 50)
    print("SISTEMA DE INVENTARIO - Reporte de Reorden")
    print("=" * 50)

    datos_raw = leer_inventario(ARCHIVO_INVENTARIO)
    productos = crear_productos(datos_raw)
    necesitan_reorden = filtrar_necesitan_reorden(productos)
    necesitan_reorden = ordenar_por_faltantes(necesitan_reorden)

    print("\nPRODUCTOS QUE NECESITAN REORDEN:")
    for p in necesitan_reorden:
        print(p)

    escribir_reporte(necesitan_reorden, ARCHIVO_REPORTE)
    print(f"\nReporte guardado en: {ARCHIVO_REPORTE}")


if __name__ == "__main__":
    main()