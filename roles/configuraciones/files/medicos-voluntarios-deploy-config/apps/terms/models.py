import json
from collections import OrderedDict

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField


class TermsAcceptanceManager(models.Manager):
    def get_for_model(self, instance, default=None, raise_exception=True):
        params = {}
        params["content_type"] = ContentType.objects.get_for_model(instance)
        params["object_id"] = instance.pk
        try:
            return self.get(**params)
        except self.model.DoesNotExist as e:
            if raise_exception:
                raise e
            return default


class TermsAcceptance(models.Model):

    HEADERS_FOR_CONTEXT = ["HTTP_USER_AGENT", "REMOTE_HOST", "REMOTE_USER"]

    terms_type = models.CharField(verbose_name=_("Tipo de versión"), max_length=64, null=True, blank=True)

    terms_version = models.CharField(verbose_name=_("Versión"), max_length=64, null=True, blank=True)

    ip_address = models.GenericIPAddressField(verbose_name=_("Dirección IP"), blank=True, null=True)

    request_context = JSONField(verbose_name=_("Contexto de la solicitud"), blank=True, null=True)

    content_type = models.ForeignKey(
        ContentType, verbose_name=_("Tipo de contenido"), related_name="pageview_counters", on_delete=models.PROTECT,
    )

    object_id = models.CharField(max_length=36, verbose_name=_("ID del objeto"))

    related_object = GenericForeignKey("content_type", "object_id")

    objects = TermsAcceptanceManager()

    created_at = models.DateTimeField(verbose_name=_("Fecha y hora de creación"), auto_now_add=True)

    class Meta:
        verbose_name = _("aceptación de términos y condiciones")
        verbose_name_plural = _("aceptaciones de términos y condiciones")

    def __str__(self):
        template = _("Aceptación de términos de {instance}")
        return template.format(instante=self.related_object)

    @classmethod
    def create_from_request(cls, request, terms_type=None, instance=None, save=True):
        obj = cls()
        obj.ip_address = request.META["REMOTE_ADDR"]
        context = cls.extract_context_from_request(request)
        obj.request_context = json.dumps(context, indent=4)
        if terms_type:
            version = cls.get_terms_version(terms_type)
        else:
            version = None
        if version:
            obj.terms_version = version
            obj.terms_type = terms_type
        if instance:
            obj.content_type = ContentType.objects.get_for_model(instance)
            obj.object_id = instance.pk
        if save:
            obj.save()
        return obj

    @classmethod
    def extract_context_from_request(cls, request):
        context = OrderedDict()
        for header in cls.HEADERS_FOR_CONTEXT:
            value = request.META.get(header, None)
            if value:
                context[header] = value
        return context

    @classmethod
    def get_terms_version(cls, terms_type):
        mapping = getattr(settings, "CURRENT_TERMS_VERSIONS", None)
        return mapping.get(terms_type, None)
