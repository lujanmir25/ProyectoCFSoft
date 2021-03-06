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
from collections import Counter 
#from datetime import date
#from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate
from bases.views import SinPrivilegios
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import datetime
from proveedor.models import Proveedor
#from dateutil.parser import *
#Local
from ventas.models import Cliente, FacturaEnc, FacturaDet, OrdenFacturaEnc, OrdenFacturaDet, Caja, ComprasEnc, ComprasDet
from .forms import ClienteForm, CajaForm, FacturaDetForm, FacturaEncForm
from productos.models import Producto, NotaCredito
import productos.views as productos
from proveedor.models import PagoProveedor



class ClienteView(SinPrivilegios, generic.ListView):
    model = Cliente
    template_name = "ventas/cliente_list.html"
    context_object_name = "obj"
    permission_required="cmp.view_cliente"


class VistaBaseCreate(SuccessMessageMixin,SinPrivilegios,
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
    permission_required = "ventas.view_caja"
    Model = Caja
    template_name = "ventas/caja_form.html"
    context_object_name = "obj"
    form_class=CajaForm
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
    form_class=CajaForm
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
        form_FacEnc = FacturaEncForm()
        enc = FacturaEnc.objects.filter(pk=id).first()
        #fecha_ini_timbrado = datetime.date.isoformat(enc.fecha_ini_timbrado)
        #fecha_fin_timbrado = datetime.date.isoformat(enc.fecha_fin_timbrado)
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
                'fecha':datetime.datetime.now(),
                'cliente':0,
                'sub_total':0.00,
                'descuento':0.00,
                'total': 0.00
            }

            detalle=None
        else:
            fecha_ini_timbrado = datetime.date.isoformat(enc.fecha_ini_timbrado)
            fecha_fin_timbrado = datetime.date.isoformat(enc.fecha_fin_timbrado)
            encabezado = {
                'id':enc.id,
                'fecha':enc.fecha,
                'cliente':enc.cliente,
                'no_factura': enc.no_factura,
                'no_timbrado': enc.no_timbrado,
                'fecha_fin_timbrado': fecha_fin_timbrado,
                'fecha_ini_timbrado': fecha_ini_timbrado,
                'sub_total':enc.sub_total,
                'descuento':enc.descuento,
                'total':enc.total
            }
            form_FacEnc = FacturaEncForm(encabezado)

        detalle=FacturaDet.objects.filter(factura=enc)
        
        contexto = {"enc":encabezado,"det":detalle,"clientes":clientes, "form_Fac":form_FacEnc}
        return render(request,template_name,contexto)
    
    if request.method == "POST":
        cliente = request.POST.get("enc_cliente")
        fecha  = request.POST.get("fecha")
        no_factura = request.POST.get("no_factura")
        no_timbrado = request.POST.get("no_timbrado")
        fecha_fin_timbrado = request.POST.get("fecha_fin_timbrado")
        fecha_ini_timbrado = request.POST.get("fecha_ini_timbrado")
        #cli=Cliente.objects.get(pk=cliente)

        if not id:
            cli = Cliente.objects.get(pk=cliente)
            enc = FacturaEnc(
                cliente = cli,
                fecha = fecha,
                no_factura = ('001-'+'002-' + int(str(7 - len(str(no_factura))))*'0' + str(no_factura)),
                no_timbrado = no_timbrado,
                fecha_fin_timbrado = fecha_fin_timbrado,
                fecha_ini_timbrado = fecha_ini_timbrado,
            )

            if enc:
                enc.save()
                id = enc.id
        else:
            enc = FacturaEnc.objects.filter(pk=id).first()
            if enc:
                #enc.cliente = cli
                enc.no_factura = no_factura
                enc.no_timbrado=no_timbrado
                enc.fecha_fin_timbrado = fecha_fin_timbrado
                enc.fecha_ini_timbrado = fecha_ini_timbrado

                enc.save()

        if not id:
            messages.error(request,'No Puedo Continuar No Pude Detectar No. de Factura')
            return redirect("ventas:factura_list")

        orden_id = request.POST.get("id_orden")
        detalleOrdenes = OrdenFacturaDet.objects.filter(factura=orden_id)
        detalleOrdenes = list(detalleOrdenes)
        #prod = FacturaDet.objects.filter(pk=id).first()
       #caja = Caja.objects.all()

        for items in detalleOrdenes:
            #prod = FacturaDet.objects.filter(pk=id).first()
            cantidad_d = items.cantidad
            #desc = prod.producto.descripcion
            precio_d = items.precio
            sub_total_d = items.sub_total
            total_d = items.total
            producto_id = items.producto_id
            prod = Producto.objects.get(pk=producto_id)

            #fecha = datetime.datetime.strptime(enc.fecha, '%d/%m/%y %H:%M:%S')

            #prod = Producto.objects.get(codigo=codigo)
            det = FacturaDet(
                factura = enc,
                fecha_detalle = enc.fecha,
                producto = prod,
                cantidad = cantidad_d,
                precio = precio_d,
                sub_total = sub_total_d,
                descuento = 0,
                total = total_d
            )
            det.save()


        # Calculos para la Caja
        total = OrdenFacturaDet.objects.filter(factura=orden_id).aggregate(Sum('sub_total'))
        cant = Caja.objects.all().count()
        cajalist = Caja.objects.all()
        total_detalle = total["sub_total__sum"]
        saldo = cajalist[cant-1].saldo_actual
        saldo_actual = total_detalle + saldo

        caja = Caja (
            fac = enc,
            descripcion = 'VENTA',
            entrada = total_detalle,
            salida = 0,
            saldo_actual = saldo_actual
        )

        caja.save()
        
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
    template_name = "ventas/factura_borrar_ordenDetalle.html"

    det = OrdenFacturaDet.objects.get(pk=id)

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
            det.total = (-1 * det.total)
            det.save()
            return HttpResponse("ok")
        return HttpResponse("Usuario no autorizado")
    return render(request,template_name,context)

def productos_vendidos(request): 
    from datetime import datetime
    #template_name = "ventas/top_productos_list.html"
    ventas_collection = {}
    ventas = FacturaDet.objects.all()
    if request.method == "POST": 
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin") 
        #Fechas convertidas 
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        ventas_list = list(ventas)
        if fecha_inicio: 
            for v in ventas_list:
                fecha = v.fecha_detalle 
                #id_producto = v.producto.id 
                nombre = v.producto.product_name
                if (fecha_fin >= fecha) and (fecha_inicio <= fecha):
                    if nombre in ventas_collection: 
                        ventas_collection[nombre] += v.cantidad 
                    else: 
                        ventas_collection[nombre] = v.cantidad
    ventas_collection = {k:v for k,v in sorted(ventas_collection.items(), key=lambda item: item[1], reverse= True)}        
    contador = Counter(ventas_collection)
    contador_counter = contador.most_common(5)
    contexto = {'obj': contador_counter}
    #import pdb; pdb.set_trace()
    return render(request,"ventas/top_productos_list.html" ,contexto)

def reporte_ganancias(request): 
    #from datetime import datetime
    import datetime 
    from ventas.models import Caja
    ganancias_collection = {}
    Caja = Caja.objects.all()
    if request.method == "POST": 
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin") 
        fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha_fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        ventas = 0
        compras = 0
        
        Saldo_Caja = list(Caja)
        if fecha_inicio: 
            for v in Saldo_Caja:
                Entro = 0
                fecha = v.fecha
                f1_str = fecha.strftime('%Y-%m-%d')
                fecha = datetime.datetime.strptime(f1_str, "%Y-%m-%d").date()
                Descrip = v.descripcion 
                monto_venta = v.entrada
                monto_compra = v.salida 
                
                if (fecha >= fecha_inicio ) and (fecha <= fecha_fin) :
                    Entro = 1
                    if Descrip == 'VENTA':
                        ventas += monto_venta 
                    if Descrip == 'COMPRA':
                        compras += monto_compra
            Total = ventas - compras
            #import pdb; pdb.set_trace()
            Total_por = round((Total / ventas ) * 100,2)
            ganancias_collection = { 'Ventas = ': ventas, 'Compras = ': compras, 'Ganancia % ': Total_por}
            
    ganancias_collection = {k:v for k,v in sorted(ganancias_collection.items(), key=lambda item: item[1])}

    contexto = {'obj': ganancias_collection}
    
    return render(request,"ventas/reporte_ganancias.html" ,contexto)

def productos_comprados_prov(request): 
    compras_collection = {}
    proveedor_collection = {}
    proveedores = Proveedor.objects.all() 
    if request.method == "POST":  
        prov = request.POST.get("id_proveedor")
        
        compras_all = ComprasEnc.objects.all()
        compras_list = list(compras_all)
        
        for v in compras_list:
            proveedor_id = v.proveedor.cedula
            entro = 0
            if prov == proveedor_id:
                entro = 1
                compra_id = v.id 
                nombre_prov = v.proveedor.nombre+' '+v.proveedor.apellido
                proveedor_collection[prov] = nombre_prov
                comprasDet = ComprasDet.objects.filter(compra = compra_id )
                compras_det_list = list(comprasDet)
                for i in compras_det_list: 
                    nombre_prod = i.producto.product_name 
                    cantidad = i.cantidad
                    if nombre_prod in compras_collection: 
                        compras_collection[nombre_prod] += cantidad 
                    else: 
                        compras_collection[nombre_prod] = cantidad 
        
    compras_collection = {k:v for k,v in sorted(compras_collection.items(), key=lambda item: item[1], reverse= True)}        
    contador = Counter(compras_collection)
    contador_counter = contador.most_common(5)
    contexto = {'obj': contador_counter,'prov':proveedor_collection,'proveedores': proveedores}    
    return render(request,"ventas/reporte_comprados.html" ,contexto)

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


@login_required(login_url='/login/')
@permission_required('fac.change_facturaenc', login_url='bases:sin_privilegios')
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
                'fecha':datetime.datetime.now(),
                'descripcion':0.0, 
                'sub_total':0.00,
                'total': 0.00
            }
            detalle=None
        else:
            encabezado = {
                'id':enc.id,
                'fecha':enc.fecha,
                'descripcion': enc.descripcion,
                'sub_total':enc.sub_total,
                'total':enc.total
            }

        detalle=OrdenFacturaDet.objects.filter(factura=enc)
        contexto = {"enc":encabezado,"det":detalle,"clientes":clientes,"facDet":facDet}
        return render(request,template_name,contexto)
    
    if request.method == "POST":
        fecha  = request.POST.get("fecha")
        descripcion_enc = request.POST.get("descripcion_enc")

        if not id:
            enc = OrdenFacturaEnc(
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
                #enc.descripcion = descripcion_enc
                enc.save()

        if not id:
            messages.error(request,'No Puedo Continuar No Pude Detectar No. de Factura')
            return redirect("ventas:orden_factura_list")
        
        codigo = request.POST.get("codigo")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        s_total = request.POST.get("sub_total_detalle")
        total = request.POST.get("total_detalle")


        producto = Producto.objects.filter(codigo=codigo)
        products_list = list(producto)

        for item in products_list: 
            existencia = item.existencia


        prod = Producto.objects.get(codigo=codigo)
        #import pdb; pdb.set_trace()

        if existencia < float(cantidad) :
            messages.error(request,'No disponemos suficiente existencia')
            return redirect("ventas:orden_factura_list")

        if existencia == 0 :
            messages.error(request,'No disponemos existencia compre por fa')
            return redirect("ventas:orden_factura_list")


        prod = Producto.objects.get(codigo=codigo)

        #import pdb; pdb.set_trace()

        det = OrdenFacturaDet(
            factura = enc,
            producto = prod,
            cantidad = cantidad,
            precio = precio,
            sub_total = s_total,
            total = total
        )
        
         #   descuento = descuento,

        if det:
            det.save()

            sub_total = OrdenFacturaDet.objects.filter(factura=id).aggregate(Sum('sub_total'))
            enc.sub_total = sub_total["sub_total__sum"]
            enc.save() 

        return redirect("ventas:orden_factura_edit",id=id)

    return render(request,template_name,contexto)


def notaCredito(request,id):
    template_name = "ventas/nota_credito_venta.html"
    contexto = {}
    enc = FacturaEnc.objects.filter(pk=id).first()

    if request.method == "GET":
        detalle = FacturaDet.objects.filter(factura=id)
        contexto = {'detalle': detalle}

    if request.method == "POST":
        cantidad = request.POST.get("cantidad")
        codigo  = request.POST.get("codigo")

        #inicializaciones
        producto = Producto.objects.filter(id=int(codigo)).first()
        det = FacturaDet.objects.filter(factura=enc)
        det = list(det)

        for item in det:
            if item.producto.id == int(codigo):
                factura_det = FacturaDet.objects.filter(id=item.id).first()
                #Ajuste de Inventario
                producto.existencia = producto.existencia + int(cantidad)
                producto.save()

                #Ajuste De la Factura
                salida = factura_det.sub_total
                factura_det.cantidad = factura_det.cantidad  - int(cantidad)
                factura_det.sub_total = factura_det.cantidad*factura_det.precio
                #factura_det.save()
                salida = salida - factura_det.sub_total

                #Registro de Caja
                cant = Caja.objects.all().count()
                cajalist = Caja.objects.all()
                saldo = cajalist[cant-1].saldo_actual
                saldo_actual = saldo - salida

                caja = Caja (
                    fac = enc,
                    #fecha = datetime.today(),
                    descripcion = 'Nota de Cr??dito x Venta',
                    entrada = 0,
                    salida = salida,
                    saldo_actual = saldo_actual
                )

                caja.save()

                total = (factura_det.precio*int(cantidad))

                gravada = round(float(total/1.05))
                iva = round((total/21))

                nota = NotaCredito (
                    no_factura = enc.no_factura,
                    producto = producto.product_name,
                    descripcion = 'Nota de Credito x Venta', 
                    cantidad = cantidad,
                    gravada = gravada,
                    iva = iva,
                    precio = factura_det.precio,
                    total = total
                )

                nota.save()
        

    return render(request, template_name,contexto)

def cerrarCaja(request,id):

    if request.method=="POST":
        cant = Caja.objects.all().count()
        cajalist = Caja.objects.all()
        total_detalle = cajalist[cant-1].saldo_actual
        saldo = cajalist[cant-1].saldo_actual
        saldo_actual = saldo - total_detalle 

        caja = Caja (
        descripcion = 'CIERRE DE CAJA',
        entrada = 0,
        salida = total_detalle,
        saldo_actual = saldo_actual
        )

        caja.save()
        return HttpResponse("OK")
