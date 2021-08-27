# Register your models here.

from django.contrib import admin
from Clientes.models import Cliente
from Clientes import views

#admin.site.register(Cliente)

#class ClienteAdmin(admin.ModelAdmin):
#	pass

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
	pass