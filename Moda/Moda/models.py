from django.db import models

from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=8, decimal_places=2)

    # Relación 1:N (Una marca tiene muchos productos)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='productos')

    # Relación N:N (Un producto puede estar en varias categorías)
    categorias = models.ManyToManyField(Categoria, related_name='productos')

    def __str__(self):
        return self.nombre


# --- MODELOS DE USUARIO Y COMPRAS ---

class Direccion(models.Model):
    """Guarda las direcciones de envío del usuario"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='direcciones')
    titulo = models.CharField(max_length=50, help_text="Ej: Casa, Trabajo")
    calle = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"


class Favorito(models.Model):
    """Lista de deseos de los usuarios"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto.nombre} - Favorito de {self.usuario.username}"


class Carrito(models.Model):
    """El carrito de compras activo de un usuario"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class ItemCarrito(models.Model):
    """Los productos individuales dentro de un carrito, con su talla y color"""
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    # Opciones que vimos en tu diseño
    talla = models.CharField(max_length=10, blank=True, null=True)  # Ej: S, M, L
    color = models.CharField(max_length=30, blank=True, null=True)  # Ej: Negro, Blanco

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en {self.carrito}"