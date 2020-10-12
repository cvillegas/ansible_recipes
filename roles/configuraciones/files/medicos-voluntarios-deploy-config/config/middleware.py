from apps.persona.models import Perfil


class InitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session["rol"] = None
        request.persona = None
        request.medico = None

        if request.user.is_authenticated:
            try:
                request.perfiles = Perfil.objects.filter(usuario=request.user)
                if request.perfiles.count() > 0:
                    request.persona = request.perfiles.first().persona
                    request.medico = request.perfiles.filter(rol_id="MEDIC").first()
            except AttributeError:
                request.perfiles = []

        return self.get_response(request)
