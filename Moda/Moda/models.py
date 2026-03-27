from django.db import models

from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)  # <-- NUEVO

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='marcas/', null=True, blank=True) # <-- NUEVO

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='productos')
    categorias = models.ManyToManyField(Categoria, related_name='productos')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True) # <-- NUEVO

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


# --- MODELOS DE PEDIDOS (CHECKOUT) ---

class Pedido(models.Model):
    """Guarda el ticket de compra definitivo de un usuario"""

    # Opciones de estado para la pantalla de "Mis Pedidos"
    ESTADOS = (
        ('Procesando', 'Procesando'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Procesando')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username} ({self.estado})"


class ItemPedido(models.Model):
    """La foto fija de los productos que se compraron en ese pedido"""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    # Usamos SET_NULL por si en el futuro borras una camiseta del catálogo, que el ticket de compra no desaparezca
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)

    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)  # El precio que costaba ese día
    talla = models.CharField(max_length=10, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        nombre = self.producto.nombre if self.producto else 'Producto descatalogado'
        return f"{self.cantidad}x {nombre} en Pedido #{self.pedido.id}"