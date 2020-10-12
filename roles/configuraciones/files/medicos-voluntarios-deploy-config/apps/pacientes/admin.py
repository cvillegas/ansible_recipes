from django.contrib import admin


class PacienteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombres",
        "apellidos",
        "tipo_documento",
        "numero_documento",
        "lugar",
    )

    list_filter = ("lugar", "genero")

    search_fields = ("nombres", "apellidos", "numero_documento", "lugar")

    readonly_fields = ("id", "creado_en", "actualizado_en")
