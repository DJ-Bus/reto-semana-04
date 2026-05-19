"""Modelo de dominio: el protagonista del inventario, el Producto."""


class Producto:
    """Representa un producto en el inventario de la tienda.

    Cada producto sabe su precio, cuántas unidades quedan y si ya
    es hora de pedir más al proveedor (spoiler: casi siempre sí).

    Attributes:
        sku: Identificador único tipo 'SKU001'. Como su CURP pero de producto.
        nombre: Nombre descriptivo, e.g. 'Laptop HP'.
        categoria: A qué familia pertenece (Electrónica, Accesorios, etc).
        precio: Precio unitario en pesos (>= 0, ojalá no sea gratis).
        stock: Cuántas unidades hay ahorita en bodega (>= 0).
        stock_minimo: Cuántas debería haber como mínimo antes de hacer pedido.
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
        """¿Ya se nos están acabando? True si el stock bajó del mínimo."""
        return self.stock < self.stock_minimo

    def unidades_faltantes(self) -> int:
        """Cuántas unidades hay que pedir para llegar al mínimo.

        Si no necesita reorden, retorna 0 (estamos bien, relax).
        """
        if self.necesita_reorden():
            return self.stock_minimo - self.stock
        return 0

    def valor_inventario(self) -> float:
        """Cuánto vale lo que tenemos en bodega (precio × stock actual)."""
        return self.precio * self.stock

    # ─── Representación ───────────────────────────────────────────────────────

    def __str__(self) -> str:
        """Versión bonita para mostrar al usuario, con etiqueta de estado."""
        estado = "[REORDEN]" if self.necesita_reorden() else "[OK]"
        return (
            f"{estado} {self.sku}: {self.nombre} "
            f"- Stock: {self.stock}/{self.stock_minimo}"
        )

    def __repr__(self) -> str:
        """Versión técnica para debugging, por si algo se rompe a las 3am."""
        return (
            f"Producto('{self.sku}', '{self.nombre}', '{self.categoria}', "
            f"{self.precio}, {self.stock}, {self.stock_minimo})"
        )