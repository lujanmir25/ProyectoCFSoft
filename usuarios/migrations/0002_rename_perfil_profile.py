# Generated by Django 3.2.5 on 2021-08-14 18:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Perfil',
            new_name='Profile',
        ),
    ]
