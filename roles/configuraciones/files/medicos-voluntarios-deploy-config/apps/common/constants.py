from django.utils.translation import ugettext_lazy as _

TIPO_DOCUMENTO_DNI = "dni"
TIPO_DOCUMENTO_CE = "ce"
TIPO_DOCUMENTO_PASAPORTE = "pa"

TIPO_DOCUMENTO_CHOICES = (
    (TIPO_DOCUMENTO_DNI, _("D.N.I.")),
    (TIPO_DOCUMENTO_CE, _("C.E.")),
    (TIPO_DOCUMENTO_PASAPORTE, _("Pasaporte")),
)

GENERO_MASCULINO = "M"
GENERO_FEMENINO = "F"

GENERO_CHOICES = (
    (GENERO_MASCULINO, _("Masculino")),
    (GENERO_FEMENINO, _("Femenino")),
)

ORIGEN_CONSULTA_WEB = "web"
ORIGEN_CONSULTA_WHATSAPP = "whatsapp"

ORIGEN_CHOICES = (
    (ORIGEN_CONSULTA_WEB, _("Web")),
    (ORIGEN_CONSULTA_WHATSAPP, _("Whatsapp")),
)

PERFIL_CHOICES = (
    (u"PACIE", u"Paciente"),
    (u"MEDIC", u"Medico"),
    (u"MINSA", u"Minsa"),
)
