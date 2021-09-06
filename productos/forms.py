# Django
from django import forms
# Local
from .models import Producto
# La vista llama a este formulario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['product_name', 'unidad_medida',
                   'categoria', 'marca', 'precio_venta']

        labels = {'product_name': "Nombre Producto",
                  'unidad_medida': "Unidad de Medida",
                  'categoria': "Categoria",
                  'marca': "Marca",
                  'precio_venta': 'Precio_venta'}
        #Modificar tipo de datos.
        widget = {'product_name': forms.TextInput, 'unidad_medida': forms.TextInput,
                  'categoria': forms.TextInput, 'precio_venta': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})
