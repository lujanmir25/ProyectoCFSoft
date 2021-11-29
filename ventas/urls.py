#Django
from django.urls import path,include

#Local
from ventas.views import ClienteView,ClienteNew,ClienteEdit,clienteInactivar,FacturaView,facturas, \
ProductoView, borrar_detalle_factura, cliente_add_modify,orden_facturas,borrar_OrdenDetalle_factura, OrdenFacturaView, \
OrdenView, ordenInactivar, CajaView, CajaNew, CajaEdit, CajaDel, VentaDetEdit, cerrarCaja

from .reportes import imprimir_factura_recibo, imprimir_factura_list

urlpatterns = [

    path('clientes/',ClienteView.as_view(), name="cliente_list"),
    path('clientes/new',ClienteNew.as_view(), name="cliente_new"),
    path('clientes/<int:pk>',ClienteEdit.as_view(), name="cliente_edit"),
    path('clientes/estado/<int:id>',clienteInactivar, name="cliente_inactivar"),

	path('ventas/',FacturaView.as_view(), name='factura_list'),
    path('orden_ventas/',OrdenFacturaView.as_view(), name='orden_factura_list'),  
   # path('orden_ventas/',OrdenVentaView.as_view(), name='orden_venta_list'),
	path('ventas/new',facturas, name='factura_new'),
    path('ventas/orden_new',orden_facturas, name='orden_new'),
    #path('orden_ventas/new',OrdenVentaNew.as_view(), name="orden_venta_new"),
	path('ventas/edit/<int:id>',facturas, name='factura_edit'),
    path('orden_ventas/edit/<int:id>',orden_facturas, name='orden_factura_edit'),
    path('ventas_detalles/edit/<int:pk>', VentaDetEdit.as_view(), name="ventas_det_edit"),

	path('ventas/buscar-producto',ProductoView.as_view(), name='factura_producto'),
    path('ventas/buscar-orden',OrdenView.as_view(), name='factura_orden'),

	path('ventas/borrar-detalle/<int:id>',borrar_detalle_factura, name="factura_borrar_detalle"),
    path('ventas/borrar-OrdenDetalle/<int:id>',borrar_OrdenDetalle_factura, name="factura_borrar_OrdenDetalle"),

    path('ventas/imprimir/<int:id>',imprimir_factura_recibo, name="factura_imprimir_one"),
    path('ventas/imprimir-todas/<str:f1>/<str:f2>',imprimir_factura_list, name="factura_imprimir_all"),

    path('orden_venta/estado/<int:id>',ordenInactivar, name="orden_inactivar"),
    
    path('ventas/clientes/new/',cliente_add_modify,name="fac_cliente_add"),
    path('ventas/clientes/<int:pk>',cliente_add_modify,name="fac_cliente_mod"),

    path('caja/',CajaView.as_view(), name='caja_list'),
    path('caja/new',CajaNew.as_view(), name='caja_new'),
    path('caja/edit/<int:pk>',CajaEdit.as_view(), name='caja_edit'),
    path('caja/delete/<int:pk>',CajaDel.as_view(), name='caja_del'),

    path('cierre/<int:id>',cerrarCaja, name="cierre_caja"),

]