from django.contrib.auth.models import User
from django.test import TestCase

from apps.common import constants
from apps.medicos.models import Medico
from apps.minsa.utils import create_user_for_doctor
from apps.persona.models import Contacto, Persona


class TargetModelTest(TestCase):
    fixtures = ("especialidades.json", "roles.json")

    def setUp(self) -> None:
        contacto = Contacto.objects.create(correo="pepito@grillo.com", telefono_movil="+51999666333")
        persona = Persona.objects.create(
            contacto=contacto,
            nombres="Pepito",
            apellido_paterno="Grillo",
            apellido_materno="Del campo",
            tipo_documento=constants.TIPO_DOCUMENTO_DNI,
            numero_documento="12341234",
            genero=constants.GENERO_MASCULINO,
        )
        self.medico = Medico.objects.create(
            persona=persona, especialidad_id=1,  # from fixtures file 'especialidades.json'
        )

    def test_create_user(self):
        super_user = User.objects.create_superuser("admin")
        user = create_user_for_doctor(self.medico, super_user)
        self.assertIsNotNone(user)
