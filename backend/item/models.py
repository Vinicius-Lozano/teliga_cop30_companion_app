from django.db import models

class Item(models.Model):
    
    class Tipo(models.TextChoices):
        NEN = 'NEN', 'Sem Tipo'
        ANI = 'ANI', 'Animal'
        PLA = 'PLA', 'Planta'
        POC = 'POC', 'Poção'
        
    nome = models.CharField(unique=True, max_length=100)
    descricao = models.TextField(null=True)
    tipo = models.CharField(max_length=3, choices = Tipo.choices, default=Tipo.NEN)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, default=30.0)
    imagem = models.URLField(blank=True, null=True)
    curiosidades = models.TextField(blank=True, null=True)

    bonus_captura = models.IntegerField(
        null=True, 
        blank=True,
        help_text="Bônus de captura em porcentagem. Aplicavel apenas a poções."
    )
    
    def __str__(self):
        return self.nome