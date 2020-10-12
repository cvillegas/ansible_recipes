from django.db import IntegrityError, models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from apps.common import constants
from apps.common.models.abstracts import UUIDModel
from apps.common.utils.time import age_in_years


class PacienteManager(models.Manager):
    def create_as_needed(self, update=True, **params):
        try:
            this_object = self.model(**params)
            this_object.save()
            return "new", this_object
        except IntegrityError:
            this_object = self.get(
                tipo_documento=params.get("tipo_documento", "dni"),
                numero_documento=params.get("numero_documento", "xxxxxxxx"),
            )
            # Update fields
            if update:
                fields = ["celular", "lugar", "fecha_nacimiento"]
                for f in fields:
                    value = params.get(f, None)
                    if value is not None:
                        setattr(this_object, f, value)
                this_object.save()
            return "existing", this_object


class Paciente(UUIDModel):

    nombres = models.CharField(verbose_name=_("Nombres"), max_length=128)

    apellidos = models.CharField(verbose_name=_("Apellidos"), max_length=128)

    tipo_documento = models.CharField(
        verbose_name=_("Tipo de documento"), max_length=3, choices=constants.TIPO_DOCUMENTO_CHOICES,
    )

    numero_documento = models.CharField(verbose_name=_("Número de documento"), max_length=64)

    genero = models.CharField(verbose_name=_("Género"), max_length=1, choices=constants.GENERO_CHOICES)

    telefono = PhoneNumberField(verbose_name=_("Teléfono"))

    correo = models.EmailField(verbose_name=_("Correo electrónico"), null=True, blank=True)

    fecha_nacimiento = models.DateField(verbose_name=_("Fecha de nacimiento"), null=True, blank=True)

    lugar = models.CharField(verbose_name=_("Lugar"), max_length=255)

    creado_en = models.DateTimeField(
        verbose_name=_("Fecha y hora de creación"), auto_now_add=True, null=True, blank=True,
    )

    actualizado_en = models.DateTimeField(verbose_name=_("Fecha y hora de actualización"), null=True, blank=True)

    objects = PacienteManager()

    class Meta:
        verbose_name = _("paciente")
        verbose_name_plural = _("paciente")
        unique_together = ("tipo_documento", "numero_documento")

    def __str__(self):
        return self.nombre_completo

    @property
    def nombre_completo(self):
        return f"{self.apellidos}, {self.nombres}"

    @property
    def edad(self):
        return age_in_years(self.fecha_nacimiento)
