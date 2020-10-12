import secrets

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import IntegrityError
from django.utils import timezone

from apps.permisos.models import Perfil


class CreateUserException(Exception):
    """Custom exception for creation of user for a doctor"""

    ...


def create_user_for_doctor(medico, current_user):
    """Create a user and send email with password"""
    rol = "MEDIC"  # from fixtures file 'roles.json'
    password = secrets.token_urlsafe(12)

    if medico.persona.contacto is None:
        raise CreateUserException("El médico seleccionado no tiene información de contacto.")

    try:
        user = User.objects.create_user(medico.persona.contacto.correo, password=password)
    except IntegrityError:
        raise CreateUserException("Ya existe un usuario creado con el correo de este médico.") from IntegrityError

    Perfil.objects.create(
        usuario=user, persona=medico.persona, rol_id=rol,
    )

    medico.validado = True
    medico.validado_por_id = str(current_user.pk)
    medico.validado_en = timezone.now()
    medico.save()

    send_mail(
        "Usuario creado",
        f"Su usuario ha sido creado, su contraseña es: {password}",
        "no-reply@medicosvoluntarios.pe",
        [medico.persona.contacto.correo],
        fail_silently=False,
    )
    return user
