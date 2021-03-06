# Generated by Django 3.2.6 on 2021-09-06 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0005_auto_20210827_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='apellido',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cedula',
            field=models.IntegerField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='ruc',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]
