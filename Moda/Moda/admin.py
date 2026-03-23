from django.contrib import admin
from .models import Categoria, Marca, Producto

# Registramos los modelos para que aparezcan en el panel web
admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Producto)
