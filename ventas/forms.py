from django import forms

from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=['nombres','apellidos','tipo',
            'celular','estado']
        exclude = ['um','fm','uc','fc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })



# La vista llama a este formulario

class OrdenVentaForm(forms.ModelForm):
    class Meta:
        model = OrdenVenta
        fields = ['codigo_ordenV','producto','precio','cantidad']

        labels = {'codigo':'codigo',
                'producto': "Nombre Producto",
                  'precio': 'Precio',
                  'cantidad':'cantidad'}
        # Modificar tipo de datos.
        widget = {'product_name': forms.TextInput, 'precio_venta': forms.TextInput, 'cantidad':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })