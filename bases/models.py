#Django
from django.db import models
from django.contrib.auth.models import User


class ClaseModelo(models.Model):
	uc = models.ForeignKey(User, on_delete=models.CASCADE)
	um = models.IntegerField(blank=True, null=True)

	class Meta:
		abstract = True
