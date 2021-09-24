#Django
from django.shortcuts import render
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

#Local
from ventas.models import FacturaEnc, FacturaDet


class FacturaView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
	permission_required = "ventas.view_facturaenc"
	model = FacturaEnc
	template_name = "ventas/factura_list.html"
	context_object_name = "obj"
	login_url = 'bases:login'