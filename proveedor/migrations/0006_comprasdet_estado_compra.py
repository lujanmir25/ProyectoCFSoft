# Generated by Django 3.2.5 on 2021-10-18 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0005_comprasdet_comprasenc'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprasdet',
            name='estado_compra',
            field=models.CharField(default='En proceso', max_length=12),
        ),
    ]
