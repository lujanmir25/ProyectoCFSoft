# Generated by Django 3.2.9 on 2021-11-26 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0021_alter_caja_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturaenc',
            name='no_factura',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='facturaenc',
            name='no_timbrado',
            field=models.CharField(default=0, max_length=8),
        ),
    ]