# Generated by Django 3.2.9 on 2021-11-25 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0017_auto_20211124_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprasenc',
            name='no_factura',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AlterField(
            model_name='comprasenc',
            name='no_timbrado',
            field=models.IntegerField(default=0),
        ),
    ]