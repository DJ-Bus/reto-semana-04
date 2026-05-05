"""Funciones de lectura y escritura de archivos CSV para el sistema de inventario."""


def leer_inventario(ruta_archivo: str) -> list[dict]:
    """Lee el archivo de inventario CSV y retorna una lista de diccionarios.

    Cada diccionario tiene como claves los encabezados del CSV y como valores
    los datos de cada producto en formato texto. Solo se incluyen las lineas
    que tienen exactamente el mismo numero de columnas que el encabezado.

    Args:
        ruta_archivo: Ruta al archivo CSV de inventario.

    Returns:
        Lista de diccionarios con los datos crudos de cada producto.

    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta indicada.
    """
    productos_raw = []

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

        # Si el archivo esta vacio, retornar lista vacia
        if not lineas:
            return productos_raw

        encabezados = lineas[0].strip().split(",")

        # Procesar cada linea de datos (omitir encabezado)
        for linea in lineas[1:]:
            linea = linea.strip()
            if not linea:
                continue

            valores = linea.split(",")
            if len(valores) == len(encabezados):
                producto_dict = dict(zip(encabezados, valores))
                productos_raw.append(producto_dict)

    return productos_raw


def escribir_reporte(productos: list, ruta_archivo: str) -> None:
    """Escribe el reporte de productos que necesitan reorden en un archivo CSV.

    El archivo generado incluye los encabezados y una linea por cada producto
    de la lista recibida.

    Args:
        productos: Lista de objetos Producto a incluir en el reporte.
        ruta_archivo: Ruta donde se guardara el archivo CSV de salida.
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

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        # Escribir encabezados
        archivo.write(",".join(encabezados) + "\n")

        # Escribir una linea por cada producto
        for p in productos:
            linea = (
                f"{p.sku},{p.nombre},{p.categoria},{p.stock},"
                f"{p.stock_minimo},{p.unidades_faltantes()},{p.valor_inventario():.2f}"
            )
            archivo.write(linea + "\n")