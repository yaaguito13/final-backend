from django.contrib import admin
from django.urls import path
from Moda import views # Importamos las vistas de tu app Moda

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas de autenticación
    path('api/registro/', views.registro_usuario, name='registro'),
    path('api/login/', views.login_usuario, name='login'),
]