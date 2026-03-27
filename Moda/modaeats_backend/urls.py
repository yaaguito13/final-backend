from django.contrib import admin
from django.urls import path
from Moda import views
from django.conf import settings # <-- NUEVO
from django.conf.urls.static import static # <-- NUEVO

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

    # Rutas del carrito
    path('api/carrito/', views.gestionar_carrito, name='gestionar_carrito'),

    # Rutas de direcciones
    path('api/direcciones/', views.gestionar_direcciones, name='gestionar_direcciones'),
]

# <-- NUEVO: Solo para entorno de desarrollo, permite servir los archivos multimedia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)