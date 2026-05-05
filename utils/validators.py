"""Funciones de validacion de datos para el sistema de inventario."""


def validar_sku(sku) -> bool:
    """Valida que el SKU no este vacio.

    Args:
        sku: El SKU a validar.

    Returns:
        True si el SKU es valido, False si no.
    """
    if not sku or not str(sku).strip():
        return False
    return True


def validar_precio(precio) -> bool:
    """Valida que el precio sea un numero >= 0.

    Args:
        precio: El precio a validar.

    Returns:
        True si el precio es valido, False si no.
    """
    try:
        precio_num = float(precio)
        return precio_num >= 0
    except (ValueError, TypeError):
        return False


def validar_stock(stock) -> bool:
    """Valida que el stock sea un entero >= 0.

    Args:
        stock: El valor de stock a validar.

    Returns:
        True si el stock es valido, False si no.
    """
    try:
        stock_num = int(stock)
        return stock_num >= 0
    except (ValueError, TypeError):
        return False


def validar_producto(sku, nombre, categoria, precio, stock, stock_minimo) -> tuple:
    """Valida todos los campos necesarios para crear un Producto.

    Args:
        sku: Identificador unico del producto.
        nombre: Nombre descriptivo del producto.
        categoria: Categoria del producto.
        precio: Precio unitario (debe ser un numero >= 0).
        stock: Cantidad actual en inventario (debe ser entero >= 0).
        stock_minimo: Nivel minimo de stock (debe ser entero >= 0).

    Returns:
        tuple: (es_valido: bool, mensaje_error: str | None).
            Si es valido, mensaje_error es None.
    """
    if not validar_sku(sku):
        return False, "SKU vacio o invalido"

    if not nombre or not str(nombre).strip():
        return False, "Nombre vacio"

    if not validar_precio(precio):
        return False, f"Precio invalido: {precio}"

    if not validar_stock(stock):
        return False, f"Stock invalido: {stock}"

    if not validar_stock(stock_minimo):
        return False, f"Stock minimo invalido: {stock_minimo}"

    return True, None