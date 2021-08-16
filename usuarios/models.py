"""Modelo de usuarios """

#Django dependencies
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model): 
	"""Modelo de perfil """

	user = models.OneToOneField(User, on_delete=models.CASCADE)

	website = models.URLField(max_length=100, blank=True)
	phone_number = models.CharField(max_length=20, blank=True)

	photo = models.ImageField(upload_to='users/pictures',blank=True, null= True )

	created = models.DateTimeField(auto_now_add=True )
	modified = models.DateTimeField(auto_now=True )

	def __str__(self):
		"""Retorna el nombre de usuario """
		return self.user.username 