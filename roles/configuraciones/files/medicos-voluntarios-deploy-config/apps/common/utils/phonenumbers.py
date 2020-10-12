from django.conf import settings


def add_country_phone_prefix(value):
    if isinstance(value, str) and len(value.strip()) > 0 and not value.startswith("+"):
        return settings.PHONENUMBER_COUNTRY_PREFIX + value
    return value
