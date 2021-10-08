from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy
import datetime
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum

from .models import Proveedor, ComprasEnc, ComprasDet
from .forms import ProveedorForm, ComprasEncForm
from bases.models import ClaseModelo
from productos.models import Producto


class ProveedorView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = "proveedor.view_proveedor"
    model = Proveedor
    template_name = "prov/proveedor_list.html"
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


@login_required(login_url='/login/')
@permission_required('proveedor.view_comprasenc', login_url='bases:login')
def compras(request, compra_id=None):
    template_name = "prov/compras.html"
    prod = Producto.objects.filter(estado_c=True)
    form_compras = {}
    contexto = {}

    if request.method == 'GET':
        form_compras = ComprasEncForm()
        enc = ComprasEnc.objects.filter(pk=compra_id).first()

        if enc:
            det = ComprasDet.objects.filter(compra=enc)
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            fecha_factura = datetime.date.isoformat(enc.fecha_factura)
            e = {
                'fecha_compra': fecha_compra,
                'proveedor': enc.proveedor,
                'observacion': enc.observacion,
                'no_factura': enc.no_factura,
                'fecha_factura': fecha_factura,
                'sub_total': enc.sub_total,
                'descuento': enc.descuento,
                'total': enc.total
            }
            form_compras = ComprasEncForm(e)
        else:
            det = None

        contexto = {'productos': prod, 'encabezado': enc, 'detalle': det, 'form_enc': form_compras}

    if request.method == 'POST':
        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
        no_factura = request.POST.get("no_factura")
        fecha_factura = request.POST.get("fecha_factura")
        proveedor = request.POST.get("proveedor")
        sub_total = 0
        descuento = 0
        total = 0

        if not compra_id:
            prov = Proveedor.objects.get(pk=proveedor)

            enc = ComprasEnc(
                fecha_compra=fecha_compra,
                observacion=observacion,
                no_factura=no_factura,
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
                enc.no_factura = no_factura
                enc.fecha_factura = fecha_factura
                enc.um = request.user.id
                enc.save()
        if not compra_id:
            return redirect("proveedor:compras_list")

        producto = request.POST.get("id_id_producto")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        sub_total_detalle = request.POST.get("id_sub_total_detalle")
        descuento_detalle = request.POST.get("id_descuento_detalle")
        total_detalle = request.POST.get("id_total_detalle")

        prod = Producto.objects.get(pk=producto)

        det = ComprasDet(
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

            sub_total = ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('sub_total'))
            descuento = ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('descuento'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.descuento = descuento["descuento__sum"]
            enc.save()

        return redirect("proveedor:compras_edit", compra_id=compra_id)

    return render(request, template_name, contexto)


class CompraDetDelete(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = "proveedor.delete_comprasdet"
    model = ComprasDet
    template_name = "prov/compras_det_del.html"
    context_object_name = 'obj'

    # success_url = reverse_lazy("proveedor:proveedor_list")

    def get_success_url(self):
        compra_id = self.kwargs['compra_id']
        return reverse_lazy('proveedor:compras_edit', kwargs={'compra_id': compra_id})
