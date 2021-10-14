# Django
from rest_framework import serializers

# Local
from productos.models import Producto
from Clientes.models import Cliente


class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model=Producto
        fields='__all__'

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model=Cliente
        fields='__all__'