from django.contrib import admin

from .models import Perfil, Rol


class RolAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "home",
        "avatar",
    )


admin.site.register(Rol, RolAdmin)
admin.site.register(Perfil)
