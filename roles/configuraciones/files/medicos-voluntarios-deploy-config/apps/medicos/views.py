from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from apps.common.utils.phonenumbers import add_country_phone_prefix
from apps.consultas.forms import ConsultaForm
from apps.consultas.models import Consulta
from apps.medicos.forms import RegistroForm
from apps.medicos.models import Medico
from apps.terms.models import TermsAcceptance


class TerminosCondicionesView(TemplateView):
    template_name = "medico/terms.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        terms = "dataaaa"
        context.update({"terms": terms})
        return context


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "medico/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil = self.request.perfiles.filter(rol_id="MEDIC").first()

        medico = Medico.objects.get(persona_id=perfil.persona.id)
        pacients = Consulta.objects.filter(especialidad_id=medico.especialidad_id, atendida=False)
        pacientes = pacients.filter(
            medico_asignado_id=self.request.medico.persona.id, atendida=False, asignada=True,
        ) | pacients.filter(especialidad_id=medico.especialidad_id, atendida=False, asignada=False)

        context.update({"medico": medico, "pacientes": pacientes, "perfil": perfil})
        return context


class RegistroView(TemplateView):
    # pylint: disable=unused-argument
    template_name = "medico/registro.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RegistroForm()
        organization = settings.TERMS_ORGANIZATION
        context.update(
            {
                "organization": organization,
                "form": form,
                "days": settings.MEDICAL_AVAILABILITY_DAYS,
                "shifts": settings.MEDICAL_AVAILABILITY_SHIFTS,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        post_data = request.POST.copy()
        fields = ["telefono_movil", "telefono_fijo", "whatsapp"]
        for f in fields:
            post_data[f] = add_country_phone_prefix(post_data.get(f, None))

        form = RegistroForm(post_data)
        if form.is_valid():
            registro = form.save()
            TermsAcceptance.create_from_request(request=request, terms_type="medicos", instance=registro)
            return redirect(reverse("success"))
        context.update({"form": form})
        return self.render_to_response(context)


class ConsultaDetalleView(LoginRequiredMixin, TemplateView):
    template_name = "medico/consulta_detalle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil = self.request.perfiles.filter(rol_id="MEDIC").first()

        medico = Medico.objects.get(persona_id=perfil.persona.id)
        consulta_id = self.kwargs.get("consulta_id")
        consulta = Consulta.objects.get(id=consulta_id)
        form = ConsultaForm(instance=consulta)
        context.update({"consulta": consulta, "medico": medico, "form": form, "perfil": perfil})
        return context
