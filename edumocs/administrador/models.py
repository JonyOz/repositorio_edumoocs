from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return self.user.username

# Señal para crear o actualizar automáticamente el perfil de usuario cuando el usuario se crea/actualiza
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Prueba(models.Model):
    id=models.AutoField(primary_key=True,verbose_name="clave")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(verbose_name="Descripcion",default="")
    created = models.DateTimeField(blank=True,default=datetime.now)
    updated = models.DateTimeField(blank=True,default=datetime.now)

    