# Sistema de Inventario Modular

> **Reto Semana 4 — Programación para Ciencia de Datos**  
> Instituto Politécnico Nacional · ESCOM · Semestre Febrero-Julio 2026

---

## Descripción

Sistema modular en Python 3.11 que automatiza la gestión de inventario para una cadena de tiendas de tecnología. Lee un archivo CSV con el estado actual del inventario, identifica los productos cuyo stock se encuentra por debajo del mínimo requerido y genera un reporte CSV ordenado por urgencia de reorden.

El proyecto aplica principios de **código limpio**, **modularidad** y **separación de responsabilidades**.

---

## Estructura del Proyecto

```
reto-semana-04/
├── main.py                    # Punto de entrada — orquesta todo el sistema
├── README.md                  # Documentación del proyecto
├── .gitignore                 # Archivos excluidos del control de versiones
│
├── models/                    # Clases de dominio
│   ├── __init__.py
│   └── producto.py            # Clase Producto con métodos de negocio
│
├── utils/                     # Utilidades reutilizables
│   ├── __init__.py
│   ├── io.py                  # Funciones de lectura y escritura CSV
│   └── validators.py          # Funciones de validación de datos
│
├── data/                      # Datos de entrada
│   └── inventario.csv         # Inventario con SKU, precios y stocks
│
└── outputs/                   # Resultados generados
    └── reporte_inventario.csv # Reporte de productos que necesitan reorden
```

---

## Cómo Ejecutar

```bash
# Desde la raíz del proyecto
python main.py
```

El programa imprime en consola los productos que necesitan reorden y guarda el reporte en `outputs/reporte_inventario.csv`.

---

## Entrada — `data/inventario.csv`

Archivo CSV con **una fila por producto** (sin duplicados). Columnas requeridas:

| Columna | Tipo | Descripción | Ejemplo |
|---|---|---|---|
| `sku` | texto | Identificador único | `SKU001` |
| `nombre` | texto | Nombre del producto | `Laptop HP` |
| `categoria` | texto | Categoría | `Electronica` |
| `precio` | decimal | Precio unitario ≥ 0 | `15000.00` |
| `stock` | entero | Cantidad actual ≥ 0 | `5` |
| `stock_minimo` | entero | Mínimo antes de reordenar ≥ 0 | `10` |

Las líneas con datos inválidos (precio no numérico, stock no numérico, columnas faltantes o extra) **se ignoran automáticamente** mostrando una advertencia.

---

## Salida — `outputs/reporte_inventario.csv`

Contiene **únicamente** los productos con `stock < stock_minimo`, ordenados por `unidades_faltantes` de forma **descendente** (mayor urgencia primero).

| Columna | Descripción |
|---|---|
| `sku` | Identificador del producto |
| `nombre` | Nombre del producto |
| `categoria` | Categoría |
| `stock_actual` | Stock en existencia |
| `stock_minimo` | Mínimo requerido |
| `unidades_faltantes` | `stock_minimo − stock_actual` |
| `valor_inventario` | `precio × stock_actual` (2 decimales) |

### Ejemplo de salida

```csv
sku,nombre,categoria,stock_actual,stock_minimo,unidades_faltantes,valor_inventario
SKU002,Mouse Logitech,Accesorios,3,15,12,1050.00
SKU005,Audifonos Sony,Accesorios,2,10,8,2400.00
SKU001,Laptop HP,Electronica,5,10,5,75000.00
SKU007,SSD 1TB,Almacenamiento,0,5,5,0.00
```

---

## Requisitos

- Python **3.11** o superior
- Sin dependencias externas (solo biblioteca estándar)

---

## Autor

**Diego Jehu Bustamante Villanueva**  
Licenciatura en Ciencia de Datos — Tercer Semestre  
Escuela Superior de Cómputo (ESCOM) — Instituto Politécnico Nacional (IPN)
