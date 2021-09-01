from django.db import models

from bases.models import ClaseModelo, ClaseModeloInv


class Categoria(ClaseModelo, ClaseModeloInv):
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripcion de la categoria',
        unique=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    """def save(self):
        self.descripcion = self.descripcion.upper()
        super(Categoria, self).save()"""

    class Meta:
        verbose_name_plural = "Categorias"


class SubCategoria(ClaseModeloInv):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length=100,
        help_text='Descripcion de la categoria',
    )

    def __str__(self):
        return '{}:{}'.format(self.categoria.descripcion, self.descripcion)

    class Meta:
        verbose_name_plural = "Sub Categorias"
        unique_together = ('categoria', 'descripcion')