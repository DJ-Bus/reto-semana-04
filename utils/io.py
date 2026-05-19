"""Funciones de lectura y escritura CSV para el inventario.

Todo lo que toca archivos vive aquí. Si algo no lee o no escribe bien,
ya sabes dónde buscar el culpable.
"""

from pathlib import Path


def leer_inventario(ruta_archivo: str) -> list[dict]:
    """Lee el CSV del inventario y lo convierte en una lista de diccionarios.

    Cada diccionario tiene como llaves los encabezados del CSV y como
    valores los datos en texto (después los validamos y convertimos).
    Las líneas con columnas de más o de menos se ignoran en silencio.

    Args:
        ruta_archivo: Ruta al archivo CSV, e.g. 'data/inventario.csv'.

    Returns:
        Lista de diccionarios con los datos crudos de cada producto.

    Raises:
        FileNotFoundError: Si el archivo no existe (obvio, no somos magos).
    """
    productos_raw = []

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

        # Archivo vacío = nada que hacer, nos vamos temprano a casa
        if not lineas:
            return productos_raw

        encabezados = lineas[0].strip().split(",")

        # Recorrer cada línea saltando el encabezado
        for linea in lineas[1:]:
            linea = linea.strip()
            if not linea:
                continue

            valores = linea.split(",")
            # Solo aceptamos líneas con el número exacto de columnas
            if len(valores) == len(encabezados):
                producto_dict = dict(zip(encabezados, valores))
                productos_raw.append(producto_dict)

    return productos_raw


def escribir_reporte(productos: list, ruta_archivo: str) -> None:
    """Genera el CSV de reporte con los productos que necesitan reorden.

    El archivo incluye encabezados y una línea por producto,
    con datos calculados como unidades faltantes y valor del inventario.

    Args:
        productos: Lista de objetos Producto a reportar.
        ruta_archivo: Dónde guardar el CSV de salida.
    """
    encabezados = [
        "sku",
        "nombre",
        "categoria",
        "stock_actual",
        "stock_minimo",
        "unidades_faltantes",
        "valor_inventario",
    ]

    # Por si la carpeta outputs/ todavía no existe, la creo y así no me truena nada
    Path(ruta_archivo).parent.mkdir(parents=True, exist_ok=True)

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(",".join(encabezados) + "\n")

        for p in productos:
            linea = (
                f"{p.sku},{p.nombre},{p.categoria},{p.stock},"
                f"{p.stock_minimo},{p.unidades_faltantes()},{p.valor_inventario():.2f}"
            )
            archivo.write(linea + "\n")