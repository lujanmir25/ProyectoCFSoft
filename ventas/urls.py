#Django
from django.urls import path,include

#Local
from ventas.views import FacturaView,facturas,ProductoView



urlpatterns = [
	path('ventas/',FacturaView.as_view(), name='factura_list'),
	path('ventas/new',facturas, name='factura_new'),
	path('ventas/buscar-producto',ProductoView.as_view(), name='factura_producto'),
]