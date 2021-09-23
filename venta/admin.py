from django.contrib import admin

# Register your models here.

@admin.register(FacturaEnc)
class FacturaEncAdmnin(admin.ModelAdmin):
	"Fact Admnin "
	pass