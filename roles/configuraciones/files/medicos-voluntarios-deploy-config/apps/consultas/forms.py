from django import forms

from .models import Consulta


class ConsultaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConsultaForm, self).__init__(*args, **kwargs)

        self.fields["comentarios"].widget.attrs = {
            "class": "form-control pl-2",
        }

    class Meta:
        # pylint: disable=modelform-uses-exclude
        # ToDo: Use explicit `fields` instead of excluding many fields
        model = Consulta
        exclude = (
            "id",
            "paciente",
            "persona",
            "telefono",
            "fecha_nacimiento",
            "lugar",
            "origen",
            "especialidad",
            "detalle_dolencias",
            "tiempo_dolencias",
            "fuma",
            "drogas",
            "medico_asignado",
            "medicamentos",
            "asignada",
            "atendida",
            "creada_en",
            "asignada_en",
            "atendida_en",
            "actualizada_en",
        )
