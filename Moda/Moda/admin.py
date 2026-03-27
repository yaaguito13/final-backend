from django.contrib import admin
# Añadimos Pedido e ItemPedido a la lista de importaciones
from .models import Categoria, Marca, Producto, Direccion, Favorito, Carrito, ItemCarrito, Pedido, ItemPedido

admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Producto)
admin.site.register(Direccion)
admin.site.register(Favorito)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
# Registramos los dos nuevos
admin.site.register(Pedido)
admin.site.register(ItemPedido)