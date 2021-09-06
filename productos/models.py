'''Modelo de productos'''
from django.db import models

from bases.models import ClaseModelo
from django.utils import timezone

class Producto(ClaseModelo):
    """Modelo de producto"""
    #product_id = models.CharField(unique=True, max_length=50)

    product_name = models.CharField(max_length=50)

    unidad_medida = models.CharField(max_length=5)

    categoria = models.CharField(max_length=30)
    
    marca = models.CharField(max_length=30)
    
    precio_venta = models.IntegerField(blank=False)

    def __str__(self):
        return '{}'.format(self.product_name)
        #return f'{self.name}, {self.checkIn}, {self.checkOut}, {self.occupant}'

    class Meta:
        verbose_name_plural = "Productos"
