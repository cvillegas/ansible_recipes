import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_dni(value):
    if not re.match(r"^[0-9]{8}$", value):
        raise ValidationError(
            _("El valor '%(value)s' no es un DNI válido"), params={"value": value},
        )
