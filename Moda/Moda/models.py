from django.db import models


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