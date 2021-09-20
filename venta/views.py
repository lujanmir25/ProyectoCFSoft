#Django
from django.shortcuts import render
from django.views import generic

#Local
#from bases.views import SinPrivilegios
from Clientes.models import Cliente 

"""class ClienteView(SinPrivilegios, geneic.ListView):
	model = Cliente
	template_name = "Cliente/cliente_list.html"
	context_object_name = "obj"
	permission_required = "cmp.view_cliente""""