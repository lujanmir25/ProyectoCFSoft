# Generated by Django 3.2.9 on 2021-11-26 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0022_auto_20211126_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturaenc',
            name='no_factura',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='facturaenc',
            name='no_timbrado',
            field=models.CharField(max_length=8),
        ),
    ]
