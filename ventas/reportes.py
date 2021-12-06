from dataclasses import replace
from itertools import count

from django.db.models import Sum
from past.builtins import xrange

from proveedor.models import ComprasEnc
from .models import FacturaEnc,FacturaDet

from django.shortcuts import render
from django.utils.dateparse import parse_date
from datetime import timedelta, datetime


def imprimir_factura_recibo(request,id):
    template_name="ventas/factura_one.html"

    enc = FacturaEnc.objects.get(id=id)
    det = FacturaDet.objects.filter(factura=id)
    context={
        'request':request,
        'enc':enc,
        'detalle':det,
    }
    return render(request,template_name,context)

def imprimir_factura_list(request,f1,f2):
    template_name="ventas/facturas_print_all.html"

    f1=parse_date(f1)
    f2=parse_date(f2)
    f2=f2 + timedelta(days=1)

    enc = FacturaEnc.objects.filter(fecha__gte=f1,fecha__lt=f2)
    f2=f2 - timedelta(days=1)
    
    context = {
        'request':request,
        'f1':f1,
        'f2':f2,
        'enc':enc
    }

    return render(request,template_name,context)


def GraficoVentas(request):
    data = []
    year = datetime.now().year
    for m in range(1, 13):
        total = FacturaEnc.objects.filter(fecha__year=year, fecha__month=m).aggregate(r=Sum('total')).get('r')
        data.append(total)

    for i in xrange(len(data)):
        if data[i] == None:
            data[i] = 0

    #import pdb;
    #pdb.set_trace()
    return render(request,'ventas/grafico_venta_max.html', {'data':data})


def GraficoCompras(request):
    data = []
    year = datetime.now().year
    for m in range(1, 13):
        total = ComprasEnc.objects.filter(fecha_compra__year=year, fecha_compra__month=m).aggregate(r=Sum('total')).get('r')
        data.append(total)

    for i in xrange(len(data)):
        if data[i] == None:
            data[i] = 0

    #import pdb;
    #pdb.set_trace()
    return render(request,'ventas/grafico_compra_max.html', {'data':data})
