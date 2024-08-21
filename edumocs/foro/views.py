from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from contenido.context_processors import notificaciones
from .models import Pregunta, Respuesta
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RespuestaForm

def foro_view(request):
    preguntas = Pregunta.objects.filter(es_predefinida=True)
    return render(request, 'foro/foro.html', {'preguntas': preguntas})


@login_required
def recibir_pregunta(request):
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')

        pregunta = Pregunta.objects.create(mensaje=mensaje)

        notificar_administradores(pregunta)

        pregunta.notificado = True
        pregunta.save()

        return JsonResponse({'respuesta': 'Tu pregunta ha sido enviada a un administrador. Recibirás una respuesta pronto.'})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def enviar_pregunta(request):
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje').strip()
        pregunta_id = request.POST.get('pregunta_id')

        if pregunta_id:
            pregunta = get_object_or_404(Pregunta, id=pregunta_id)
            respuesta = Respuesta.objects.get(pregunta=pregunta)
            return JsonResponse({'respuesta': respuesta.respuesta})
        else:
            nueva_pregunta = Pregunta.objects.create(mensaje=mensaje)
            # Aquí puedes notificar a los administradores
            return JsonResponse({'respuesta': "Un administrador responderá pronto."})
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)



def notificar_administradores(pregunta):
    administradores = User.objects.filter(is_staff=True)
    
    for admin in administradores:
        # Aquí puedes enviar un correo o simplemente registrar el evento en los logs.
        print(f'Notificando a {admin.username} sobre la pregunta: {pregunta.mensaje}')
    pregunta.notificado = True
    pregunta.save()

@login_required
def ver_notificaciones(request):
    if request.user.is_staff:
        notificaciones = Pregunta.objects.filter(notificada=True, respondida=False)
        return render(request, 'foro/notificaciones.html', {'notificaciones': notificaciones})
    return redirect('inicio')

@login_required
def responder_pregunta(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.pregunta = pregunta
            respuesta.save()
            # Redireccionar o mostrar mensaje de éxito
            return redirect('alguna_vista')
        else:
            # Manejar el caso de formulario inválido
            return render(request, "foro/responder.html", {'form': form, 'pregunta': pregunta})
    else:
        form = RespuestaForm()
    return render(request, "foro/responder.html", {'form': form, 'pregunta': pregunta})



