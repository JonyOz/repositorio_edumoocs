from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime 
import phonenumbers
from ckeditor.fields import RichTextField

class Cursos(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="Clave de Curso")
    nombre = models.CharField(verbose_name="Nombre del Curso",max_length=50, default="")
    costo = models.DecimalField(verbose_name="Precio del Curso",max_digits=10, decimal_places=2, default=0.00)  
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio del Curso",default=timezone.now)
    fecha_termino = models.DateField(verbose_name="Fecha de Finalización del Curso",default=timezone.now)
    horas = models.IntegerField(verbose_name="Total de Horas del Curso",default=0)
    cupos = models.IntegerField(verbose_name="Limite de cupos",default=0)
    cupos_restantes = models.IntegerField(verbose_name="Cupos Restantes",default=0)
    imagen = models.ImageField(null=True,upload_to="fotos",verbose_name="Fotografia")
    descripcion = models.TextField(verbose_name="Descripcion General del Curso",default="")
    profesor = models.CharField( max_length=50,default="Por asignar")
    contenido = RichTextField(verbose_name="Contenido",default="")
    created = models.DateTimeField(blank=True,default=datetime.now)
    updated = models.DateTimeField(blank=True,default=datetime.now)
    preinscripciones_count = models.IntegerField(default=0, verbose_name="Total de Preinscripciones")
    class Meta:
        verbose_name = ("Curso")
        verbose_name_plural = ("Cursos")
        ordering = ["-created"]
    
    def save(self,*args,**kwargs):
        if not self.pk:
            self.cupos_restantes = self.cupos_restantes
        super(Cursos,self).save(*args,**kwargs)

    def __str__(self):
        return self.nombre
    
class Preinscripcion(models.Model):
        nombre = models.CharField(verbose_name="Nombre",max_length=50)
        ciudad = models.CharField(verbose_name ="Ciudad", max_length=30)
        telefono = models.CharField(max_length=10)
        estado = models.CharField(verbose_name= "Estado", max_length=30)
        correo = models.EmailField(max_length=254)
        curso = models.ForeignKey(Cursos,on_delete= models.CASCADE, verbose_name= "Curso")
        created = models.DateTimeField(auto_now_add=True,verbose_name="Registro")
        class Meta:
            verbose_name = ("Preinscripción")
            verbose_name_plural = ("Preinscripciones")
            ordering = ["-created"]

        def clean(self):
            try:
                p = phonenumbers.parse(self.telefono,'MX')
                if not phonenumbers.is_valid_number(p):
                    raise ValidationError ("El numero no es valido")
            except phonenumbers.NumberParseException:
                raise ValidationError("El formato del numero de telefono no es valido")
            super().clean()

        def __str__(self):
            return self.nombre