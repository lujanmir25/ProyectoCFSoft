# Generated by Django 3.2.6 on 2021-09-06 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0002_auto_20210906_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='cedula',
            field=models.IntegerField(error_messages={'unique': 'Person with this FirstName already exists.'}, max_length=50, unique=True),
        ),
    ]
