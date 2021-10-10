# Django
from django.urls import path

# Local
from .views import ProveedorView, ProveedorNew, ProveedorEdit, ProveedorDel, \
    ComprasView, compras, CompraDetDelete

urlpatterns = [
    path('proveedor/', ProveedorView.as_view(), name='proveedor_list'),
    path('proveedor/new', ProveedorNew.as_view(), name='proveedor_new'),
    path('proveedor/edit/<int:pk>', ProveedorEdit.as_view(), name='proveedor_edit'),
    path('proveedor/delete/<int:pk>', ProveedorDel.as_view(), name='proveedor_del'),

    path('compras/', ComprasView.as_view(), name="compras_list"),
    path('compras/new', compras, name="compras_new"),
    path('compras/edit/<int:compra_id>', compras, name="compras_edit"),
    path('compras/<int:compra_id>/delete/<int:pk>', CompraDetDelete.as_view(), name="compras_del"),
]
