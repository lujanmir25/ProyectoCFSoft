#Django
from django.db import models

#Local
from bases.models import ClaseModelo, ClaseModelo2, ClaseModeloUsuario
from Clientes.models import Cliente
from productos.models import Producto


""" Encabezado de la factura """

class FacturaEnc(ClaseModelo2):
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
	fecha = models.DateTimeField(auto_now_add=True)
	sub_total = models.FloatField(default=0)
	descuento = models.FloatField(default=0)
	total = models.FloatField(default=0)

def __str__(self):
	return '{}'.format(self.id)

def save(self):
	self.total = self.sub_total - self.descuento
	super(FacturaEnc,self).save()

class Meta:
	verbose_name_plural = "Encabezado de Facturas"
	verbose_name = "Encabezado Factura"


 
""" Detalle de la factura """

class FacturaDet(ClaseModelo2):
	factura = models.ForeignKey(FacturaEnc, on_delete=models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
	cantidad = models.BigIntegerField(default=0)
	precio = models.FloatField(default=0)
	sub_total = models.FloatField(default=0)
	descuento = models.FloatField(default=0)
	total = models.FloatField(default=0)

def __str__(self):
	return '{}'.format(self.producto)	

def save(self):
	self.sub_total = float(float(int(self.cantidad)) * float(self.precio))
	self.total = self.sub_total - float(self.descuento)
	super(FacturaDet, self).save()

class Meta:
	verbose_name_plural = "Detalles Facturas"
	verbose_name = "Detalle Factura"