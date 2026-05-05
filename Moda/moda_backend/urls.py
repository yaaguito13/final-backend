from django.contrib import admin
from django.urls import path
from Moda import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de autenticación
    path('api/registro/', views.registro_usuario, name='registro'),
    path('api/login/', views.login_usuario, name='login'),

    # Rutas de Catálogo y Marcas
    path('api/marcas/', views.lista_marcas, name='marcas'),
    path('api/productos/', views.catalogo_productos, name='productos'),

    # Ruta de Detalle de un producto (Path Param)
    path('api/productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),

    # Rutas de favoritos
    path('api/favoritos/', views.gestionar_favoritos, name='gestionar_favoritos'),
    path('api/favoritos/<int:producto_id>/', views.eliminar_favorito, name='eliminar_favorito'),

    # Ruta del carrito
    path('api/carrito/', views.gestionar_carrito, name='gestionar_carrito'),
    path('api/carrito/<int:item_id>/', views.modificar_item_carrito, name='modificar_item_carrito'),

    # Ruta de direcciones
    path('api/direcciones/', views.gestionar_direcciones, name='gestionar_direcciones'),

    # Ruta de categorias
    path('api/categorias/', views.lista_categorias, name='categorias'),

    # Ruta de perfil
    path('api/perfil/', views.perfil_usuario, name='perfil'),

    # Rutas de pedidos (CHECKOUT)
    path('api/pedidos/checkout/', views.checkout_pedido, name='checkout'),
    path('api/pedidos/', views.historial_pedidos, name='historial_pedidos'),
]

# <-- NUEVO: Solo para entorno de desarrollo, permite servir los archivos multimedia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)