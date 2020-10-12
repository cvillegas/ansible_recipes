from django.db import models
from django.utils.translation import ugettext_lazy as _


class EspecialidadManager(models.Manager):
    def as_choices(self):
        choices = []
        for record in self.all():
            choices.append((record.slug, record.nombre))
        return tuple(choices)


class Especialidad(models.Model):

    nombre = models.CharField(verbose_name=_("Categoría"), max_length=64, unique=True)

    slug = models.SlugField(verbose_name=_("Slug"),)

    weight = models.PositiveIntegerField(
        verbose_name=_("Peso"), help_text=_("A mayor peso menor precedencia en el listado"), default=1,
    )

    objects = EspecialidadManager()

    class Meta:
        verbose_name = _("especialidad")
        verbose_name_plural = _("especialidades")
        ordering = (
            "weight",
            "nombre",
        )

    def __str__(self):
        return self.nombre
