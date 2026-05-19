"""Utilidades del inventario — validadores, lectura y escritura de archivos."""
from .validators import validar_sku, validar_precio, validar_stock
from .io import leer_inventario, escribir_reporte

# La lista de "lo que sí se puede usar desde afuera", y de paso calla los warnings
__all__ = [
    "validar_sku",
    "validar_precio",
    "validar_stock",
    "leer_inventario",
    "escribir_reporte",
]