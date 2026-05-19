"""Validadores de datos para el inventario.

Aquí checamos que los datos no vengan chuecos antes de crear un Producto.
Más vale prevenir que debuggear a las 2am.
"""


def validar_sku(sku) -> bool:
    """Verifica que el SKU no venga vacío o puro espacio en blanco.

    Args:
        sku: El identificador a revisar.

    Returns:
        True si tiene algo útil, False si es None, vacío o puro aire.
    """
    if not sku or not str(sku).strip():
        return False
    return True


def validar_precio(precio) -> bool:
    """Checa que el precio sea un número y que no sea negativo.

    Porque nadie vende laptops a -$5000... aunque sería buen negocio para el comprador.

    Args:
        precio: El valor a validar (puede venir como string del CSV).

    Returns:
        True si se puede convertir a float y es >= 0.
    """
    try:
        precio_num = float(precio)
        return precio_num >= 0
    except (ValueError, TypeError):
        return False


def validar_stock(stock) -> bool:
    """Verifica que el stock sea un entero no negativo.

    No puedes tener -3 laptops en bodega... ¿o sí?

    Args:
        stock: Valor a validar (puede venir como string del CSV).

    Returns:
        True si es un entero >= 0, False para cualquier cosa rara.
    """
    try:
        stock_num = int(stock)
        return stock_num >= 0
    except (ValueError, TypeError):
        return False


def validar_producto(sku, nombre, categoria, precio, stock, stock_minimo) -> tuple:
    """Pasa todos los campos por el filtro antes de crear un Producto.

    Revisa cada campo uno por uno y si algo falla, retorna cuál fue
    el problema para que el usuario sepa qué corregir.

    Args:
        sku: Identificador único del producto.
        nombre: Nombre descriptivo.
        categoria: Categoría a la que pertenece.
        precio: Precio unitario (debe ser número >= 0).
        stock: Cantidad actual (entero >= 0).
        stock_minimo: Nivel mínimo aceptable (entero >= 0).

    Returns:
        Tupla (es_valido, mensaje_error). Si todo bien, el error es None.
    """
    if not validar_sku(sku):
        return False, "SKU vacio o invalido"

    if not nombre or not str(nombre).strip():
        return False, "Nombre vacio"

    # Categoría también es obligatoria, no queremos productos huérfanos
    if not categoria or not str(categoria).strip():
        return False, "Categoria vacia"

    if not validar_precio(precio):
        return False, f"Precio invalido: {precio}"

    if not validar_stock(stock):
        return False, f"Stock invalido: {stock}"

    if not validar_stock(stock_minimo):
        return False, f"Stock minimo invalido: {stock_minimo}"

    return True, None