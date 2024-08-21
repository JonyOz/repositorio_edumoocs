from django.db import models
from django.contrib.auth.models import User

class Pregunta(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="Id_Pregunta")
    nombre_usuario = models.CharField(max_length=100 ,default="Usuario")
    mensaje = models.TextField()
    fecha_pregunta = models.DateTimeField(auto_now_add=True)
    es_predefinida = models.BooleanField(default=False)
    respondida = models.BooleanField(default= False)
    notificado = models.BooleanField(default= False)
    created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"Pregunta :{self.mensaje} - Respondida: {self.respondida}"

class Respuesta(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="Id_Respuesta")
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuestas')
    respuesta = models.TextField()
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    respondida_por = models.ForeignKey(User, on_delete=models.SET_NULL,null= True, blank= True)

    def __str__(self):
        return f"Respuesta a la pregunta: {self.pregunta.mensaje}"
    
    
    


