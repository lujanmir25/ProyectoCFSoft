# Django
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Local
from .serializers import ProductoSerializer,ClienteSerializer
from productos.models import Producto
from Clientes.models import Cliente

class ProductoList(APIView):
    def get(self,request):
        prod = Producto.objects.all()
        data = ProductoSerializer(prod,many=True).data
        return Response(data)


class ProductoDetalle(APIView):
    def get(self,request, codigo):
        prod = get_object_or_404(Producto,Q(codigo=codigo))
        data = ProductoSerializer(prod).data
        return Response(data)

class ProductoDetalle(APIView):
    def get(self,request, codigo):
        prod = get_object_or_404(Producto,Q(codigo=codigo)|Q(codigo_barra=codigo))
        data = ProductoSerializer(prod).data
        return Response(data)


class ClienteList(APIView):
    def get(self,request):
        obj = Cliente.objects.all()
        data = ClienteSerializer(obj,many=True).data
        return Response(data)