# Generated by Django 3.2.9 on 2021-11-21 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0015_remove_facturadet_caja'),
    ]

    operations = [
        migrations.AddField(
            model_name='caja',
            name='fac',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.facturaenc'),
        ),
    ]
