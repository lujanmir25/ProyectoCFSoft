"""#Django
from django.urls import path

#Local
from .views import ClienteView, ClienteNew, ClienteEdit, ClienteDel

urlpatterns = [
	path('clientes/',ClienteView.as_view(), name='cliente_list'),
	path('clientes/new',ClienteNew.as_view(), name='cliente_new'),
	path('clientes/edit/<int:pk>',ClienteEdit.as_view(), name='cliente_edit'),
	path('clientes/delete/<int:pk>',ClienteDel.as_view(), name='cliente_del'),
]

"""