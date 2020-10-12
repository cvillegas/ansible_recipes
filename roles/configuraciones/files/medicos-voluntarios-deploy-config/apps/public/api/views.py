from collections import OrderedDict

from django.conf import settings
from django.urls import reverse

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.mixins.restful import RestfulViewMixin
from apps.common.utils.phonenumbers import add_country_phone_prefix

from .forms import RegistrarConsultaForm
from .permissions import ApiKeyPermission


class DocumentRootAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def __init__(self, *args, **kwargs):
        self.setup_document()
        self.setup_consultas()
        super().__init__(*args, **kwargs)

    def get(self, request):
        return Response(self.doc)

    def setup_document(self):
        self.doc = OrderedDict()

    def get_api_prefix(self):
        return getattr(settings, "API_URL", "http://localhost:8000")

    def add_entry(self, key, value):
        if not (value.startswith("http") or value.startswith("https")):
            value = self.get_api_prefix() + value
        self.doc[key] = value

    def setup_consultas(self):
        self.add_entry("consultas_url", reverse("api:consultas_endpoint"))


class ConsultasAPIView(RestfulViewMixin, APIView):

    permission_classes = [ApiKeyPermission]

    def post(self, request):
        data = self.fix_celular(request.data)
        form = RegistrarConsultaForm(data)
        if form.is_valid():
            consulta = form.save()
            mensaje = f"La consulta #{consulta.pk} se ha creado exitosamente."
            detalles = {"codigo": consulta.codigo}
            return self.successful_response(mensaje, detalles)

        return self.error_response(form.errors)

    def fix_celular(self, data):
        celular = data.get("celular", "")
        celular = add_country_phone_prefix(celular)
        data["celular"] = celular
        return data
