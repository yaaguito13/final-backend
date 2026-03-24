from django.contrib import admin
from django.urls import path
from Moda import views
from django.conf import settings # <-- NUEVO
from django.conf.urls.static import static # <-- NUEVO

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/registro/', views.registro_usuario, name='registro'),
    path('api/login/', views.login_usuario, name='login'),
    path('api/marcas/', views.lista_marcas, name='marcas'),
    path('api/productos/', views.catalogo_productos, name='productos'),
]

# <-- NUEVO: Solo para entorno de desarrollo, permite servir los archivos multimedia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)