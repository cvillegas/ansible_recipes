from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView

from apps.medicos.models import Medico
from apps.minsa.utils import CreateUserException, create_user_for_doctor


class IndexView(LoginRequiredMixin, ListView):
    model = Medico
    context_object_name = "medicos"
    template_name = "minsa/index.html"
    queryset = Medico.objects.filter(validado=False, validado_por=None, usuario__isnull=True).order_by("creado_en")
    paginate_by = 20


class MedicoDetalleView(LoginRequiredMixin, DetailView):
    model = Medico
    pk_url_kwarg = "medico_uuid"
    context_object_name = "medico"
    template_name = "minsa/medicos_detalle.html"


class MedicoUsuarioAdministrarView(LoginRequiredMixin, View):
    # pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        medico = get_object_or_404(Medico, pk=kwargs.get("medico_uuid"))
        accion = request.POST.get("accion")

        if accion == "aprobar":
            try:
                create_user_for_doctor(medico, request.user)
                messages.success(request, f"Médico aprobado: <b>{medico.nombre_completo}</b>.")
            except CreateUserException as ex:
                messages.warning(request, str(ex))
                return redirect("minsa:medico-detalle", medico_uuid=medico.pk)

        elif accion == "desaprobar":
            messages.warning(request, f"Médico desaprobado: <b>{medico.nombre_completo}</b>.")
        else:
            messages.info(request, f"Acción <b>{accion}</b> no reconocida.")
        return redirect("minsa:index")
