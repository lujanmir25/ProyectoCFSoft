#Django
from django.db import models
from django.contrib.auth.models import User

class ClaseModeloInv(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ClaseModelo(models.Model):
	estado_c = models.BooleanField(default=True)
	uc = models.ForeignKey(User, on_delete=models.CASCADE)
	um = models.IntegerField(blank=True, null=True)

	class Meta:
		abstract = True

class ClaseModeloUsuario(models.Model):
	cedula = models.CharField(max_length=50,blank=True) 
	nombre = models.CharField(max_length=50,blank=True)
	apellido = models.CharField(max_length=50,blank=True)
	ruc = models.CharField(max_length=50,blank=True)
	email = models.CharField(max_length=50,blank=True)
	telefono = models.CharField(max_length=50,blank=True)
	direccion = models.CharField(max_length=50,blank=True)
	

	class Meta:
		abstract = True