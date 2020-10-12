from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models.abstracts import UUIDModel
from apps.especialidades.models import Especialidad
from apps.persona.models import Persona


def get_medical_availability_choices():
    ret = []
    for day in settings.MEDICAL_AVAILABILITY_DAYS:
        for shift in settings.MEDICAL_AVAILABILITY_SHIFTS:
            ret.append(("%s_%s" % (day[0], shift[0]), "%s (%s)" % (day[1], shift[1])))
    return ret


class Medico(UUIDModel):
    persona = models.OneToOneField(Persona, verbose_name=_("Persona"), on_delete=models.PROTECT)

    especialidad = models.ForeignKey(Especialidad, verbose_name=_("Especialidad"), on_delete=models.PROTECT)

    biografia = models.TextField(verbose_name=_("Biografía"), blank=True, null=True)

    numero_colegio_medico = models.CharField(
        verbose_name=_("Número de Colegio Médico"), max_length=64, blank=True, null=True
    )

    centro_laboral = models.CharField(verbose_name=_("Centro laboral"), max_length=128, blank=True, null=True)

    experiencia_en_anios = models.PositiveIntegerField(verbose_name=_("Años de experiencia"), blank=True, null=True)

    validado = models.BooleanField(verbose_name=_("¿Validado?"), default=False)

    usuario = models.OneToOneField(
        User, verbose_name=_("Usuario asociado"), on_delete=models.PROTECT, null=True, blank=True,
    )

    creado_en = models.DateTimeField(
        verbose_name=_("Fecha y hora de creación"), auto_now_add=True, null=True, blank=True,
    )

    actualizado_en = models.DateTimeField(verbose_name=_("Fecha y hora de actualización"), null=True, blank=True)

    validado_en = models.DateTimeField(
        verbose_name=_("Fecha y hora de validación"), auto_now_add=True, null=True, blank=True,
    )

    validado_por = models.ForeignKey(
        User,
        verbose_name=_("Usuario validador"),
        on_delete=models.PROTECT,
        related_name="medicos_validados",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("médico")
        verbose_name_plural = _("médicos")

    def __str__(self):
        return self.nombre_completo

    @property
    def nombre_completo(self):
        return f"{self.persona}"


class Disponibilidad(UUIDModel):
    inicio_disponibilidad = models.DateTimeField(_("Inicio del periodo"), null=True, blank=True)

    fin_disponibilidad = models.DateTimeField(_("Fin del periodo"), null=True, blank=True)

    turnos = ArrayField(
        models.CharField(max_length=50, choices=get_medical_availability_choices()), blank=True, null=True
    )

    ejecutado_por = models.ForeignKey(
        Medico, verbose_name=_("Ejecutado por"), related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("disponibilidad")
        verbose_name_plural = _("disponibilidades")

    def __str__(self):
        return ", ".join(self.turnos)
