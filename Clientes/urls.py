#Django
from django.urls import path

#Local
from .views import ClienteView, ClienteNew, ClienteEdit

urlpatterns = [
	path('clientes/',ClienteView.as_view(), name='cliente_list'),
	path('clientes/new',ClienteNew.as_view(), name='cliente_new'),
	path('clientes/edit/<int:pk>',ClienteEdit.as_view(), name='cliente_edit'),
]