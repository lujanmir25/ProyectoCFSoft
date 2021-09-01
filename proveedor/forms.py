from django import forms

# Local
from .models import Proveedor


# La vista llama a este formulario

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['cedula', 'nombre', 'apellido', 'ruc', 'email', 'telefono', 'direccion']
        labels = {'cedula': "Cédula", 'apellido': "Apellido", 'ruc': "RUC", 'email': "Email", 'telefono': "Tel/Cel", 'direccion': "Dirección"}
        widget = {'cedula': forms.TextInput, 'nombre': forms.TextInput, 'apellido': forms.TextInput,'ruc': forms.TextInput, 'email': forms.TextInput, 'telefono': forms.TextInput,'direccion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})