from django import forms

from .models import Cliente, Caja, FacturaDet

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

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['apertura','sub_total','total']
        labels = {'apertura':"Apertura",'sub_total':"Recaudaciones",'total':"Total"}
        widget = {'apertura':forms.TextInput,'sub_total':forms.TextInput,'total':forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})
        self.fields ['sub_total'].widget.attrs['readonly'] = True
        self.fields ['total'].widget.attrs['readonly'] = True
        #self.fields ['existencia'].widget.attrs['readonly'] = True  

class FacturaDetForm(forms.ModelForm):

    class Meta:
        model = FacturaDet
        fields = ['factura', 'producto', 'cantidad','precio' ,'sub_total', 'descuento', 'total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'from-control'
            })
        self.fields['producto'].widget.attrs['readonly'] = True 
        self.fields['cantidad'].widget.attrs['readonly'] = True
        self.fields['precio'].widget.attrs['readonly'] = False 
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = False
        self.fields['total'].widget.attrs['readonly'] = True