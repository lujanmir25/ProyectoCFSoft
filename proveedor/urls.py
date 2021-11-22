# Django
from django.urls import path

# Local
from .views import ProveedorView, ProveedorNew, ProveedorEdit, ProveedorDel, PagoView, ComprasDetEdit,ComprasDetView, \
    ComprasView, compras, CompraDetDelete, OrdenComprasView, orden_compras, OrdenView, clienteInactivar, realizarPago, detalle_compras
from .reportes import reporte_compras, imprimir_compra

urlpatterns = [
    path('proveedor/', ProveedorView.as_view(), name='proveedor_list'),
    path('proveedor/new', ProveedorNew.as_view(), name='proveedor_new'),
    path('proveedor/edit/<int:pk>', ProveedorEdit.as_view(), name='proveedor_edit'),
    path('proveedor/delete/<int:pk>', ProveedorDel.as_view(), name='proveedor_del'),
    path('compras/listado', reporte_compras, name='compras_print_all'),
    path('compras/<int:compras_id>/imprimir', imprimir_compra, name="compras_print_one"),

    path('compras/', ComprasView.as_view(), name="compras_list"),
    path('compras_detalle/', ComprasDetView.as_view(), name="compras_det_list"), 
    path('orden_compras/', OrdenComprasView.as_view(), name="orden_compras_list"),
    path('pago/', PagoView.as_view(), name="pago_list"),
    path('compras/new', compras, name="compras_new"),
    path('orden_compras/new', orden_compras, name="orden_compras_new"),
    path('compras/edit/<int:compra_id>', compras, name="compras_edit"),  
    path('compras_detalle/<int:compra_id>/edit/<int:pk>', ComprasDetEdit.as_view(), name="compras_detalle_edit"),
    #path('compras_detalles/edit/<int:id>', ComprasDetEdit.as_view(), name="compras_det_edit"),
    path('compras_detalles/edit/<int:pk>', ComprasDetEdit.as_view(), name="compras_det_edit"),
    path('orden_compras/edit/<int:compra_id>', orden_compras, name="orden_compras_edit"),
    path('compras/<int:compra_id>/delete/<int:pk>', CompraDetDelete.as_view(), name="compras_del"),
    path('orden_compra/estado/<int:id>',clienteInactivar, name="cliente_inactivar"),
    path('pago/<int:id>',realizarPago, name="realizar_pago"),
    path('proveedor/buscar-orden',OrdenView.as_view(), name='buscar_compra'),

   # path('caja/new', caja, name="caja_reg")
]
