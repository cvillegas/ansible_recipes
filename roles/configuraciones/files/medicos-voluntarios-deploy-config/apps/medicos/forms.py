from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django_countries.data import COUNTRIES
from phonenumber_field.formfields import PhoneNumberField

from apps.common import constants
from apps.especialidades.models import Especialidad
from apps.medicos.models import Disponibilidad, Medico, get_medical_availability_choices
from apps.persona.models import Persona


class RegistroForm(forms.Form):

    nombres = forms.CharField(label=_("Nombres"), max_length=128)

    apellido_paterno = forms.CharField(label=_("Apellido paterno"), max_length=128)

    apellido_materno = forms.CharField(label=_("Apellido materno"), max_length=128)

    genero = forms.TypedChoiceField(
        label=_("Género"), choices=constants.GENERO_CHOICES, empty_value="---------", coerce=str,
    )

    tipo_documento = forms.TypedChoiceField(
        label=_("Tipo de documento"), choices=constants.TIPO_DOCUMENTO_CHOICES, empty_value="---------", coerce=str,
    )

    numero_documento = forms.CharField(label=_("Número de documento"), max_length=64)

    pais_de_origen = forms.TypedChoiceField(
        label=_("Nacionalidad"),
        choices=list(COUNTRIES.items()),
        initial=settings.DEFAULT_COUNTRY,
        empty_value="---------",
        coerce=str,
    )

    especialidad = forms.ModelChoiceField(label=_("Especialidad"), queryset=Especialidad.objects.all())

    linkedin = forms.CharField(label=_("LinkedIn"), max_length=200, required=False)

    numero_colegio_medico = forms.CharField(label=_("Nro de colegio médico"), max_length=64)

    centro_laboral = forms.CharField(label=_("Centro laboral"), max_length=128, required=False)

    experiencia_en_anios = forms.IntegerField(label=_("Años de experiencia"), required=False, min_value=0)

    correo = forms.EmailField(label=_("Correo electrónico"))

    telefono_fijo = PhoneNumberField(label=_("Número fijo"), required=False)

    telefono_movil = PhoneNumberField(label=_("Número de celular"), required=True)

    whatsapp = PhoneNumberField(label=_("Número de Whatsapp"), required=False)

    acepto_terminos = forms.BooleanField(label=_("Acepto los términos y condiciones"))

    availability = forms.MultipleChoiceField(label=_("Disponibilidad"), choices=get_medical_availability_choices())

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields["nombres"].widget.attrs = {
            "class": "form-control pl-5",
            "placeholder": "Nombres",
        }
        self.fields["apellido_paterno"].widget.attrs = {
            "class": "form-control pl-5",
            "placeholder": "Apellido paterno",
        }
        self.fields["apellido_materno"].widget.attrs = {
            "class": "form-control pl-5",
            "placeholder": "Apellido materno",
        }
        self.fields["genero"].widget.attrs = {"class": "form-control custom-select pl-5"}
        self.fields["tipo_documento"].widget.attrs = {"class": "form-control custom-select pl-5"}
        self.fields["numero_documento"].widget.attrs = {
            "class": "form-control pl-5",
            "placeholder": "Número de documento",
        }
        self.fields["pais_de_origen"].widget.attrs = {"class": "form-control custom-select pl-5"}
        self.fields["especialidad"].widget.attrs = {"class": "form-control pl-5"}
        self.fields["linkedin"].widget.attrs = {
            "class": "form-control pl-5",
            "placeholder": "URL de tu perfil de LinkedIn",
        }
        self.fields["numero_colegio_medico"].widget.attrs = {
            "class": "form-control pl-5",
            "placeholder": "Número de colegio médico",
        }
        self.fields["centro_laboral"].widget.attrs = {
            "class": "form-control pl-5",
            "placeholder": "Centro laboral",
        }
        self.fields["experiencia_en_anios"].widget.attrs = {
            "class": "form-control pl-5",
            "placeholder": "Años de experiencia",
        }
        self.fields["correo"].widget.attrs = {
            "class": "form-control pl-5",
            "placeholder": "Correo electrónico",
        }
        self.fields["telefono_fijo"].widget.attrs = {
            "class": "form-control pl-5",
            "placeholder": "Teléfono fijo",
        }
        self.fields["telefono_movil"].widget.attrs = {
            "class": "form-control pl-5",
            "placeholder": "Telefono celular",
        }
        self.fields["whatsapp"].widget.attrs = {
            "class": "form-control pl-5",
            "placeholder": "Número de Whatsapp",
        }

    def save(self):

        _, persona = Persona.objects.create_or_update(
            nombres=self.cleaned_data.get("nombres", None),
            apellido_paterno=self.cleaned_data.get("apellido_paterno", None),
            apellido_materno=self.cleaned_data.get("apellido_materno", None),
            tipo_documento=self.cleaned_data.get("tipo_documento", None),
            numero_documento=self.cleaned_data.get("numero_documento", None),
            genero=self.cleaned_data.get("genero", None),
            pais_de_origen=self.cleaned_data.get("pais_de_origen", None),
            linkedin=self.cleaned_data.get("linkedin", None),
            whatsapp=self.cleaned_data.get("whatsapp", None),
            correo=self.cleaned_data.get("correo", None),
            telefono_movil=self.cleaned_data.get("telefono_movil", None),
            telefono_fijo=self.cleaned_data.get("telefono_fijo", None),
        )

        # Create a physician
        medico = Medico.objects.create(
            persona=persona,
            especialidad=self.cleaned_data.get("especialidad", None),
            numero_colegio_medico=self.cleaned_data.get("numero_colegio_medico", None),
            centro_laboral=self.cleaned_data.get("centro_laboral", None),
            experiencia_en_anios=self.cleaned_data.get("experiencia_en_anios", None),
        )

        # Create availability
        Disponibilidad.objects.create(ejecutado_por=medico, turnos=self.cleaned_data.get("availability"))

        return medico
