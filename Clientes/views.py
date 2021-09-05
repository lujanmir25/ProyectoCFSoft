#Django
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

#Local
from .models import Cliente
from .forms import ClienteForm


#def MenuCliente(request):
#	clientes = Cliente.objects.all
#	return render(request,'clientes.html',{'clientes': clientes})

class ClienteView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
	permission_required = "Clientes.view_cliente"
	model = Cliente
	template_name = "clientes/cliente_list.html"
	context_object_name = "obj"
	login_url = 'bases:login'


class ClienteNew(LoginRequiredMixin, generic.CreateView):
	Model = Cliente
	template_name = "clientes/cliente_form.html"
	context_object_name = "obj"
	form_class=ClienteForm
	success_url = reverse_lazy("Clientes:cliente_list")
	login_url = "bases:login"

	#Para obtener el usuario que esta logueado
	def form_valid(self, form):
		form.instance.uc = self.request.user
		return super().form_valid(form)  

class ClienteEdit(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
	permission_required = "Clientes.change_cliente"
	model = Cliente
	template_name = "clientes/cliente_form.html"
	context_object_name = "obj"
	form_class=ClienteForm
	success_url = reverse_lazy("Clientes:cliente_list")
	login_url = "bases:login"

	def form_valid(self, form):
		form.instance.um = self.request.user.id
		return super().form_valid(form)


class ClienteDel(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
	permission_required = "Clientes.delete_cliente"
	model = Cliente
	template_name = "clientes/cliente_del.html"
	context_object_name = "obj"
	success_url = reverse_lazy("Clientes:cliente_list")

