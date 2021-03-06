# Generated by Django 3.2.5 on 2021-11-14 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0012_rename_precio_venta_producto_precio'),
    ]

    operations = [
        migrations.CreateModel(
            name='AjusteInventario',
            fields=[
                ('producto_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='productos.producto')),
            ],
            options={
                'verbose_name_plural': 'Productos Ajustados',
            },
            bases=('productos.producto',),
        ),
    ]
