from django.urls import path

from .views import IndexView, MedicoDetalleView, MedicoUsuarioAdministrarView

app_name = "minsa"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("medicos/<uuid:medico_uuid>/", MedicoDetalleView.as_view(), name="medico-detalle",),
    path("medicos/<uuid:medico_uuid>/update/", MedicoUsuarioAdministrarView.as_view(), name="medico-usuario-admin",),
]
