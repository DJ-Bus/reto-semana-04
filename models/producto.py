"""Modelo de dominio que representa un producto del inventario."""

from __future__ import annotations


class Producto:
    """Representa un producto en el inventario.

    Attributes:
        sku: Identificador único del producto (Stock Keeping Unit).
        nombre: Nombre descriptivo del producto.
        categoria: Categoría a la que pertenece el producto.
        precio: Precio unitario del producto (>= 0).
        stock: Cantidad actual en existencia (>= 0).
        stock_minimo: Cantidad mínima requerida antes de reordenar (>= 0).
    """

    def __init__(
        self,
        sku: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int,
        stock_minimo: int,
    ) -> None:
        self.sku = sku
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.stock_minimo = stock_minimo

    # ─── Métodos de negocio ───────────────────────────────────────────────────

    def necesita_reorden(self) -> bool:
        """Retorna True si el stock actual está por debajo del mínimo."""
        return self.stock < self.stock_minimo

    def unidades_faltantes(self) -> int:
        """Retorna cuántas unidades faltan para alcanzar el stock mínimo."""
        if self.necesita_reorden():
            return self.stock_minimo - self.stock
        return 0

    def valor_inventario(self) -> float:
        """Retorna el valor total del inventario actual (precio × stock)."""
        return self.precio * self.stock

    # ─── Representación ───────────────────────────────────────────────────────

    def __str__(self) -> str:
        estado = "[REORDEN]" if self.necesita_reorden() else "[OK]"
        return (
            f"{estado} {self.sku}: {self.nombre} "
            f"- Stock: {self.stock}/{self.stock_minimo}"
        )

    def __repr__(self) -> str:
        return (
            f"Producto('{self.sku}', '{self.nombre}', '{self.categoria}', "
            f"{self.precio}, {self.stock}, {self.stock_minimo})"
        )