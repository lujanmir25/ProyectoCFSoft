#Django
from django.db import models

#Local 
from bases.models import ClaseModelo

# El id no es necesario ya que Django maneja eso con una secuencia
class Cliente(ClaseModelo):
	cedula = models.CharField(max_length=50,blank=True) 
	nombre = models.CharField(max_length=50,blank=True)
	apellido = models.CharField(max_length=50,blank=True)
	ruc = models.CharField(max_length=50,blank=True)
	email = models.CharField(max_length=50,blank=True)
	telefono = models.CharField(max_length=50,blank=True)
	direccion = models.CharField(max_length=50,blank=True)
	

	def __str__(self):
		return '{}'.format(self.cedula)

	class Meta:
		verbose_name_plural= "Clientes"