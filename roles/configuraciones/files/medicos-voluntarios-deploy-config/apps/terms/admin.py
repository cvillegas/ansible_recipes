from django.contrib import admin

from .models import TermsAcceptance

# Register your models here.


class TermsAcceptanceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "related_object",
        "created_at",
    )


admin.site.register(TermsAcceptance, TermsAcceptanceAdmin)
