#Django
from django.urls import path,include

#Local
from ventas.views import FacturaView,facturas



urlpatterns = [
	path('ventas/',FacturaView.as_view(), name='factura_list'),
	path('ventas/new',facturas, name='factura_new'),
]