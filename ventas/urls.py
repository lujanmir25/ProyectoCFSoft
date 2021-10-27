#Django
from django.urls import path,include

#Local
from ventas.views import FacturaView,facturas,ProductoView, orden_facturas, OrdenFacturaView



urlpatterns = [
	path('ventas/',FacturaView.as_view(), name='factura_list'),
	path('orden_ventas/',OrdenFacturaView.as_view(), name='orden_factura_list'),
	path('ventas/new',facturas, name='factura_new'),
	path('orden_ventas/new',orden_facturas, name='orden_factura_new'),
	path('ventas/edit/<int:id>',facturas, name='factura_edit'),
	path('orden_ventas/edit/<int:id>',orden_facturas, name='orden_factura_edit'),
	path('ventas/buscar-producto',ProductoView.as_view(), name='factura_producto'),
]