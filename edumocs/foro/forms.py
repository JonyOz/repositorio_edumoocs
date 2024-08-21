from django import forms
from .models import Pregunta, Respuesta

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['nombre_usuario', 'mensaje']

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['respuesta']

