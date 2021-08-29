# Django
from django import forms
# Local
from .models import Producto
# La vista llama a este formulario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['product_name', 'stock_actual', 'stock_minimo', 'unidad_medida',
                  'fecha_ingreso', 'fecha_caducidad', 'categoria', 'marca']

        labels = {'product_name': "Nombre Producto",
                  'stock_actual': 'Stock Actual',
                  'stock_minimo': 'Stock Minimo',
                  'unidad_medida': 'Unidad de Medida',
                  'fecha_ingreso': 'Fecha de Ingreso',
                  'fecha_caducidad': 'Fecha de Caducidad',
                  'categoria': 'Categoria',
                  'marca': 'Marca'}
        #Modificar tipo de datos.
        widget = {'product_name': forms.TextInput, 'stock_actual': forms.TextInput,
                  'stock_minimo': forms.TextInput, 'unidad_medida': forms.TextInput,
                  'fecha_ingreso': forms.TextInput, 'fecha_caducidad': forms.TextInput,
                  'categoria': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})
