# Generated by Django 3.2.6 on 2021-10-24 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0002_alter_facturadet_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturadet',
            name='descuento',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='facturadet',
            name='sub_total',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='facturadet',
            name='total',
            field=models.FloatField(default=0, null=True),
        ),
    ]