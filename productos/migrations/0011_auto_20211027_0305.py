# Generated by Django 3.2.6 on 2021-10-27 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0010_auto_20211024_2345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='estado_c',
            new_name='estado',
        ),
        migrations.AddField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(default='.', max_length=200),
        ),
        migrations.AddField(
            model_name='producto',
            name='ultima_compra',
            field=models.DateField(blank=True, null=True),
        ),
    ]
