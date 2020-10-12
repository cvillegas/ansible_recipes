from django.contrib import admin

from .models import Consulta


class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "paciente",
        "especialidad",
        "medico_asignado",
        "asignada",
        "atendida",
    )

    list_filter = ("especialidad", "asignada", "atendida")

    search_fields = (
        "paciente__nombres",
        "paciente__apellidos",
        "paciente__numero_documento",
        "medico_asignado__nombres",
        "medico_asignado__apellido_paterno",
        "medico_asignado__apellido_materno",
        "medico_asignado__numero_documento",
        "medico_asignado__especialidad__nombre",
        "especialidad__nombre",
    )

    readonly_fields = (
        "pk",
        "creada_en",
        "actualizada_en",
        "asignada_en",
        "atendida_en",
    )


admin.site.register(Consulta, ConsultaAdmin)
