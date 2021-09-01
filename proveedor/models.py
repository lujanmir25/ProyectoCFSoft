from django.db import models
from bases.models import ClaseModelo, ClaseModeloUsuario


class Proveedor(ClaseModelo, ClaseModeloUsuario):
    """cedula = models.CharField(max_length=50, blank=True)
    ruc = models.CharField(max_length=50, blank=True)
    nombre = models.CharField(max_length=50, blank=True)
    apellido = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    direccion = models.CharField(max_length=50, blank=True)"""

    def __str__(self):
        return '{}'.format(self.cedula)

    class Meta:
        verbose_name_plural = 'Proveedores'