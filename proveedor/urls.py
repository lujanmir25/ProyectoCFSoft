# Django
from django.urls import path

# Local
from .views import ProveedorView, ProveedorNew, ProveedorEdit, ProveedorDel

urlpatterns = [
    path('proveedor/', ProveedorView.as_view(), name='proveedor_list'),
    path('proveedor/new', ProveedorNew.as_view(), name='proveedor_new'),
    path('proveedor/edit/<int:pk>', ProveedorEdit.as_view(), name='proveedor_edit'),
    path('proveedor/delete/<int:pk>', ProveedorDel.as_view(), name='proveedor_del'),
]
