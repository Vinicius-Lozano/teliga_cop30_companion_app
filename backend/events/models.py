# backend/events/models.py

from django.db import models

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    imagem = models.URLField(max_length=1024, blank=True, null=True)
    descricao = models.TextField()
    curiosidades = models.TextField(blank=True, null=True)
    endereco = models.CharField(max_length=200)
    data = models.DateField()
    horario = models.TimeField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    icone = models.CharField(max_length=255, blank=True, null=True)
    imagens_extras = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.titulo