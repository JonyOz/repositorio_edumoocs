"""
URL configuration for edumocs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from contenido import views
from cursos import views as views_cursos
from administrador import views as viewsAdmin
from foro import views as viewsForo
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio ,name="Inicio"),
    path('cursos/',views_cursos.cursosPrincipal,name="Cursos"),
    path('acercade/',views.acercade,name="Acercade"),
    
    path('foro/',viewsForo.foro_view,name="Foro"),
    path('eliminarCursos/<int:id>/',viewsAdmin.eliminarCurso,name='Eliminar'),
    path('administrador/',viewsAdmin.panelPrincipal,name="Administrador"),
    path('cursoEditado/<int:id>/',viewsAdmin.editarCurso,name='Editar'),
    path('editarCurso/<int:id>/',viewsAdmin.consultarCursoIndividual,name='ConsultaIndividual'),
    path('altaCursos/',viewsAdmin.altaCurso,name='Alta'),
    path('continuar/',viewsAdmin.continuar,name='Continuar'),
    path('cursoContenido/<int:id>/',views_cursos.cursoContenido,name = 'CursoContenido'),
    path('preinscripcion/<int:curso_id>/',views_cursos.preinscripcion,name = 'Preinscripcion'),
    path('login/', viewsAdmin.CustomLoginView.as_view(), name='login'),
    path('filtros.html',viewsAdmin.administrador,name='Filtros'),
    path('preinscripcion/',views_cursos.preinscripcion,name = 'Preinscripcion'),
    path('logout/', viewsAdmin.custom_logout, name='Logout'),
    path('login/', viewsAdmin.CustomLoginView.as_view(), name='Login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('responder/<int:pregunta_id>', viewsForo.responder_pregunta, name='responder_pregunta'),
    path('confirmacion/',views_cursos.confirmacion,name='confirmacion'),
    path('no_cupos/',views_cursos.no_cupos,name='no_cupos'),
    path('enviar_pregunta/', viewsForo.enviar_pregunta, name='enviar_pregunta'),
    path('dashboard/', viewsAdmin.cursos_populares, name='Dashboard'),
    path('busqueda/', views_cursos.busqueda, name='Buscar'),
    path('eliminar-seleccionados/', viewsAdmin.eliminar_seleccionados, name='eliminar_seleccionados'),
    path('tablon/',viewsAdmin.tablon,name="Tablon"),
    path('preguntas/', viewsAdmin.verPreguntas, name='verPreguntas'),
    path('preguntas/eliminar/<int:id>/', viewsAdmin.eliminar_pregunta, name='eliminar_pregunta'),
    path('preguntas/responder/<int:pregunta_id>/', viewsAdmin.responder_pregunta, name='responder_pregunta'),

] 

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    
