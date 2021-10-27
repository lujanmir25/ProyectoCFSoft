'''Modelo de productos'''
from django.db import models

from bases.models import ClaseModelo
from django.utils import timezone


class Producto(ClaseModelo):
    """Modelo de producto"""
    codigo = models.CharField(max_length=20, unique=True, blank=False, default='cod_def' )
    product_name = models.CharField(max_length=50)

    unidad_medida = models.CharField(max_length=5)

    categoria = models.CharField(max_length=30)

    marca = models.CharField(max_length=30)

    precio = models.FloatField(default=0)
    existencia = models.FloatField(default=0)

    ultima_compra = models.DateField(null=True, blank=True)

    descripcion = models.CharField(max_length=200,default='.')

    def __str__(self):
        return '{}'.format(self.product_name)
        # return f'{self.name}, {self.checkIn}, {self.checkOut}, {self.occupant}'

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Producto,self).save()

    class Meta:
        verbose_name_plural = "Productos"
        """unique_together = ('codigo')"""
