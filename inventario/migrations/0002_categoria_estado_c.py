
# Generated by Django 3.2.7 on 2021-10-04 13:27

# Generated by Django 3.2.6 on 2021-10-04 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='estado_c',
            field=models.BooleanField(default=True),
        ),
    ]
