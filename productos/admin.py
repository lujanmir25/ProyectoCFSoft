from django.contrib import admin


# Register your models here.
from productos.models import Producto
from productos import views

@admin.register(Producto)
class ProductosAdmnin(admin.ModelAdmin):
	"Productos Admnin "
	pass
	#list_display = ('product_name','stock_actual')