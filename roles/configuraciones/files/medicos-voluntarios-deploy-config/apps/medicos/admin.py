from django.contrib import admin

from .models import Disponibilidad, Medico


class MedicoAdmin(admin.ModelAdmin):

    list_display = ("pk", "especialidad", "numero_colegio_medico")

    list_filter = ("especialidad", "validado")


admin.site.register(Medico, MedicoAdmin)
admin.site.register(Disponibilidad)
