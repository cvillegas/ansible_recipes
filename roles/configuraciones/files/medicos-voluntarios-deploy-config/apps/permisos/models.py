from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models.abstracts import UUIDModel
from apps.persona.models import Persona


class Rol(models.Model):
    id = models.CharField(primary_key=True, verbose_name=_("Id"), max_length=10)

    nombre = models.CharField(verbose_name=_("Origen"), max_length=128)

    home = models.CharField(verbose_name=_("Ruta registrada en django"), max_length=64)

    ruta = models.CharField(verbose_name=_("Ruta absoluta"), max_length=128, null=True)

    avatar = models.ImageField(verbose_name=_("Avatar"), max_length=128, upload_to="Roles/avatar/")

    activo = models.BooleanField(verbose_name=_("¿Activo?"), default=True)

    creada_en = models.DateTimeField(
        verbose_name=_("Fecha y hora de creación"), auto_now_add=True, null=True, blank=True,
    )

    actualizada_en = models.DateTimeField(verbose_name=_("Fecha y hora de actualización"), null=True, blank=True)

    class Meta:
        verbose_name = _("Rol")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return f"{self.nombre}: {self.home}"


class Perfil(UUIDModel):
    usuario = models.ForeignKey(User, verbose_name=_("Usuario"), on_delete=models.PROTECT, blank=True, null=True)

    persona = models.ForeignKey(Persona, verbose_name=_("Persona"), on_delete=models.PROTECT, blank=False, null=False,)

    rol = models.ForeignKey(Rol, verbose_name=_("Rol"), on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        return f"{self.usuario} - {self.persona.numero_documento} - {self.rol}"

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
        unique_together = ("usuario", "rol")
