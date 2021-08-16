from django.contrib import admin
#Modelo
from usuarios.models import Profile
# Register your models here.
#admin.site.register(Profile)

@admin.register(Profile)
class ProfileAdmnin(admin.ModelAdmin):
	"perfil administrador"

	list_display = ('pk','user', 'phone_number')