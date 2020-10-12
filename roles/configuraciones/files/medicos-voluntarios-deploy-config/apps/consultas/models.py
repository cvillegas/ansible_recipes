from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from apps.common import constants
from apps.common.models.abstracts import UUIDModel
from apps.especialidades.models import Especialidad
from apps.medicos.models import Medico
from apps.persona.models import Persona

from .utils import consulta_encode_code


class Consulta(UUIDModel):  # pylint: disable=too-many-instance-attributes

    paciente = models.ForeignKey(
        Persona, verbose_name=_("Persona"), on_delete=models.PROTECT, related_name="consultas",
    )

    telefono = PhoneNumberField(verbose_name=_("Teléfono"))

    fecha_nacimiento = models.DateField(verbose_name=_("Fecha de nacimiento"), null=True, blank=True)

    lugar = models.CharField(verbose_name=_("Lugar"), max_length=255)

    origen = models.CharField(verbose_name=_("Origen"), max_length=32, choices=constants.ORIGEN_CHOICES)

    especialidad = models.ForeignKey(
        Especialidad, verbose_name=_("Especialidad"), on_delete=models.PROTECT, related_name="consultas",
    )

    detalle_dolencias = models.TextField(verbose_name=_("Detalle de dolencias"))

    tiempo_dolencias = models.CharField(verbose_name=_("Tiempo de dolencias"), max_length=255, null=True, blank=True)

    medicamentos = models.TextField(verbose_name=_("Medicamentos"), null=True, blank=True)

    fuma = models.TextField(verbose_name=_("¿Fuma?"), null=True, blank=True)

    drogas = models.TextField(verbose_name=_("¿Consume alcohol ó drogas?"), null=True, blank=True)

    medico_asignado = models.ForeignKey(
        Medico,
        verbose_name=_("Médico asignado"),
        on_delete=models.PROTECT,
        related_name="consultas_asignadas",
        null=True,
        blank=True,
    )

    comentarios = models.TextField(verbose_name="Comentarios del médico", null=True, blank=True)

    asignada = models.BooleanField(verbose_name=_("¿Asignada?"), default=False)

    atendida = models.BooleanField(verbose_name=_("¿Atendida?"), default=False)

    latitud = models.FloatField(
        verbose_name=_("Latitud"),
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        null=True,
        blank=True,
    )

    longitud = models.FloatField(
        verbose_name=_("Longitud"),
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        null=True,
        blank=True,
    )

    creada_en = models.DateTimeField(
        verbose_name=_("Fecha y hora de creación"), auto_now_add=True, null=True, blank=True,
    )

    asignada_en = models.DateTimeField(verbose_name=_("Fecha y hora de asignación"), null=True, blank=True)

    atendida_en = models.DateTimeField(
        verbose_name=_("Fecha y hora de atención"), auto_now_add=True, null=True, blank=True,
    )

    actualizada_en = models.DateTimeField(verbose_name=_("Fecha y hora de actualización"), null=True, blank=True)

    class Meta:
        verbose_name = _("consulta")
        verbose_name_plural = _("consultas")

    def __str__(self):
        return f"Consulta #{self.pk}: {self.paciente}"

    @property
    def codigo(self):
        return consulta_encode_code(self.pk)
