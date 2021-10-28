# Generated by Django 3.2.6 on 2021-10-24 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0003_auto_20211024_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturadet',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='facturadet',
            name='fc',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='facturadet',
            name='fm',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='facturaenc',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='facturaenc',
            name='fc',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='facturaenc',
            name='fm',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='facturadet',
            name='descuento',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='facturadet',
            name='precio',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='facturadet',
            name='sub_total',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='facturadet',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]