# contenido/context_processors.py

from foro.models import Pregunta

def notificaciones(request):
    if request.user.is_authenticated and request.user.is_staff:
        notificaciones = Pregunta.objects.filter(respondida=False)
        return {
            'notificaciones': notificaciones,
            'notificaciones_count': notificaciones.count()
        }
    return {}
