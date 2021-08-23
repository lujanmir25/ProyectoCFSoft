from django.contrib import admin

# Register your models here.

from productos.models import Producto 

@admin.register(Producto)
class ProductosAdmnin(admin.ModelAdmin):
	"Productos Admnin "
	
	list_display = ('product_id', 'product_name')