from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from apps.common import constants
from apps.common.models.abstracts import UUIDModel


class PersonaManager(models.Manager):
    def create_or_update(self, update=True, **params):
        try:
            person = self.get(
                tipo_documento=params.get("tipo_documento", "dni"),
                numero_documento=params.get("numero_documento", "xxxxxxxx"),
            )

            # Update
            if update:
                # Updating Persona fields
                fields = [
                    "nombres",
                    "apellido_paterno",
                    "apellido_materno",
                    "genero",
                    "pais_de_origen",
                ]
                for f in fields:
                    value = params.get(f, None)
                    if value is not None:
                        setattr(person, f, value)
                person.save()

                # Updating Contacto fields
                contact = person.contacto
                fields = [
                    "linkedin",
                    "facebook",
                    "correo",
                    "telefono_fijo",
                    "telefono_movil",
                ]
                for f in fields:
                    value = params.get(f, None)
                    if value is not None:
                        setattr(contact, f, value)
                contact.save()

            return ("existing", person)

        except self.model.DoesNotExist:

            # Create a person
            person = Persona(
                nombres=params.get("nombres", None),
                apellido_paterno=params.get("apellido_paterno", None),
                apellido_materno=params.get("apellido_materno", None),
                tipo_documento=params.get("tipo_documento", None),
                numero_documento=params.get("numero_documento", None),
                genero=params.get("genero", None),
                pais_de_origen=params.get("pais_de_origen", None),
            )
            person.save()

            # Create contact record
            contact = Contacto(
                linkedin=params.get("linkedin", None),
                whatsapp=params.get("whatsapp", None),
                correo=params.get("correo", None),
                telefono_fijo=params.get("telefono_fijo", None),
                telefono_movil=params.get("telefono_movil", None),
            )
            contact.save()

            # Associate contacto record with person
            person.contacto = contact
            person.save()

            return ("new", person)


class Contacto(UUIDModel):
    linkedin = models.URLField(verbose_name=_("Perfil en LikedIn"), blank=True, null=True)

    facebook = models.URLField(verbose_name=_("Perfil en Facebook"), blank=True, null=True)

    whatsapp = PhoneNumberField(verbose_name=_("Número Whatsapp"), null=True, blank=True,)

    correo = models.EmailField(verbose_name=_("Correo electrónico"), blank=False, null=False)

    telefono_fijo = PhoneNumberField(verbose_name=_("Teléfono fijo"), null=True, blank=True,)

    telefono_movil = PhoneNumberField(verbose_name=_("Teléfono móvil"), null=True, blank=True,)

    class Meta:
        verbose_name = _("contacto")
        verbose_name_plural = _("contactos")

    def __str__(self):
        return self.correo


class Persona(UUIDModel):
    contacto = models.OneToOneField(
        Contacto, verbose_name=_("Contactos"), on_delete=models.PROTECT, blank=True, null=True,
    )

    nombres = models.CharField(verbose_name=_("Nombres"), max_length=128)

    apellido_paterno = models.CharField(verbose_name=_("Apellido paterno"), max_length=128)

    apellido_materno = models.CharField(verbose_name=_("Apellido materno"), max_length=128, null=True, blank=True)

    tipo_documento = models.CharField(
        verbose_name=_("Tipo de documento"), max_length=3, choices=constants.TIPO_DOCUMENTO_CHOICES,
    )

    numero_documento = models.CharField(verbose_name=_("Número de documento"), max_length=64)

    genero = models.CharField(verbose_name=_("Género"), max_length=1, choices=constants.GENERO_CHOICES)

    pais_de_origen = CountryField(verbose_name=_("País de orígen"), null=True, blank=True)

    creado_en = models.DateTimeField(
        verbose_name=_("Fecha y hora de creación"), auto_now_add=True, null=True, blank=True,
    )

    actualizado_en = models.DateTimeField(verbose_name=_("Fecha y hora de actualización"), null=True, blank=True)

    objects = PersonaManager()

    class Meta:
        ordering = ["apellido_paterno", "apellido_materno", "nombres"]
        verbose_name = _("persona")
        verbose_name_plural = _("personas")
        unique_together = ("tipo_documento", "numero_documento")

    def __str__(self):
        return self.nombre_completo

    @property
    def nombre_completo(self):
        if not self.apellido_materno:
            self.apellido_materno = ""
        return f"{self.apellido_paterno} {self.apellido_materno} {self.nombres}"


class Perfil(UUIDModel):
    usuario = models.ForeignKey(
        User, verbose_name=_("Usuario"), on_delete=models.PROTECT, blank=True, null=True, related_name="usuario",
    )

    persona = models.ForeignKey(Persona, on_delete=models.PROTECT, blank=False, null=False, related_name="persona",)

    perfil = models.CharField(verbose_name=_("Tipo de perfil"), max_length=5, choices=constants.PERFIL_CHOICES)

    def __str__(self):
        return f"{self.usuario} - {self.persona.numero_documento} - {self.perfil}"

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
        unique_together = ("usuario", "perfil")
