from django.db import models

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    imagem = models.URLField()
    descricao = models.TextField()
    curiosidades = models.TextField(blank=True, null=True)
    endereco = models.CharField(max_length=200)
    data = models.DateField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    icone = models.URLField()
    # imagensExtras armazenadas em lista de URLs
    imagens_extras = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.titulo
