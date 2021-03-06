from django.db import models
# Para los signals
from django.db.models.signals import post_save, post_delete
from django.urls import reverse
from django.dispatch import receiver
from django.db.models import Sum
from bases.models import ClaseModelo, ClaseModeloUsuario
from productos.models import Producto
from datetime import datetime



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
    fecha_compra = models.DateTimeField(null=True, blank=True)
    #fecha_compra = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)
    no_factura = models.CharField(max_length=100, default=0)
    cantidad_cuotas = models.CharField(max_length=12, default='')
    no_timbrado = models.CharField(max_length=8)
    fecha_fin_timbrado = models.DateField(null=True, blank=True)
    fecha_ini_timbrado = models.DateField(null=True, blank=True)
    fecha_factura = models.DateField()
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        #return '{}'.format(self.observacion)
        return '{}'.format(self.id)

    def save(self, **kwargs):
        #self.observacion = self.observacion.upper() 
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
    dif_cantidad = models.IntegerField(default=0)
    precio_prv = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)
    costo = models.FloatField(default=0)

    def __str__(self):
        #return '{}'.format(self.producto)
        return f'{self.compra}, {self.producto}, {self.cantidad}, {self.precio_prv}, {self.sub_total} , {self.total}'

    def save(self, **kwargs):
        self.cantidad = self.cantidad + self.dif_cantidad
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
    id_compra = instance.compra.id
    fecha_compra=instance.compra.fecha_compra
    precio_compra = instance.precio_prv

    enc = ComprasEnc.objects.filter(pk=id_compra).first()
    #caja = Caja.objects.filter(comp= id_compra).first()
    #import pdb; pdb.set_trace()

    if enc:
        sub_total = ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('sub_total'))
        descuento = ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('descuento'))
        enc.sub_total = sub_total['sub_total__sum']
        enc.descuento = descuento['descuento__sum']
        enc.save()

    cantidad = enc.cantidad_cuotas
    monto_cuenta = enc.sub_total

    deuda = PagoProveedor.objects.filter(compra_id=id_compra).first()
    if deuda:
        deuda.monto_mensual = monto_cuenta/int(cantidad)
        deuda.cantidad_cuotas= cantidad
        deuda.monto_total_pag = 0
        deuda.estado_cuenta = 'Pendiente'
        deuda.save()


    prod = Producto.objects.filter(pk=id_producto).first()
    if prod:
        if instance.dif_cantidad < 0:
             cantidad = int(prod.existencia) - int(instance.cantidad)
        else:
            cantidad = int(prod.existencia) + int(instance.cantidad)
        prod.existencia = cantidad
        prod.ultima_compra=fecha_compra
        prod.precio = precio_compra
        prod.save()

    # Caja 
    from ventas.models import Caja

    c = Caja.objects.filter(comp=id_compra).first()
    # si ya existe la caja entonces editamos
    if c:
        #c = list(c)
        #for item in c:
        id_caja = c.id
        caja = Caja.objects.filter(id=id_caja).first()                                                                                                                                                      
        #import pdb; pdb.set_trace()
        caja.saldo_actual = caja.salida + caja.saldo_actual
        caja.salida = enc.total
        caja.saldo_actual = caja.saldo_actual - caja.salida
        caja.save()

        # Calculo para ajustar los saldos
        """cajaList = Caja.objects.all()
        cajaList = list(cajaList)
        lastid = cajaList[-1].id 
        import pdb; pdb.set_trace()
        if lastid > id_caja :
            #cajaList = list(cajaList)
            saldo_actual = caja.saldo_actual
            i = id_caja + 1
            import pdb; pdb.set_trace()
            while i < lastid or i == lastid:
                caja = Caja.objects.filter(id=i).first()
                if caja.entrada > 0:
                    caja.saldo_actual = saldo_actual + caja.entrada
                    saldo_actual = caja.saldo_actual
                else:
                    caja.saldo_actual = saldo_actual - caja.salida
                    saldo_actual = caja.saldo_actual
                i=i+1
                caja.save()"""
    # si no existe la caja crea un nuevo registro           
    else:
        cant = Caja.objects.all().count()
        cajalist = Caja.objects.all()
        total_detalle = enc.total
        saldo = cajalist[cant-1].saldo_actual
        saldo_actual = saldo - total_detalle 

        caja = Caja (
            comp = enc,
            #fecha = datetime.today(),
            descripcion = 'COMPRA',
            entrada = 0,
            salida = total_detalle,
            saldo_actual = saldo_actual
        )

        caja.save()

    #import pdb;pdb.set_trace()

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

#Modelo pagos_proveedor 

class PagoProveedor(models.Model):
    compra = models.ForeignKey(ComprasEnc, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cantidad_cuotas = models.CharField(max_length=3, default='')
    #cant_cuotas_pagadas = models.BigIntegerField(default=0)
    monto_mensual = models.FloatField(default=0)
    monto_total_pag = models.FloatField(default=0)
    estado_cuenta = models.CharField(max_length=12, default= 'Iniciado' )

    def __str__(self):
        #return '{}'.format(self.producto)
        return f'{self.proveedor}, {self.cantidad_cuotas},{self.monto_mensual},{self.monto_total_pag}'

    class Meta:
        verbose_name_plural = "Pago de Proveedores"
        verbose_name = "Pago de Proveedor"