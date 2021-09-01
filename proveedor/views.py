from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Proveedor
from .forms import ProveedorForm


class ProveedorView(LoginRequiredMixin, generic.ListView):
    model = Proveedor
    template_name = "prov/proveedor_list.html"
    context_object_name = "obj"
    login_url = "bases:login"


class ProveedorNew(LoginRequiredMixin, generic.CreateView):
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


class ProveedorEdit(LoginRequiredMixin, generic.UpdateView):
    model = Proveedor
    template_name = "prov/proveedor_form.html"
    context_object_name = 'obj'
    form_class = ProveedorForm
    success_url = reverse_lazy("proveedor:proveedor_list")
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ProveedorDel(LoginRequiredMixin, generic.DeleteView):
    model = Proveedor
    template_name = "prov/proveedor_del.html"
    context_object_name = 'obj'
    success_url = reverse_lazy("proveedor:proveedor_list")