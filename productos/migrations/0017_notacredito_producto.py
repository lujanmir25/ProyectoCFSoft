# Generated by Django 3.2.9 on 2021-12-06 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0016_notacredito'),
    ]

    operations = [
        migrations.AddField(
            model_name='notacredito',
            name='producto',
            field=models.CharField(max_length=50, null=True),
        ),
    ]