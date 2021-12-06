'''Modelo de productos'''
from django.db import models

from bases.models import ClaseModelo,ClaseModelo2
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        return '{}'.format(self.id)
        # return f'{self.name}, {self.checkIn}, {self.checkOut}, {self.occupant}'

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Producto,self).save()

    class Meta:
        verbose_name_plural = "Productos"
        """unique_together = ('codigo')"""


class AjusteInventario(Producto):
    """Modelo de Ajuste inventario"""


    def __str__(self):
        #return '{}'.format(self.product_name)
        return f'{self.product_name}, {self.existencia}'

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Producto,self).save()

    class Meta:
        verbose_name_plural = "Productos Ajustados"


class NotaCredito(ClaseModelo2):
    no_factura = models.CharField(max_length=100, default=0)
    producto = models.CharField(max_length=50, null=True)
    descripcion = models.CharField(max_length=200,default='.')
    cantidad = models.BigIntegerField(default=0)
    precio = models.FloatField(default=0)
    total = models.FloatField(default=0) 
    gravada = models.FloatField(default=0)
    iva = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.id)

    def save(self):
        super(NotaCredito,self).save()

    class Meta:
        verbose_name_plural = "Notas de Creditos"

