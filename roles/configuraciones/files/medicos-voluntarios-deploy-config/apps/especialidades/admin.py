from django.contrib import admin

from .models import Especialidad


class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "slug")

    prepopulated_fields = {
        "slug": ("nombre",),
    }


admin.site.register(Especialidad, EspecialidadAdmin)
