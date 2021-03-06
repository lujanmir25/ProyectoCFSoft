# Generated by Django 3.2.6 on 2021-08-27 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0003_auto_20210826_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='apellido',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cedula',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombre',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='ruc',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
