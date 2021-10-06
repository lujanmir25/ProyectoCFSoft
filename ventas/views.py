#Django
from django.shortcuts import render,redirect
from django.views import generic
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import datetime


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
	encabezado = {
		'fecha':datetime.today()
	}
	detalle = {}
	clientes = Cliente.objects.filter
	print(clientes)

	contexto={"enc":encabezado,"det":detalle,"clientes":clientes}


	return render(request,template_name, contexto)

class ProductoView(productos.ProductoView):
	template_name="ventas/buscar_producto.html"
