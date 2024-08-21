from django.contrib import admin
from .models import Pregunta, Respuesta

class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'mensaje')

class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'respuesta')

admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Respuesta, RespuestaAdmin)
