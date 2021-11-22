#Django
from django.db import models

#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.utils import timezone
from datetime import date
#Local
from bases.models import ClaseModelo, ClaseModelo2, ClaseModeloUsuario
from productos.models import Producto
from proveedor.models import ComprasEnc, ComprasDet


class Cliente(ClaseModelo):
    NAT='Natural'
    JUR='Jurídica'
    TIPO_CLIENTE = [
        (NAT,'Natural'),
        (JUR,'Jurídica')
    ]
    nombres = models.CharField(
        max_length=100
    )
    apellidos = models.CharField(
        max_length=100
    )
    celular = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    tipo=models.CharField(
        max_length=10,
        choices=TIPO_CLIENTE,
        default=NAT
    )

    def __str__(self):
        return '{} {}'.format(self.apellidos,self.nombres)

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        super(Cliente, self).save( *args, **kwargs)

    class Meta:
        verbose_name_plural = "Clientes"


class FacturaEnc(ClaseModelo2):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    no_factura = models.CharField(max_length=15, default='0')
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)
    no_timbrado = models.CharField(default='00000000',max_length=8)
    fecha_fin_timbrado = models.DateField(null=True, blank=True)
    fecha_ini_timbrado = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.id)

    def save(self):
        self.total = self.sub_total - self.descuento
        super(FacturaEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado Facturas"
        verbose_name="Encabezado Factura"
        permissions = [
            ('sup_caja_facturaenc','Permisos de Supervisor de Caja Encabezado')
        ]


class Caja(ClaseModelo2):
    fac = models.ForeignKey(FacturaEnc,on_delete=models.CASCADE, null=True)
    comp = models.ForeignKey(ComprasEnc,on_delete=models.CASCADE, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now,null=True)
    entrada = models.BigIntegerField(default=0,null=True)
    salida = models.BigIntegerField(default=0,null=True)
    saldo_actual = models.BigIntegerField(default=0,null=True)


    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        if self.salida != 0:
            cant = Caja.objects.all().count()
            cajalist = Caja.objects.all()
            saldo = cajalist[cant-1].saldo_actual
            self.saldo_actual = saldo - self.salida
        else:
            cant = Caja.objects.all().count()
            if cant >=1:
                cajalist = Caja.objects.all()
                saldo = cajalist[cant-1].saldo_actual
                self.saldo_actual = saldo + self.entrada
            else:
                self.saldo_actual = self.entrada
        super(Caja,self).save()

    class Meta:
        verbose_name_plural= "Cajas"

class FacturaDet(ClaseModelo2):
    factura = models.ForeignKey(FacturaEnc,on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad=models.BigIntegerField(default=0)
    precio=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)

    def __str__(self):
        #return '{}'.format(self.producto)
        return f'{self.factura}, {self.producto}, {self.cantidad}, {self.precio}, {self.sub_total} , {self.total}'

    def save(self):
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio))
        self.total = self.sub_total - float(self.descuento)
        super(FacturaDet, self).save()
    
    class Meta:
        verbose_name_plural = "Detalles Facturas"
        verbose_name="Detalle Factura"
        permissions = [
            ('sup_caja_facturadet','Permisos de Supervisor de Caja Detalle')
        ]

@receiver(post_save, sender=FacturaDet)
def guardar_caja_venta(sender,instance,**kwargs):
   """ factura_id = instance.factura.id
    caja_id = instance.caja.id
    caja = Caja.objects.filter(pk=factura_id)

    if caja:
        entrada = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(sub_total=Sum('sub_total')) \
            .get('sub_total',0.00)
        desc = 'VENTA'

        #caja = Caja(factura=factura_id,descripcion=desc,entrada=entrada,salida=0)
        caja.entrada = caja.entrada + entrada
        caja.descripcion = desc
        caja.save() """


@receiver(post_save, sender=FacturaDet)
def detalle_fac_guardar(sender,instance,**kwargs):
    factura_id = instance.factura.id
    producto_id = instance.producto.id
    enc = FacturaEnc.objects.get(pk=factura_id)
    if enc:
        sub_total = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(sub_total=Sum('sub_total')) \
            .get('sub_total',0.00)
        
        descuento = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(descuento=Sum('descuento')) \
            .get('descuento',0.00)
        
        enc.sub_total = sub_total
        enc.descuento = descuento
        enc.save()

        cant = Caja.objects.all().count()
        cajalist = Caja.objects.all()
        total_detalle = enc.total
        saldo = cajalist[cant-1].saldo_actual
        saldo_actual = total_detalle + saldo

        caja = Caja (
            fac = enc,
            fecha = date.today(),
            descripcion = 'VENTA',
            entrada = total_detalle,
            salida = 0,
            saldo_actual = saldo_actual
        )

        caja.save() 


    prod=Producto.objects.filter(pk=producto_id).first()
    #import pdb; pdb.set_trace()
    if prod:
        cantidad = int(prod.existencia) - int(instance.cantidad)
        prod.existencia = cantidad
        prod.save()


class OrdenFacturaEnc(ClaseModelo2):
    #caja = models.ForeignKey(Caja, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.id)

    def save(self):
        #self.descripcion = self.descripcion.upper()
        self.total = self.sub_total - self.descuento
        super(OrdenFacturaEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado Orden Facturas"
        verbose_name="Encabezado Orden Factura"
        permissions = [
            ('sup_caja_facturaenc','Permisos de Supervisor de Caja Orden Encabezado')
        ]
    

class OrdenFacturaDet(ClaseModelo2):
    factura = models.ForeignKey(OrdenFacturaEnc,on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad=models.BigIntegerField(default=0)
    precio=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    #descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)

    def __str__(self):
        #return '{}'.format(self.producto)
        return f'{self.factura}, {self.producto}, {self.cantidad}, {self.precio}, {self.sub_total} , {self.total}'

    def save(self):
        self.sub_total = float(float(self.cantidad)) * float(self.precio)
        self.total = self.sub_total 
        super(OrdenFacturaDet, self).save()
    
    class Meta:
        verbose_name_plural = "Detalles Ordenes Facturas"
        verbose_name="Detalle orden Factura"
        permissions = [
            ('sup_caja_facturadet','Permisos de Supervisor de Caja Detalle')
        ]


