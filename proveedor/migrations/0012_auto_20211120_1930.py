# Generated by Django 3.2.5 on 2021-11-20 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0011_auto_20211113_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprasenc',
            name='cantidad_cuotas',
            field=models.CharField(default='0', max_length=3),
        ),
        migrations.AlterField(
            model_name='pagoproveedor',
            name='cantidad_cuotas',
            field=models.CharField(default='0', max_length=3),
        ),
    ]
