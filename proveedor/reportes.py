import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils.dateparse import parse_date
from xhtml2pdf import pisa
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from collections import Counter

from .models import ComprasEnc, ComprasDet, OrdenComprasDet


def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
                return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path


def reporte_compras(request):
        template_path = 'prov/compras_print_all.html'
        today = timezone.now()

        compras = ComprasEnc.objects.all()
        context = {
                'obj': compras,
                'today': today,
                'request': request
        }
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisaStatus = pisa.CreatePDF(
                html, dest=response, link_callback=link_callback)
        # if error then show some funy view
        if pisaStatus.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


def imprimir_compra(request, compras_id):
        template_path = 'prov/compras_print_one.html'
        today = timezone.now()

        enc = ComprasEnc.objects.filter(id=compras_id).first()
        if enc:
                detalle = ComprasDet.objects.filter(compra__id=compras_id)
        else:
                detalle = {}

        context = {
                'detalle': detalle,
                'encabezado': enc,
                'today': today,
                'request': request
        }
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisaStatus = pisa.CreatePDF(
                html, dest=response, link_callback=link_callback)
        # if error then show some funy view
        if pisaStatus.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

def imprimir_compras_rang(request,f1,f2):
        template_name='prov/prueba_compras.html'

        f1=parse_date(f1)
        f2=parse_date(f2)
        f2=f2 + timedelta(days=1)

        enc = ComprasEnc.objects.filter(fecha_compra__gte=f1, fecha_compra__lt=f2)
        f2 = f2 - timedelta(days=1)
        context = {
                'request': request,
                'f1': f1,
                'f2': f2,
                'enc': enc,
        }
        return render(request, template_name, context)


"""def top_compras(request):
        template_name = 'prov/prueba_compras.html'
        orden_id = request.POST.get("id_id_orden_compra")
        detalleOrdenes = OrdenComprasDet.objects.filter(compra=orden_id)
        conteo_compras = {}

        for v in detalleOrdenes:
                if v['producto'] in conteo_compras:
                        conteo_compras[v['producto']] += v['cantidad']
                else:
                        conteo_compras[v['producto']] = v['cantidad']
        conteo_compras = {k: v for k, v in sorted(conteo_compras.items(), key=lambda item: item[1])}

        contador = Counter(conteo_compras)
        #cont = contador.most_common(1)

        return render(template_name,contador)"""

