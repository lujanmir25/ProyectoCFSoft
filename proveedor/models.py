from django.db import models
# Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from bases.models import ClaseModelo, ClaseModeloUsuario
from productos.models import Producto


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


class ComprasEnc(ClaseModelo):
    fecha_compra = models.DateField(null=True, blank=True)
    observacion = models.TextField(blank=True, null=True)
    no_factura = models.CharField(max_length=100)
    fecha_factura = models.DateField()
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.observacion)

    def save(self, **kwargs):
        self.observacion = self.observacion.upper()
        if self.sub_total == None  or self.descuento == None:
            self.sub_total = 0
            self.descuento = 0

        self.total = self.sub_total - self.descuento
        super(ComprasEnc, self).save()

    class Meta:
        verbose_name_plural = "Encabezado Compras"
        verbose_name = "Encabezado Compra"


class ComprasDet(ClaseModelo):
    compra = models.ForeignKey(ComprasEnc, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)
    precio_prv = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)
    costo = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.producto)

    def save(self, **kwargs):
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio_prv))
        self.total = self.sub_total - float(self.descuento)
        super(ComprasDet, self).save()

    class Meta:
        verbose_name_plural = "Detalles Compras"
        verbose_name = "Detalle Compra"


@receiver(post_delete, sender=ComprasDet)
def detalle_compra_borrar(sender, instance, **kwargs):
    id_producto = instance.producto.id
    id_compra = instance.compra.id

    enc = ComprasEnc.objects.filter(pk=id_compra).first()
    if enc:
        sub_total = ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('sub_total'))
        descuento = ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('descuento'))
        enc.sub_total = sub_total['sub_total__sum']
        enc.descuento = descuento['descuento__sum']
        enc.save()

    prod = Producto.objects.filter(pk=id_producto).first()
    if prod:
        cantidad = int(prod.existencia) - int(instance.cantidad)
        prod.existencia = cantidad
        prod.save()


@receiver(post_save, sender=ComprasDet)
def detalle_compra_guardar(sender, instance, **kwargs):
    id_producto = instance.producto.id
    fecha_compra=instance.compra.fecha_compra

    prod = Producto.objects.filter(pk=id_producto).first()
    if prod:
        cantidad = int(prod.existencia) + int(instance.cantidad)
        prod.existencia = cantidad
        prod.ultima_compra=fecha_compra
        prod.save()

class OrdenComprasEnc(ClaseModelo):
    fecha_compra = models.DateField(null=True, blank=True)
    observacion = models.TextField(blank=True, null=True)
#    no_factura = models.CharField(max_length=100)
#    fecha_factura = models.DateField()
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    #proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        #return '{}'.format(self.total)
        return f'{self.observacion}, {self.total}'

    def save(self, **kwargs):
        self.observacion = self.observacion.upper()
        if self.sub_total == None  or self.descuento == None:
            self.sub_total = 0
            self.descuento = 0

        self.total = self.sub_total - self.descuento
        super(OrdenComprasEnc, self).save()

    class Meta:
        verbose_name_plural = "Encabezado de Orden Compras"
        verbose_name = "Encabezado Orden Compra"

class OrdenComprasDet(ClaseModelo):
    compra = models.ForeignKey(OrdenComprasEnc, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)
    precio_prv = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)
    costo = models.FloatField(default=0)
    estado_compra = models.CharField(max_length=12, default= 'En proceso' ) 

    def __str__(self):
        #return '{}'.format(self.producto)
        return f'{self.producto}, {self.cantidad}, {self.precio_prv},{self.descuento},{self.total}'

    def save(self, **kwargs):
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio_prv))
        self.total = self.sub_total - float(self.descuento)
        super(OrdenComprasDet, self).save()
    

    class Meta:
        verbose_name_plural = "Detalles orden Compras"
        verbose_name = "Detalle Orden Compra"
#fin de clase orden compra enc y detalle

