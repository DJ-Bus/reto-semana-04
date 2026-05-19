"""Modelos de dominio — aquí viven las clases que representan cosas del negocio."""
from .producto import Producto

# Le aviso a Python qué cosas quiero compartir, así nadie me regaña por "import sin usar"
__all__ = ["Producto"]