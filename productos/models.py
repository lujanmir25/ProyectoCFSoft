'''Modelo de productos'''
from django.db import models

from bases.models import ClaseModelo
from django.utils import timezone

class Producto(ClaseModelo):
    """Modelo de producto"""
    #product_id = models.CharField(unique=True, max_length=50)

    product_name = models.CharField(max_length=50)

    stock_actual = models.IntegerField(blank=False)
    stock_minimo = models.IntegerField(default=10, blank=False)
    unidad_medida = models.CharField(max_length=5)

    fecha_ingreso = models.DateTimeField(default=timezone.now)
    fecha_caducidad = models.DateField()

    categoria = models.CharField(max_length=30)
    marca = models.CharField(max_length=30)

    def __str__(self):
        return '{}'.format(self.product_name) #, {self.stock_actual}, {self.stock_minimo}, {self.unidad_medida},{self.fecha_ingreso}, {self.fecha_caducidad},{self.categoria},{self.marca}'
        #return f'{self.name}, {self.checkIn}, {self.checkOut}, {self.occupant}'

    class Meta:
        verbose_name_plural = "Productos"
