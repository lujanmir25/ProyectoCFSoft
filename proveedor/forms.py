from django import forms

# Local
from .models import Proveedor, ComprasEnc, OrdenComprasEnc, PagoProveedor, ComprasDet


# La vista llama a este formulario

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['cedula', 'nombre', 'apellido', 'ruc', 'email', 'telefono', 'direccion']
        labels = {'cedula': "Cédula", 'apellido': "Apellido", 'ruc': "RUC", 'email': "Email", 'telefono': "Tel/Cel",
                  'direccion': "Dirección"}
        widget = {'cedula': forms.TextInput, 'nombre': forms.TextInput, 'apellido': forms.TextInput,
                  'ruc': forms.TextInput, 'email': forms.TextInput, 'telefono': forms.TextInput,
                  'direccion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ComprasEncForm(forms.ModelForm):
    fecha_compra = forms.DateInput()
    fecha_factura = forms.DateInput()

    class Meta:
        model = ComprasEnc
        fields = ['proveedor', 'fecha_compra','cantidad_cuotas' ,'observacion','fecha_ini_timbrado', 'fecha_fin_timbrado',
                  'no_factura', 'no_timbrado' , 'fecha_factura', 'sub_total', 'descuento', 'total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'from-control'
            })
        self.fields['fecha_compra'].widget.attrs['readonly'] = True
        self.fields['fecha_ini_timbrado'].widget.attrs['readonly'] = True
        self.fields['fecha_fin_timbrado'].widget.attrs['readonly'] = True
        self.fields['fecha_factura'].widget.attrs['readonly'] = True
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True


#Formulario orden compra.
class OrdenComprasEncForm(forms.ModelForm):
    fecha_compra = forms.DateInput()
    #fecha_factura = forms.DateInput()

    class Meta:
        model = OrdenComprasEnc
        fields = ['fecha_compra','observacion', 'sub_total', 'descuento', 'total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'from-control'
            })
        self.fields['fecha_compra'].widget.attrs['readonly'] = True
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True

#Formulario Pagos 
class PagoProveedorForm(forms.ModelForm):
    class Meta:
        model = PagoProveedor
        fields = ['compra','proveedor', 'cantidad_cuotas', 'monto_mensual', 'monto_total_pag','estado_cuenta']
        labels = {'compra':'compra','proveedor':'proveedor','cantidad cuotas': 'cantidad_cuotas','monto mensual': 'monto_mensual', 'monto total':'monto_total_pag','estado cuenta':  'estado_cuenta' }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'from-control'
            })
        self.fields['monto_total_pag'].widget.attrs['readonly'] = True

class ComprasDetForm(forms.ModelForm):

    class Meta:
        model = ComprasDet
        fields = ['compra', 'producto', 'cantidad','precio_prv' ,'sub_total', 'descuento', 'total', 'costo','dif_cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'from-control'
            })
        self.fields['producto'].widget.attrs['readonly'] = True
        self.fields['compra'].widget.attrs['readonly'] = True 
        self.fields['cantidad'].widget.attrs['readonly'] = False
        self.fields['precio_prv'].widget.attrs['readonly'] = False 
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = False
        self.fields['total'].widget.attrs['readonly'] = True
        self.fields['costo'].widget.attrs['readonly'] = True