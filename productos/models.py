'''Modelo de productos'''
from django.db import models

class Producto(models.Model):
	"""Modelo de producto"""
	product_id = models.CharField(unique=True, max_length=50)

	product_name = models.CharField(max_length=50)
	
	stock_actual = models.IntegerField(blank=False)
	stock_minimo = models.IntegerField(blank=False)
	unidad_medida = models.CharField(max_length=5)
	
	fecha_ingreso = models.DateTimeField(auto_now_add=True) 
	fecha_caducidad = models.DateField()
	
	categoria = models.CharField(max_length=30)
	marca = models.CharField(max_length=30)