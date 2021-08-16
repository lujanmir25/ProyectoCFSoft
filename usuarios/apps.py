"""Configuracion de la aplicacion de usuarios """
from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    varbose_name = 'Usuarios'