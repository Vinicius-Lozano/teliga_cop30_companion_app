from django.db import models

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    # MODIFICADO: De URLField para ImageField para permitir upload
    imagem = models.ImageField(upload_to='eventos_imagens/', blank=True, null=True)
    descricao = models.TextField()
    curiosidades = models.TextField(blank=True, null=True)
    endereco = models.CharField(max_length=200)
    data = models.DateField()
    # NOVO: Campo para o horário do evento
    horario = models.TimeField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    icone = models.CharField(max_length=255, blank=True, null=True)
    imagens_extras = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.titulo