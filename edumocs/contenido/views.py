from django.shortcuts import render, redirect

# Create your views here.
def navbar(request):
    return render(request,'contenido/BaseNavBar.html')

def inicio(request):
    if request.user.is_authenticated:
        return redirect('Administrador')
    return render(request, 'contenido/inicio.html')

def detalles_cursos(request):
    return render(request,'contenido/detalles_cursos.html')

def acercade(request):
    return render(request,'contenido/acercade.html')

def preguntas(request):
    return render(request,'contenido/preguntas.html')

def foro(request):
    return render(request,'contenido/foro.html')