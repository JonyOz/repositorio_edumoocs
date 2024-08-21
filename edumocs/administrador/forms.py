from django import forms
from cursos.models import Cursos
from .models import Prueba
from django.forms import ModelForm, ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    template_with_clear = '<br> <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'

class cursosForm(forms.ModelForm):
    class Meta:
        model = Cursos
        fields = ['nombre', 'costo', 'fecha_inicio', 'fecha_termino', 'horas', 'cupos','profesor', 'imagen', 'descripcion' ,'contenido']
        widgets = {
            'imagen': CustomClearableFileInput
        }


class PruebaForm(forms.ModelForm):
    class Meta:
        model = Prueba
        fields = ['nombre','descripcion']
