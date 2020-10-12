from django.http import JsonResponse
from django.utils import timezone

from apps.consultas.models import Consulta


def update_consulta_paciente(request):
    perfil = request.perfiles.filter(rol_id="MEDIC").first()
    response = {"error": False, "show": False}
    comentarios = request.POST.get("comentarios")
    consulta_id = request.POST.get("con")
    tipo = request.POST.get("tipo")

    try:
        consulta = Consulta.objects.get(id=consulta_id)
        if tipo == "atender":
            es_asignada = True
            es_atendida = False
            consulta.asignada_en = timezone.now()
            response["show"] = True
        elif tipo == "terminar":
            es_asignada = True
            es_atendida = True
            consulta.atendida_en = timezone.now()
        else:
            response = {"error": "Parametro incompatibles!!!"}
            return JsonResponse(response)

        consulta.comentarios = comentarios
        consulta.asignada = es_asignada
        consulta.atendida = es_atendida

        consulta.medico_asignado_id = perfil.persona.medico.id
        consulta.save()
    except Exception as error:  # pylint: disable=broad-except
        response = {"error": f"{error}"}

    return JsonResponse(response)
