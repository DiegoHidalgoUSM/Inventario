from django.db import models
from django.contrib.auth.models import User
class Carrera(models.Model):
    nombre=models.CharField(max_length=50)
    def __str__(self):
        return self.nombre
class Responsable(models.Model):
    nombre=models.CharField(max_length=50)
    def __str__(self):
        return self.nombre
class Ubicacion(models.Model):
    nombre=models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    Etiqueta = models.CharField(max_length=50)
    Numero_Serie = models.CharField(max_length=50)
    Descripcion_Equipamiento = models.CharField(max_length=50)
    Responsable = models.CharField(max_length=50)
    Carrera = models.CharField(max_length=50)
    Ubicacion = models.CharField(max_length=50)
    Observacion=models.CharField(max_length=50)
    Digitador=models.CharField(max_length=50)


    def __str__(self):
        return self.Descripcion_Equipamiento
# Create your models here.
