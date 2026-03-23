from django.contrib import admin
# Importamos TODOS nuestros modelos
from .models import Categoria, Marca, Producto, Direccion, Favorito, Carrito, ItemCarrito

# Registramos los modelos de catálogo (los que ya teníamos)
admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Producto)

# Registramos los nuevos modelos de usuario y compras
admin.site.register(Direccion)
admin.site.register(Favorito)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)