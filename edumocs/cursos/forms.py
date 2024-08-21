from django import forms
from .models import Preinscripcion

class PreinscripcionesForm (forms.ModelForm):
    class Meta: 
        model = Preinscripcion
        fields = ['nombre','ciudad','telefono','estado','correo']