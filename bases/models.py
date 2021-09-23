#Django
from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey


class ClaseModeloInv(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ClaseModelo(models.Model):
	uc = models.ForeignKey(User, on_delete=models.CASCADE)
	um = models.IntegerField(blank=True, null=True)

	class Meta:
		abstract = True

class ClaseModelo2(models.Model):
	uc = UserForeignKey(auto_user_add=True,related_name='+')
	um = UserForeignKey(auto_user=True,related_name='+')

	class Meta:
		abstract = True		

class ClaseModeloUsuario(models.Model):
	cedula = models.IntegerField(max_length=50,blank=False,unique=True,error_messages={'unique':"Person with this FirstName already exists."}) 
	nombre = models.CharField(max_length=50,blank=False)
	apellido = models.CharField(max_length=50,blank=False)
	ruc = models.CharField(max_length=50,blank=True, unique=True)
	email = models.CharField(max_length=50,blank=True)
	telefono = models.CharField(max_length=50,blank=True)
	direccion = models.CharField(max_length=50,blank=True)
	

	class Meta:
		abstract = True