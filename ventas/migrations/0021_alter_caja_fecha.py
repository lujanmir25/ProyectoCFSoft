# Generated by Django 3.2.9 on 2021-11-26 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0020_alter_facturaenc_no_factura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='fecha',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]