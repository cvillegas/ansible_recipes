from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField
from rfc3339_validator import validate_rfc3339

from apps.common import constants
from apps.common.validators.identity import validate_dni
from apps.consultas.models import Consulta
from apps.especialidades.models import Especialidad
from apps.persona.models import Persona


class RegistrarConsultaForm(forms.Form):

    origen = forms.ChoiceField(choices=constants.ORIGEN_CHOICES)

    celular = PhoneNumberField(strip=True)

    correo = forms.EmailField(required=False)

    tipodoc = forms.ChoiceField(choices=constants.TIPO_DOCUMENTO_CHOICES)

    numdoc = forms.CharField(strip=True)

    nombres = forms.CharField(strip=True)

    apellidos = forms.CharField(strip=True)

    nacimiento = forms.DateField()

    genero = forms.ChoiceField(choices=constants.GENERO_CHOICES)

    lugar = forms.CharField(strip=True)

    latitud = forms.FloatField(required=False)

    longitud = forms.FloatField(required=False)

    dolencias = forms.CharField(strip=True)

    tiempo_dolencias = forms.CharField(strip=True, required=False)

    medicamentos = forms.CharField(strip=True, required=False)

    fuma = forms.CharField(strip=True, required=False)

    alcohol_o_drogas = forms.CharField(strip=True, required=False)

    especialidad_medica = forms.ChoiceField()

    fecha_creacion = forms.CharField(strip=True)

    def __init__(self, *args, **kwargs):
        super(RegistrarConsultaForm, self).__init__(*args, **kwargs)
        self.fields["especialidad_medica"].choices = Especialidad.objects.as_choices()

    def clean_fecha_creacion(self):
        valor = self.cleaned_data["fecha_creacion"]
        if not validate_rfc3339(valor):
            raise ValidationError(
                _("El valor '%(value)s' no cumple con el formato RFC 3339"), params={"value": valor},
            )

    def clean(self):
        tipodoc = self.cleaned_data.get("tipodoc", None)
        numdoc = self.cleaned_data.get("numdoc", None)
        if tipodoc == "dni":
            validate_dni(numdoc)
        return self.cleaned_data

    def save(self):

        # Crear a la persona
        _, paciente = Persona.objects.create_or_update(
            nombres=self.cleaned_data.get("nombres", None),
            apellido_paterno=self.cleaned_data.get("apellidos", None),
            apellido_materno=self.cleaned_data.get("apellido_materno", None),
            tipo_documento=self.cleaned_data.get("tipodoc", None),
            numero_documento=self.cleaned_data.get("numdoc", None),
            genero=self.cleaned_data.get("genero", None),
            pais_de_origen=self.cleaned_data.get("pais_de_origen", None),
            linkedin=self.cleaned_data.get("linkedin", None),
            whatsapp=self.cleaned_data.get("whatsapp", None),
            correo=self.cleaned_data.get("correo", None),
        )

        # Registrar consulta
        consulta = Consulta()
        consulta.paciente = paciente
        consulta.telefono = self.cleaned_data["celular"]
        consulta.fecha_nacimiento = self.cleaned_data["nacimiento"]
        consulta.lugar = self.cleaned_data["lugar"]
        consulta.latitud = self.cleaned_data.get("latitud", None)
        consulta.longitud = self.cleaned_data.get("longitud", None)
        consulta.origen = self.cleaned_data["origen"]
        consulta.especialidad = Especialidad.objects.get(slug=self.cleaned_data["especialidad_medica"])
        consulta.detalle_dolencias = self.cleaned_data["dolencias"]
        consulta.tiempo_dolencias = self.cleaned_data["tiempo_dolencias"]
        consulta.medicamentos = self.cleaned_data["medicamentos"]
        consulta.fuma = self.cleaned_data["fuma"]
        consulta.drogas = self.cleaned_data["alcohol_o_drogas"]
        consulta.save()

        return consulta
