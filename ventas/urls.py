#Django
from django.urls import path,include

#Local
from ventas.views import FacturaView



urlpatterns = [
	path('ventas/',FacturaView.as_view(), name='factura_list'),
]