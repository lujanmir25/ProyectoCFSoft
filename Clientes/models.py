"""#Django
from django.db import models

#Local 
from bases.models import ClaseModelo,ClaseModeloUsuario

# El id no es necesario ya que Django maneja eso con una secuencia
class Cliente(ClaseModelo,ClaseModeloUsuario):
	

	def __str__(self):
		return '{}'.format(self.cedula)

	class Meta:
		verbose_name_plural= "Clientessss" """