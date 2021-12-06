from django.urls import path

#Local
from productos.views import ProductoView, ProductoNew, ProductoEdit, ProductoDel, InvProductoEdit, ProductoInvView, NotaCreditoView
from .reportes import imprimir_nota

urlpatterns = [
	path('productos/',ProductoView.as_view(), name='producto_list'),
	path('notas_creditos/',NotaCreditoView.as_view(), name='nota_credito_list'), 
	path('inv-productos/',ProductoInvView.as_view(), name='producto_inv_list'),
	path('productos/new',ProductoNew.as_view(), name='producto_new'),
	path('productos/edit/<int:pk>',ProductoEdit.as_view(), name='producto_edit'),
	path('Inventarioproductos/edit/<int:pk>',InvProductoEdit.as_view(), name='inv_producto_edit'),
	path('productos/delete/<int:pk>',ProductoDel.as_view(), name='producto_del'),
	path('notas_creditos/<int:id>/imprimir', imprimir_nota, name="nota_credito_print"),
]