from django.contrib.auth.decorators import login_required, permission_required
from django.db.models.fields import IntegerField
from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy
import datetime
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from django.core import serializers

from .models import Proveedor, ComprasEnc, ComprasDet, OrdenComprasEnc, OrdenComprasDet, PagoProveedor
from .forms import ProveedorForm, ComprasEncForm, OrdenComprasEncForm, ComprasDetForm
from bases.models import ClaseModelo
from ventas.models import Caja
from productos.models import Producto


class ProveedorView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = "proveedor.view_proveedor"
    model = Proveedor
    template_name = "prov/proveedor_list.html"
    context_object_name = "obj"
    login_url = "bases:login"

class PagoView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = "proveedor.view_proveedor"
    model = PagoProveedor
    template_name = "prov/pago_list.html"
    context_object_name = "obj"
    login_url = "bases:login"

class ProveedorNew(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = "proveedor.add_proveedor"
    model = Proveedor
    template_name = "prov/proveedor_form.html"
    context_object_name = 'obj'
    form_class = ProveedorForm
    success_url = reverse_lazy("proveedor:proveedor_list")
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        # print(self.request.user.id)
        return super().form_valid(form)

class ComprasDetEdit(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = "proveedor.view_comprasenc"
    model = ComprasDet
    template_name = "prov/compras_det_form.html"
    context_object_name = 'obj'
    form_class = ComprasDetForm
    #success_url = reverse_lazy("proveedor:compras_list")
    login_url = 'bases:login'

    def get_success_url(self):
        compra_id = self.kwargs['compra_id']
        return reverse_lazy('proveedor:compras_edit', kwargs={'compra_id': compra_id})

    def form_valid(self, form):
        form.instance.uc = self.request.user
        # print(self.request.user.id)
        return super().form_valid(form)

class CompraDetDelete(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = "proveedor.delete_comprasdet"
    model = ComprasDet
    template_name = "prov/compras_det_del.html"
    context_object_name = 'obj'

    def get_success_url(self):
        compra_id = self.kwargs['compra_id']
        return reverse_lazy('proveedor:compras_edit', kwargs={'compra_id': compra_id})



class ProveedorEdit(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = "proveedor.change_proveedor"
    model = Proveedor
    template_name = "prov/proveedor_form.html"
    context_object_name = 'obj'
    form_class = ProveedorForm
    success_url = reverse_lazy("proveedor:proveedor_list")
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ProveedorDel(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = "proveedor.delete_proveedor"
    model = Proveedor
    template_name = "prov/proveedor_del.html"
    context_object_name = 'obj'
    success_url = reverse_lazy("proveedor:proveedor_list")


class ComprasView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = "proveedor.view_comprasenc"
    model = ComprasEnc
    template_name = "prov/compras_list.html"
    context_object_name = "obj"
    login_url = "bases:login"

class ComprasDetView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = "proveedor.view_comprasenc"
    model = ComprasDet
    template_name = "prov/compras_det_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


@login_required(login_url='/login/')
@permission_required('proveedor.view_comprasenc', login_url='bases:login')
def detalle_compras(request, id):
    template_name = "prov/compras_det.html"
    det = ComprasDet.objects.filter(pk = id)
    #import pdb; pdb.set_trace()
    form_detalles = {}
    contexto = {}

    for item in det:
        compra_det= item.compra
        producto_det= item.producto
        cantidad_det= item.cantidad
        precio_det= item.precio_prv
        descuento_det= item.descuento
        sub_total_det= item.sub_total
        total_det= item.total

    if request.method == 'GET':
        form_detalles = ComprasDetForm()
    
        if det:
            e = {
                'compra' : compra_det,
                'producto' : producto_det,
                'cantidad': cantidad_det,
                'precio_prv': precio_det, 
                'descuento': descuento_det,
                'sub_total': sub_total_det,
                'total': total_det,
            }
            form_detalles = ComprasDetForm(e)
        contexto = { 'detalle': det, 'form_det': form_detalles}

    if request.method == 'POST':
        #compra = request.POST.get("id_compra")
        producto = request.POST.get("id_producto")
        cantidad = request.POST.get("id_cantidad")
        precio_prv = request.POST.get("id_precio")
            

        det = ComprasDet(
            producto=producto, 
            cantidad = cantidad,
            precio_prv = precio_prv,
            sub_total = cantidad * precio_prv,
            total = cantidad * precio_prv,
            costo=0,
            uc=request.user) 

        det.save()

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('proveedor.view_comprasenc', login_url='bases:login')
def compras(request, compra_id=None):
    template_name = "prov/compras.html"
    prod = Producto.objects.filter(estado=True)
    orden = OrdenComprasEnc.objects.filter(estado=False)
    
#    detalle = OrdenComprasDet.objects.all()
    detalleOrdenesAll = OrdenComprasDet.objects.all()
    tempOrdenes = []
    blog = OrdenComprasDet.objects.all()
    form_compras = {}
    contexto = {}

    if request.method == 'GET':
        form_compras = ComprasEncForm()
        form_detalles = ComprasDetForm()
        enc = ComprasEnc.objects.filter(pk=compra_id).first()
        
        if enc:
            det = ComprasDet.objects.filter(compra=enc)
            cantidad_cuotas = (enc.cantidad_cuotas)
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            fecha_factura = datetime.date.isoformat(enc.fecha_factura)
            fecha_ini_timbrado = datetime.date.isoformat(enc.fecha_ini_timbrado)
            fecha_fin_timbrado = datetime.date.isoformat(enc.fecha_fin_timbrado)
            e = {
                'cantidad_cuotas' : cantidad_cuotas,
                'fecha_compra': fecha_compra,
                'proveedor': enc.proveedor,
                'observacion': enc.observacion,
                'fecha_ini_timbrado' : fecha_ini_timbrado,
                'fecha_fin_timbrado' : fecha_fin_timbrado,
                'no_factura': enc.no_factura,
                'no_timbrado': enc.no_timbrado,
                'fecha_factura': fecha_factura,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total': enc.total
            }
            form_compras = ComprasEncForm(e)
        else:
            det = None

        contexto = {'orden': orden,'productos': prod, 'encabezado': enc, 'detalle': det, 'form_enc': form_compras}

    if request.method == 'POST':
        proveedor = request.POST.get("proveedor")
        cantidad_cuotas = request.POST.get("cantidad_cuotas")
        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
        no_factura = request.POST.get("no_factura")
        fecha_factura = request.POST.get("fecha_factura")
        fecha_ini_timbrado = request.POST.get("fecha_ini_timbrado")
        fecha_fin_timbrado = request.POST.get("fecha_fin_timbrado")
        no_timbrado = request.POST.get("no_timbrado")
        
        orden_id = request.POST.get("id_id_orden_compra")

        sub_total = 0
        descuento = 0
        total = 0

        if not compra_id:
            prov = Proveedor.objects.get(pk=proveedor)

            enc = ComprasEnc(
                fecha_compra=fecha_compra,
                observacion=observacion,
                cantidad_cuotas=cantidad_cuotas,
                no_factura= ('001-'+'002-' + int(str(7 - len(str(no_factura))))*'0' + str(no_factura)),
                no_timbrado=no_timbrado,
                fecha_fin_timbrado=fecha_fin_timbrado,
                fecha_ini_timbrado=fecha_ini_timbrado,
                fecha_factura=fecha_factura,
                proveedor=prov,
                uc=request.user
            )
            if enc:
                enc.save()
                compra_id = enc.id
        else:
            enc = ComprasEnc.objects.filter(pk=compra_id).first()
            if enc:
                enc.fecha_compra = fecha_compra
                enc.observacion = observacion    
                enc.cantidad_cuotas = cantidad_cuotas
                enc.no_factura = ('001-'+'002-' + int(str(7 - len(str(no_factura))))*'0' + str(no_factura)),
                enc.no_timbrado=no_timbrado,
                enc.fecha_fin_timbrado=fecha_fin_timbrado,
                enc.fecha_ini_timbrado=fecha_ini_timbrado,
                enc.fecha_factura = fecha_factura
                enc.um = request.user.id
                enc.save()
        if not compra_id:
            return redirect("proveedor:compras_list")
         
        orden_id = request.POST.get("id_id_orden_compra") #Recibe el id de la orden.
        Descripcion = request.POST.get("id_descripcion_orden")
        

        #detalleOrdenes = OrdenComprasDet.objects.filter(compra=orden_id).values()
        detalleOrdenes = OrdenComprasDet.objects.filter(compra=orden_id)
        items = detalleOrdenes.count()
        
        detalleOrdenes = list(detalleOrdenes)

        for items in detalleOrdenes:
            cantidad_d = items.cantidad
            precio = items.precio_prv
            sub_total = items.sub_total
            total = items.total
            producto_id = items.producto_id
            prod = Producto.objects.get(pk=producto_id)

            det = ComprasDet(
                compra=enc,
                producto=prod, 
                cantidad = cantidad_d,
                precio_prv = precio,
                sub_total = sub_total,
                total = total,
                costo=0,
                uc=request.user
            ) 

            det.save()
            form_detalles = ComprasDetForm(det)

        #detalle = list(ComprasDet.objects.filter(id = 47))
        #import pdb; pdb.set_trace()


        #if det:
        #    det.save()
        
        sub_total = OrdenComprasDet.objects.filter(compra=orden_id).aggregate(Sum('sub_total'))
        #descuento = ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('descuento'))
        enc.sub_total = sub_total["sub_total__sum"]
        enc.save()
        compra = ComprasEnc.objects.get(pk=enc.id)
        pagos = PagoProveedor( 
            compra = compra, 
            proveedor = enc.proveedor,
            cantidad_cuotas = enc.cantidad_cuotas,
            monto_mensual = float(enc.total) / int(cantidad_cuotas),
            monto_total_pag = 0,
            estado_cuenta = 'Pendiente'
        )
        pagos.save()


        #Calculos para la Caja
        """cant = Caja.objects.all().count()
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

        caja.save()"""

        return redirect("proveedor:compras_edit", compra_id=compra_id)

    return render(request, template_name, contexto)


class OrdenComprasView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = "proveedor.view_comprasenc"
    model = OrdenComprasEnc
    template_name = "prov/orden_compras_list.html"
    context_object_name = "obj"
    login_url = "bases:login"

def orden_compras(request, compra_id=None):
    template_name = "prov/orden_compras.html"
    prod = Producto.objects.filter(estado=True)
    form_compras = {}
    contexto = {}

    if request.method == 'GET':
        form_compras = OrdenComprasEncForm() 
        enc = OrdenComprasEnc.objects.filter(pk=compra_id).first()

        if enc:
            det = OrdenComprasDet.objects.filter(compra=enc)
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
        #    fecha_factura = datetime.date.isoformat(enc.fecha_factura)
            e = {
                'fecha_compra': fecha_compra,
            #    'proveedor': enc.proveedor,
                'observacion': enc.observacion,
            #    'no_factura': enc.no_factura,
            #    'fecha_factura': fecha_factura,
            #    'estado_compra': enc.estado_compra,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total': enc.total
            }
            form_compras = OrdenComprasEncForm(e)
        else:
            det = None

        contexto = {'productos': prod, 'encabezado': enc, 'detalle': det, 'form_enc': form_compras}

    if request.method == 'POST':
        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
    #    no_factura = request.POST.get("no_factura")
    #    fecha_factura = request.POST.get("fecha_factura")
        proveedor = request.POST.get("proveedor")
        sub_total = 0
        descuento = 0
        total = 0

        if not compra_id:
        #    prov = Proveedor.objects.get(pk=proveedor)

            enc = OrdenComprasEnc(
                fecha_compra=fecha_compra,
                observacion=observacion,
            #    no_factura=no_factura,
            #    fecha_factura=fecha_factura,
            #    proveedor=prov,
                uc=request.user
            )
            if enc:
                enc.save()
                compra_id = enc.id
        else:
            enc = OrdenComprasEnc.objects.filter(pk=compra_id).first()
            if enc:
                enc.fecha_compra = fecha_compra
                enc.observacion = observacion
            #    enc.no_factura = no_factura
            #    enc.fecha_factura = fecha_factura
                enc.um = request.user.id
                enc.save()
        if not compra_id:
            return redirect("proveedor:orden_compras_list")

        producto = request.POST.get("id_id_producto")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        sub_total_detalle = request.POST.get("id_sub_total_detalle")
        descuento_detalle = request.POST.get("id_descuento_detalle")
        total_detalle = request.POST.get("id_total_detalle")

        prod = Producto.objects.get(pk=producto)

        det = OrdenComprasDet(
            compra=enc,
            producto=prod,
            cantidad=cantidad,
            precio_prv=precio,
            descuento=descuento_detalle,
            costo=0,
            uc=request.user
        )

        if det:
            det.save()

            sub_total = OrdenComprasDet.objects.filter(compra=compra_id).aggregate(Sum('sub_total'))
            descuento = OrdenComprasDet.objects.filter(compra=compra_id).aggregate(Sum('descuento'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.descuento = descuento["descuento__sum"]
            enc.save()

        return redirect("proveedor:orden_compras_edit", compra_id=compra_id)

    return render(request, template_name, contexto)
#CREAR CONVERSION PARA ORDENES DE COMPRA 
#f'{self.producto}, {self.cantidad}, {self.precio_prv},{self.descuento},{self.total}'


class OrdenView(OrdenComprasView):
	template_name="prov/buscar_orden_compra.html"

def clienteInactivar(request,id):
    cliente = OrdenComprasEnc.objects.filter(pk=id).first()

    if request.method=="POST":
        if cliente:
            cliente.estado = not cliente.estado
            cliente.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL") 

def realizarPago(request,id):
    deuda = PagoProveedor.objects.filter(pk=id).first()

    if request.method=="POST":
        if deuda:  
            if deuda.estado_cuenta == 'Pendiente':
            #deuda.estado = not deuda.estado
                deuda.cantidad_cuotas = int(deuda.cantidad_cuotas) -1
                deuda.monto_total_pag  = deuda.monto_total_pag + deuda.monto_mensual
                if deuda.cantidad_cuotas == 0: 
                    deuda.estado_cuenta = 'Cancelado'
                deuda.save()
                return HttpResponse("OK")
            return HttpResponse("Pay")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")



