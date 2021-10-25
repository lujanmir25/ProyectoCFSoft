#Django
from django.shortcuts import render,redirect
from django.views import generic
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse


#Local
from ventas.models import FacturaEnc, FacturaDet
from Clientes.models import Cliente
from Clientes.forms import ClienteForm
from productos.models import Producto
import productos.views as productos



class FacturaView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
	permission_required = "ventas.view_facturaenc"
	model = FacturaEnc
	template_name = "ventas/factura_list.html"
	context_object_name = "obj"
	login_url = 'bases:login'

@login_required(login_url='/login/')
@permission_required('ventas.change_facturasenc')

def facturas(request, id=None):
	template_name = 'ventas/facturas.html'
	
	detalle = {}
	clientes = Cliente.objects.filter(estado_c=True)

	if request.method == "GET":
		enc = FacturaEnc.objects.filter(pk=id).first()
		if not enc:
			encabezado = {
				'id':0,
				'fecha':datetime.today(),
				'cliente':0,
				'sub_total':0.00,
				'total': 0.00
			}
			detalle=None
		else:
			encabezado = {
				'id':enc.id,
				'fecha':enc.fecha,
				'cliente':enc.cliente,
				'sub_total':enc.sub_total,
				'total':enc.total
			}

			detalle=FacturaDet.objects.filter(factura=enc)

		contexto={"enc":encabezado,"det":detalle,"clientes":clientes}

	if request.method == "POST":
		cliente = request.POST.get("enc_cliente")
		fecha  = request.POST.get("fecha")
		cli = Cliente.objects.get(pk=cliente)

		if not id:
			enc = FacturaEnc(
				cliente = cli,
				fecha = fecha
			)
			if enc:
				enc.save()
				id = enc.id
		else:
			enc = FacturaEnc.objects.filter(pk=id).first()
			if enc:
				enc.cliente = cli
				enc.save()

		if not id:
			messages.error(request,'No Puedo Continuar No Pude Detectar No. de Factura')
			return redirect("ventas:factura_list")
	        
		codigo = request.POST.get("codigo")
		cantidad = request.POST.get("cantidad")
		precio = request.POST.get("precio")
		s_total = request.POST.get("sub_total_detalle")
		total = request.POST.get("total_detalle")

		prod = Producto.objects.get(codigo=codigo)
		det = FacturaDet(
			factura = enc,
			producto = prod,
			cantidad = cantidad,
			precio = precio,
			sub_total = s_total,
			total = total
		)

		if det:
			det.save()

		return redirect("ventas:factura_edit",id=id)

	return render(request,template_name, contexto)


class ProductoView(productos.ProductoView):
	template_name="ventas/buscar_producto.html"
