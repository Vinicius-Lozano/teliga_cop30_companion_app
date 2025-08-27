from django.db import models

# Create your models here.
from django.db import models

class Evento(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    data = models.DateField()
    hora = models.TimeField()
    local = models.CharField(max_length=255, blank=True, null=True)