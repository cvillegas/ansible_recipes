from django.urls import path

from .ajax import update_consulta_paciente

app_name = "consulta"

urlpatterns = [
    path("ajax/update_consulta_paciente/", update_consulta_paciente, name="update_consulta_paciente",),
]
