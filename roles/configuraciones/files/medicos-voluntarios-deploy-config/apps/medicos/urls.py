from django.urls import path

from .views import ConsultaDetalleView, IndexView, RegistroView, TerminosCondicionesView

app_name = "medico"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("terms/", TerminosCondicionesView.as_view(), name="terms"),
    path("medicos/registro/", RegistroView.as_view(), name="registro_de_medicos"),
    path("consulta/<int:consulta_id>/", ConsultaDetalleView.as_view(), name="consulta_detalle",),
]
