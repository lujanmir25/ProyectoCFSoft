#Django
from django.urls import path,include

#Local
from ventas.views import ClienteView,ClienteNew,ClienteEdit,clienteInactivar,FacturaView,facturas, \
ProductoView, borrar_detalle_factura, cliente_add_modify

from .reportes import imprimir_factura_recibo, imprimir_factura_list

urlpatterns = [

    path('clientes/',ClienteView.as_view(), name="cliente_list"),
    path('clientes/new',ClienteNew.as_view(), name="cliente_new"),
    path('clientes/<int:pk>',ClienteEdit.as_view(), name="cliente_edit"),
    path('clientes/estado/<int:id>',clienteInactivar, name="cliente_inactivar"),

	path('ventas/',FacturaView.as_view(), name='factura_list'),
   # path('orden_ventas/',OrdenVentaView.as_view(), name='orden_venta_list'),
	path('ventas/new',facturas, name='factura_new'),
    #path('orden_ventas/new',OrdenVentaNew.as_view(), name="orden_venta_new"),
	path('ventas/edit/<int:id>',facturas, name='factura_edit'),
	path('ventas/buscar-producto',ProductoView.as_view(), name='factura_producto'),

	path('ventas/borrar-detalle/<int:id>',borrar_detalle_factura, name="factura_borrar_detalle"),
    path('ventas/imprimir/<int:id>',imprimir_factura_recibo, name="factura_imprimir_one"),
    path('ventas/imprimir-todas/<str:f1>/<str:f2>',imprimir_factura_list, name="factura_imprimir_all"),
    
    path('ventas/clientes/new/',cliente_add_modify,name="fac_cliente_add"),
    path('ventas/clientes/<int:pk>',cliente_add_modify,name="fac_cliente_mod"),

]