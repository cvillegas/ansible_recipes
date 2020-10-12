from django.conf import settings

from baseconv import BaseConverter


def consulta_get_converter():
    return BaseConverter(settings.CONSULTAS_CODE_ALPHABET)


def consulta_encode_code(value):
    value += settings.CONSULTAS_CODE_OFFSET
    converter = consulta_get_converter()
    return converter.encode(value)


def consulta_decode_code(value):
    converter = consulta_get_converter()
    value = converter.decode(value)
    value -= settings.CONSULTAS_CODE_OFFSET
    return value
