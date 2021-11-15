# Django
from django import forms
# Local
from .models import Producto


# La vista llama a este formulario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo','product_name', 'unidad_medida','existencia','estado',
                  'categoria', 'marca', 'precio']

        labels = {'codigo':'codigo',
                'product_name': "Nombre Producto",
                  'unidad_medida': "Unidad de Medida",
                  'categoria': "Categoria",
                  'marca': "Marca",
                  'precio': 'Precio',
                  'estado': 'estado'}
        # Modificar tipo de datos.
        widget = {'product_name': forms.TextInput,
                  'categoria': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields ['existencia'].widget.attrs['readonly'] = True
        self.fields ['precio'].widget.attrs['readonly'] = True   

class InvProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo','product_name','existencia', 'precio']

        labels = {'codigo':'codigo',
                'product_name': "Nombre Producto",
                  'marca': "Marca",
                  'precio': 'Precio',
                  'estado': 'estado'}
        # Modificar tipo de datos.
        widget = {'product_name': forms.TextInput,'precio_venta': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields ['existencia'].widget.attrs['readonly'] = False