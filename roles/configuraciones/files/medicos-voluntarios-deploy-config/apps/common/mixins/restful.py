from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _

from rest_framework.response import Response


class RestfulViewMixin:
    def successful_response(self, message, details=None):
        doc = OrderedDict()
        doc["estado"] = "exito"
        doc["mensaje"] = message
        doc["detalles"] = [] if details is None else details
        return Response(doc)

    def error_response(self, errors, status_code=400):
        doc = OrderedDict()
        doc["estado"] = "error"
        if len(errors) == 1:
            doc["mensaje"] = _("Se ha producido un error")
        elif len(errors) > 0:
            doc["mensaje"] = _("Se han producido múltiples errores")
        doc["detalles"] = errors
        resp = Response(doc)
        resp.status_code = status_code
        return resp
