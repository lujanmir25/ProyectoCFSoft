# Generated by Django 3.2.9 on 2021-11-21 15:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0009_auto_20211121_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='caja',
            name='entrada',
            field=models.BigIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='caja',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='caja',
            name='saldo_actual',
            field=models.BigIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='caja',
            name='salida',
            field=models.BigIntegerField(default=0, null=True),
        ),
    ]
