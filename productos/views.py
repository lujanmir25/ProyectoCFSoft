from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, \
    PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Producto
from .forms import ProductoForm


# Create your views here.
class ProductoView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = "productos.view_producto"
    model = Producto
    template_name = "productos/producto_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'


class ProductoNew(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = "productos.add_producto"
    Model = Producto
    template_name = "productos/producto_form.html"
    context_object_name = "obj"
    form_class = ProductoForm
    success_url = reverse_lazy("productos:producto_list")
    login_url = "bases:login"

    # Para obtener el usuario que esta logueado
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class ProductoEdit(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = "productos.change_producto"
    model = Producto
    template_name = "productos/producto_form.html"
    context_object_name = "obj"
    form_class = ProductoForm
    success_url = reverse_lazy("productos:producto_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ProductoDel(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = "productos.delete_producto"
    model = Producto
    template_name = "productos/producto_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("productos:producto_list")
