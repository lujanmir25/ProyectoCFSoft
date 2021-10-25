"""cfsoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Clientes import views 
from productos import views
from ventas import views


urlpatterns = [
    path('', include(('bases.urls','bases'), namespace='bases')),
    path('Clientes/', include(('Clientes.urls','Clientes'), namespace='clientes')),
    path('proveedor/', include(('proveedor.urls', 'proveedor'), namespace='proveedor')),
    path('productos/', include(('productos.urls','productos'), namespace='productos')),
    path('inventario/', include(('inventario.urls', 'inventario'), namespace='inv')),
    path('ventas/', include(('ventas.urls', 'ventas'), namespace='ventas')),
    path('api/', include(('api.urls', 'api'), namespace='api')),
    path('admin/', admin.site.urls),
]
