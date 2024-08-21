# Create your views here.
from django.shortcuts import get_object_or_404, render,redirect
from cursos.models import Cursos
from .forms import cursosForm
from .forms import PruebaForm
from .models import Prueba
from foro.models import Pregunta
from foro.models import Respuesta
from foro.forms import PreguntaForm
from foro.forms import RespuestaForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def panelPrincipal(request):
    curso = Cursos.objects.all()
    return render(request,'administrador/administrador.html',{'cursos':curso})

@login_required
def listaUsuarios(request):
    # Obtener el usuario que ha iniciado sesión
    usuario = request.user
    # Obtener los detalles del usuario
    usuario_detalles = {
        'nombre': usuario.get_full_name(),
        'correo_electronico': usuario.email,
        'numero_telefono': usuario.profile.telefono if hasattr(usuario, 'profile') else '',
        'fecha_nacimiento': usuario.profile.fecha_nacimiento if hasattr(usuario, 'profile') else '',
        'nombre_usuario': usuario.username,
        'genero': usuario.profile.genero if hasattr(usuario, 'profile') else ''
    }
    return render(request, 'administrador/administrador.html', {'usuario_detalles': usuario_detalles})

def eliminarCurso(request,id,confirmacion='administrador/confirmarEliminacion.html'):
    cursos = get_object_or_404(Cursos,id=id)
    if request.method=='POST':
        cursos.delete()
        curso=Cursos.objects.all()
        return render(request,"administrador/administrador.html",{'cursos':curso})

    return render(request, confirmacion, {'object':cursos})


def altaCurso(request):
    if request.method == 'POST':
        form = cursosForm(request.POST,request.FILES)
        if form.is_valid(): 
            nombre = request.POST['nombre']
            costo = request.POST['costo']
            fecha_ini = request.POST['fecha_inicio']
            fecha_term = request.POST['fecha_termino']
            horas = request.POST['horas']
            cupos = request.POST['cupos']
            imagen = request.FILES['imagen']
            descripcion = request.POST['descripcion']
            contenido = request.POST['contenido']
            profesor = request.POST['profesor']
            
            insert = Cursos(nombre = nombre,costo = costo, fecha_inicio=fecha_ini, fecha_termino=fecha_term,
                            horas=horas,cupos=cupos,imagen=imagen,descripcion=descripcion,profesor=profesor,contenido=contenido)
            insert.save()
            cursos=Cursos.objects.all()
            return render(request,"administrador/continuar.html",{'curso':cursos})
    form = cursosForm()
    return render(request,'administrador/altaCursos.html',{'form':form})

def continuar(request):
    return render(request,'administrador/continuar.html')

from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import views as auth_views

class CustomLoginView(auth_views.LoginView):
    template_name = 'administrador/custom_login.html'

    def dispatch(self, request, *args, **kwargs):
        # Si el usuario ya está autenticado y pertenece al grupo "Administradores"
        if request.user.is_authenticated and request.user.groups.filter(name='Administradores').exists():
            # Redirigir al panel de administrador
            return HttpResponseRedirect(reverse('Administrador'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()

        # Realiza el inicio de sesión
        login(self.request, user)

        # Verifica si el usuario pertenece al grupo "Administradores"
        if user.groups.filter(name='Administradores').exists():
            # Redirige al panel de administrador
            return HttpResponseRedirect(reverse('Administrador'))
        else:
            # Redirige a la página de inicio para otros usuarios
            return HttpResponseRedirect(reverse('Inicio'))


def custom_logout(request):
    logout(request)
    return render(request,'administrador/custom_logout.html')

##################################Editar Cursos, aún en pruebas no tocar###################################################################
def consultarCursoIndividual(request, id):
    curso=Cursos.objects.get(id=id)
    return render(request,"administrador/editarCurso.html",{'curso':curso})


def editarCurso(request, id):
        
        curso = get_object_or_404(Cursos, id=id) 
        form = cursosForm(request.POST,instance=curso)
        if form.is_valid(): 
            
            form.save()
            cursos = Cursos.objects.all()
            return render(request,"administrador/administrador.html",{'cursos':cursos})

        return render(request,"administrador/editarCurso.html",{'curso':curso})

def prueba(request):
    if request.method == 'POST':
        form = PruebaForm(request.POST)
        if form.is_valid(): 
            form.save()
            cursos=Prueba.objects.all()
            return render(request,"administrador/administrador.html",{'curso':cursos})
    form = cursosForm()
    return render(request,'administrador/altaCursos.html',{'form':form})

#########################################################APPS Para mejorar DJango##########################################




def administrador(request):
    cursos = Cursos.objects.all()
    profesor = request.GET.get('profesor')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_termino = request.GET.get('fecha_termino')

    if profesor:
        cursos = cursos.filter(profesor__icontains=profesor)
    if fecha_inicio:
        cursos = cursos.filter(fecha_inicio__gte=fecha_inicio)
    if fecha_termino:
        cursos = cursos.filter(fecha_termino__lte=fecha_termino)
    
    query = request.GET.get("q")
    if query:
        cursos = cursos.filter(nombre__icontains=query)

    return render(request, 'administrador/administrador.html', {'cursos': cursos})




def cursos_populares(request):
    cursos_populares = Cursos.objects.order_by('-preinscripciones_count')[:5]
    return render(request, 'administrador/dashboard.html', {'cursos_populares': enumerate(cursos_populares, start=1)})


def eliminar_seleccionados(request):
    if request.method == 'POST':
        # Obtén la lista de IDs de los cursos seleccionados
        ids = request.POST.getlist('selected_courses')
        if ids:
            # Elimina los cursos con los IDs seleccionados
            Cursos.objects.filter(id__in=ids).delete()
            messages.success(request, "Los cursos seleccionados han sido eliminados exitosamente.")
        else:
            messages.error(request, "No se seleccionaron cursos para eliminar.")
    return redirect('Administrador')

from django.core.paginator import Paginator

def verPreguntas(request):
    pregunta_list = Pregunta.objects.all()
    paginator = Paginator(pregunta_list, 10)  # Muestra 10 preguntas por página

    page_number = request.GET.get('page')
    preguntas = paginator.get_page(page_number)
    return render(request, 'administrador/verPreguntas.html', {'preguntas': preguntas})
# Vista para eliminar preguntas
def eliminar_pregunta(request, id):
    pregunta = get_object_or_404(Pregunta, id=id)
    if request.method == 'POST':
        pregunta.delete()
        messages.success(request, "La pregunta ha sido eliminada exitosamente.")
        return redirect('verPreguntas')
    return render(request, 'administrador/eliminar_pregunta.html', {'pregunta': pregunta})

# Vista para responder preguntas

def responder_pregunta(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    
    if request.method == 'POST':
        respuesta_text = request.POST.get('respuesta')
        es_predefinida = request.POST.get('es_predefinida') == 'on'
        
        # Guardar la respuesta
        Respuesta.objects.create(
            pregunta=pregunta,
            respuesta=respuesta_text,
            respondida_por=request.user
        )
        
        # Actualizar la pregunta como respondida y su estado predefinido
        pregunta.respondida = True
        pregunta.es_predefinida = es_predefinida
        pregunta.save()
        
        return redirect('verPreguntas')
    
    return render(request, 'administrador/responder_pregunta.html', {'pregunta': pregunta})

def tablon(request):
    # Filtra preguntas que no sean predefinidas y que tengan al menos una respuesta
    preguntas_respuestas = Pregunta.objects.filter(es_predefinida=False, respuestas__isnull=False).order_by('-fecha_pregunta')[:10]
    return render(request, 'foro/preguntas.html', {'preguntas_respuestas': preguntas_respuestas})