#Django
from django.shortcuts import render,redirect
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate
from bases.views import SinPrivilegios
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

#Local
from ventas.models import FacturaEnc, FacturaDet,Cliente, FacturaEnc, FacturaDet, OrdenFacturaEnc, OrdenFacturaDet, Caja
from .forms import ClienteForm, CajaForm, FacturaDetForm
from productos.models import Producto
import productos.views as productos


class ClienteView(SinPrivilegios, generic.ListView):
    model = Cliente
    template_name = "ventas/cliente_list.html"
    context_object_name = "obj"
    permission_required="cmp.view_cliente"


class VistaBaseCreate(SuccessMessageMixin,SinPrivilegios, \
    generic.CreateView):
    context_object_name = 'obj'
    success_message="Registro Agregado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class VistaBaseEdit(SuccessMessageMixin,SinPrivilegios, \
    generic.UpdateView):
    context_object_name = 'obj'
    success_message="Registro Actualizado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ClienteNew(VistaBaseCreate):
    model=Cliente
    template_name="ventas/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("ventas:cliente_list")
    permission_required="ventas.add_cliente"

    def get(self, request, *args, **kwargs):
        print("sobre escribir get")
        
        try:
            t = request.GET["t"]
        except:
            t = None

        print(t)
        
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 't':t})


class ClienteEdit(VistaBaseEdit):
    model=Cliente
    template_name="ventas/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("ventas:cliente_list")
    permission_required="ventas.change_cliente"

    def get(self, request, *args, **kwargs):
        print("sobre escribir get en editar")

        print(request)
        
        try:
            t = request.GET["t"]
        except:
            t = None

        print(t)
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form,t=t)
        print(form_class,form,context)
        return self.render_to_response(context)

class VentaDetEdit(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = "proveedor.view_comprasenc"
    model = FacturaDet
    template_name = "prov/factura_det_form.html"
    context_object_name = 'obj'
    form_class = FacturaDetForm
    success_url = reverse_lazy("ventas:factura_list")
    login_url = 'bases:login'

    #def get_success_url(self):
        #compra_id = self.kwargs['compra_id']
        #return reverse_lazy('proveedor:compras_edit', kwargs={'compra_id': compra_id})

    def form_valid(self, form):
        form.instance.uc = self.request.user
        # print(self.request.user.id)
        return super().form_valid(form)

############# CAJA ################

class CajaView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required="ventas.view_facturaenc"
    model = Caja
    template_name = "ventas/caja_list.html"
    context_object_name = "obj"
    login_url = 'bases:login'


class CajaNew(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = "caja.view_caja"
    Model = Caja
    template_name = "ventas/caja_form.html"
    context_object_name = "obj"
    form_class=ClienteForm
    success_url = reverse_lazy("ventas:caja_list")
    login_url = "bases:login"

    #Para obtener el usuario que esta logueado
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)  

class CajaEdit(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = "caja.change_cliente"
    model = Caja
    template_name = "ventas/caja_form.html"
    context_object_name = "obj"
    form_class=ClienteForm
    success_url = reverse_lazy("ventas:caja_list")
    login_url = "bases:login"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class CajaDel(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = "caja.delete_cliente"
    model = Caja
    template_name = "ventas/caja_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("ventas:caja_list")



@receiver(post_save, sender=FacturaEnc)
def actualizar_caja(sender, instance, **kwargs):
    """
    id_enc = instance.id
    enc = FacturaEnc.objects.get(pk=id_enc)
    today = datetime.now().date()
    caja = Caja.objects.filter(fecha=today)
    caja = list(caja)

    s_total = caja[0].sub_total
    #totalCaja = caja[1].total


    import pdb; pdb.set_trace()

    if (caja.fecha == today):
        caja.sub_total = caja.sub_total + enc.sub_total
        caja.total = caja.apertura + caja.sub_total

    caja.save()
"""


@login_required(login_url="/login/")
@permission_required("ventas.change_cliente",login_url="/login/")
def clienteInactivar(request,id):
    cliente = Cliente.objects.filter(pk=id).first()

    if request.method=="POST":
        if cliente:
            cliente.estado = not cliente.estado
            cliente.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")

class FacturaView(SinPrivilegios, generic.ListView):
    model = FacturaEnc
    template_name = "ventas/factura_list.html"
    context_object_name = "obj"
    permission_required="ventas.view_facturaenc"

    def get_queryset(self):
        user = self.request.user
        # print(user,"usuario")
        qs = super().get_queryset()
        for q in qs:
            print(q.uc,q.id)
        
        if not user.is_superuser:
            qs = qs.filter(uc=user)

        for q in qs:
            print(q.uc,q.id)

        return qs


class OrdenFacturaView(SinPrivilegios, generic.ListView):
    model = OrdenFacturaEnc
    template_name = "ventas/orden_factura_list.html"
    context_object_name = "obj"
    permission_required="ventas.view_facturaenc"

    def get_queryset(self):
        user = self.request.user
        # print(user,"usuario")
        qs = super().get_queryset()
        for q in qs:
            print(q.uc,q.id)
        
        if not user.is_superuser:
            qs = qs.filter(uc=user)

        for q in qs:
            print(q.uc,q.id)

        return qs


@login_required(login_url='/login/')
@permission_required('ventas.change_facturaenc', login_url='bases:sin_privilegios')
def facturas(request,id=None):
    template_name='ventas/facturas.html'

    detalle = {}
    clientes = Cliente.objects.filter(estado=True)
    contexto = {}
    if request.method == "GET":
        enc = FacturaEnc.objects.filter(pk=id).first()
        if id:
            if not enc:
                messages.error(request,'Factura No Existe')
                return redirect("ventas:factura_list")

            usr = request.user
            if not usr.is_superuser:
                if enc.uc != usr:
                    messages.error(request,'Factura no fue creada por usuario')
                    return redirect("ventas:factura_list")

        if not enc:
            encabezado = {
                'id':0,
                'fecha':datetime.today(),
                'cliente':0,
                'sub_total':0.00,
                'descuento':0.00,
                'total': 0.00
            }
            detalle=None
        else:
            encabezado = {
                'id':enc.id,
                'fecha':enc.fecha,
                'cliente':enc.cliente,
                'sub_total':enc.sub_total,
                'descuento':enc.descuento,
                'total':enc.total
            }

        detalle=FacturaDet.objects.filter(factura=enc)
        contexto = {"enc":encabezado,"det":detalle,"clientes":clientes}
        return render(request,template_name,contexto)
    
    if request.method == "POST":
        cliente = request.POST.get("enc_cliente")
        fecha  = request.POST.get("fecha")
        cli=Cliente.objects.get(pk=cliente)

        if not id:
            enc = FacturaEnc(
                cliente = cli,
                fecha = fecha
            )
            if enc:
                enc.save()
                id = enc.id
        else:
            enc = FacturaEnc.objects.filter(pk=id).first()
            if enc:
                enc.cliente = cli
                enc.save()

        if not id:
            messages.error(request,'No Puedo Continuar No Pude Detectar No. de Factura')
            return redirect("ventas:factura_list")
        

        """codigo = request.POST.get("codigo")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        s_total = request.POST.get("sub_total_detalle")
        descuento = request.POST.get("descuento_detalle")
        total = request.POST.get("total_detalle") """

        orden_id = request.POST.get("id_orden")
        detalleOrdenes = OrdenFacturaDet.objects.filter(factura=orden_id)
        detalleOrdenes = list(detalleOrdenes)
       #caja = Caja.objects.all()

        for items in detalleOrdenes:
            cantidad_d = items.cantidad
            precio_d = items.precio
            sub_total_d = items.sub_total
            total_d = items.total
            producto_id = items.producto_id
            prod = Producto.objects.get(pk=producto_id)

            #prod = Producto.objects.get(codigo=codigo)
            det = FacturaDet(
                factura = enc,
                producto = prod,
                cantidad = cantidad_d,
                precio = precio_d,
                sub_total = sub_total_d,
                descuento = 0,
                total = total_d
            )
            
            det.save()

        
        #if det:
         #   det.save()
        
        return redirect("ventas:factura_edit",id=id)

    return render(request,template_name,contexto)

# Vista para buscar la Orden de venta
class OrdenVentaView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = "ventas.view_comprasenc"
    model = OrdenFacturaEnc
    template_name = "ventas/orden_factura_list.html"
    context_object_name = "obj"
    login_url = "bases:login"

# Clase para buscar los productos en la Orden Venta
class ProductoView(productos.ProductoView):
    template_name="ventas/buscar_producto.html" 


# Clase para buscar las ordenes en la Factura Venta
class OrdenView(OrdenVentaView):
    template_name="ventas/buscar_orden_venta.html" 
    #orden = OrdenFacturaEnc.objects.filter(estado=True)
    #contexto = {"orden":orden}

def borrar_detalle_factura(request, id):
    template_name = "ventas/factura_borrar_detalle.html"

    det = FacturaDet.objects.get(pk=id)

    if request.method=="GET":
        context={"det":det}

    if request.method == "POST":
        usr = request.POST.get("usuario")
        pas = request.POST.get("pass")

        user =authenticate(username=usr,password=pas)

        if not user:
            return HttpResponse("Usuario o Clave Incorrecta")
        
        if not user.is_active:
            return HttpResponse("Usuario Inactivo")

            """or user.has_perm("ventas.sup_caja_facturadet")"""

        if user.is_superuser :
            det.id = None
            det.cantidad = (-1 * det.cantidad)
            det.sub_total = (-1 * det.sub_total)
            det.descuento = (-1 * det.descuento)
            det.total = (-1 * det.total)
            det.save()

            return HttpResponse("ok")

        return HttpResponse("Usuario no autorizado")
    
    return render(request,template_name,context)

def ordenInactivar(request,id):
    orden = OrdenFacturaEnc.objects.filter(pk=id).first()

    if request.method=="POST":
        if orden:
            orden.estado = not orden.estado
            orden.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")

def borrar_OrdenDetalle_factura(request, id):
    template_name = "ventas/factura_borrar_Ordendetalle.html"

    det = FacturaDet.objects.get(pk=id)

    if request.method=="GET":
        context={"det":det}

    if request.method == "POST":
        usr = request.POST.get("usuario")
        pas = request.POST.get("pass")

        user =authenticate(username=usr,password=pas)

        if not user:
            return HttpResponse("Usuario o Clave Incorrecta")
        
        if not user.is_active:
            return HttpResponse("Usuario Inactivo")

        if user.is_superuser or user.has_perm("ventas.sup_caja_facturadet"):
            det.id = None
            det.cantidad = (-1 * det.cantidad)
            det.sub_total = (-1 * det.sub_total)
            det.descuento = (-1 * det.descuento)
            det.total = (-1 * det.total)
            det.save()

            return HttpResponse("ok")

        return HttpResponse("Usuario no autorizado")
    
    return render(request,template_name,context)


@login_required(login_url="/login/")
@permission_required("ventas.change_cliente",login_url="/login/")
def cliente_add_modify(request,pk=None):
    template_name="ventas/cliente_form.html"
    context = {}

    if request.method=="GET":
        context["t"]="fc"
        if not pk:
            form = ClienteForm()
        else:
            cliente = Cliente.objects.filter(id=pk).first()
            form = ClienteForm(instance=cliente)
            context["obj"]=cliente
        context["form"] = form
    else:
        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        celular = request.POST.get("celular")
        tipo = request.POST.get("tipo")
        usr = request.user

        if not pk:
            cliente = Cliente.objects.create(
                nombres=nombres,
                apellidos=apellidos,
                celular = celular,
                tipo = tipo,
                uc=usr,
            )
        else:
            cliente = Cliente.objects.filter(id=pk).first()
            cliente.nombres=nombres
            cliente.apellidos=apellidos
            cliente.celular = celular
            cliente.tipo = tipo
            cliente.um=usr.id

        cliente.save()
        if not cliente:
            return HttpResponse("No pude Guardar/Crear Cliente")
        
        id = cliente.id
        return HttpResponse(id)
    
    return render(request,template_name,context)


def orden_facturas(request,id=None):
    template_name='ventas/orden_facturas.html'

    detalle = {}
    contexto = {}
    clientes = Cliente.objects.filter(estado=True)
    facDet = OrdenFacturaEnc.objects.all()
    
    if request.method == "GET":
        enc = OrdenFacturaEnc.objects.filter(pk=id).first()
        if id:
            if not enc:
                messages.error(request,'Factura No Existe')
                return redirect("ventas:orden_factura_list")

            usr = request.user
            if not usr.is_superuser:
                if enc.uc != usr:
                    messages.error(request,'Factura no fue creada por usuario')
                    return redirect("ventas:orden_factura_list")

        if not enc:
            encabezado = {
               'id':0,
               'fecha':datetime.today(),
               'descripcion':0.0, 
            #   'cliente':0,
                'sub_total':0.00,
            #   'descuento':0.00,
                'total': 0.00
            }
            detalle=None
        else:
            encabezado = {
                'id':enc.id,
                'fecha':enc.fecha,
                'descripcion': enc.descripcion,
             #  'cliente':enc.cliente,
                'sub_total':enc.sub_total,
             #   'descuento':enc.descuento,
                'total':enc.total
            }

        detalle=OrdenFacturaDet.objects.filter(factura=enc)
        contexto = {"enc":encabezado,"det":detalle,"clientes":clientes,"facDet":facDet}
        return render(request,template_name,contexto)
    
    if request.method == "POST":
        cliente = request.POST.get("enc_cliente")
        fecha  = request.POST.get("fecha")
        descripcion_enc = request.POST.get("descripcion_enc")
        #cli=Cliente.objects.get(pk=cliente)

        if not id:
            enc = OrdenFacturaEnc(
                #id = enc.id,
                fecha = fecha,
                descripcion = descripcion_enc
            )
            if enc:
                enc.save()
                id = enc.id
        else:
            enc = OrdenFacturaEnc.objects.filter(pk=id).first()
            if enc:
                #enc.c = cli
                enc.fecha = fecha
                enc.save()
            
        if enc:
            enc.save()
            id = enc.id

        if not id:
            messages.error(request,'No Puedo Continuar No Pude Detectar No. de Factura')
            return redirect("ventas:orden_factura_list")
        
        codigo = request.POST.get("codigo")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        s_total = request.POST.get("sub_total_detalle")
        total = request.POST.get("total_detalle")
    
        prod = Producto.objects.get(codigo=codigo)
        import pdb; pdb.set_trace()
        det = OrdenFacturaDet(
            factura = enc,
            producto = prod,
            cantidad = cantidad,
            precio = precio,
            sub_total = s_total,
         #   descuento = descuento,
            total = total
        )
        
        #enc.descripcion = descripcion
        if det:
            det.save()

            sub_total = OrdenFacturaDet.objects.filter(factura=id).aggregate(Sum('sub_total'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.save() 

        return redirect("ventas:orden_factura_edit",id=id)

    return render(request,template_name,contexto)
