from django.db import models
from django.conf import settings

class Habilidade(models.Model):
    
    class Tipo(models.TextChoices):
        AGR = 'AGR', 'Agressivo'
        NEU = 'NEU', 'Neutro'
        AMG = 'AMG', 'Amigavel'
        IND = 'IND', 'Indefinido'
        
    tipo = models.CharField(max_length=3, choices= Tipo.choices, default=Tipo.IND)
    nome = models.CharField(unique=True, max_length=20)
    chance = models.FloatField(default=0.5)
    sucesso = models.SmallIntegerField(default=10)
    fracasso = models.SmallIntegerField(default=-5)
    som = models.URLField(blank=True, null=True)
    animacao = models.URLField(blank=True, null=True)
    karma = models.SmallIntegerField(default=0)
    icone = models.URLField(blank=True, null=True)
    
    
    def aplicar(self, progresso):
        """
        Aplica a habilidade ao progresso de captura.
        - Usa self.chance como probabilidade de sucesso entre 0 e 100 (%)
        - Se sucesso, aumenta a chance em self.sucesso
        - Se fracasso, aumenta em self.fracasso (normalmente negativo)
        """
        import random
        if random.random() * 100 <= self.chance:
            progresso.aumentar_chance(self.sucesso)
            return True
        else:
            progresso.aumentar_chance(self.fracasso)
            return False

    
    def __str__(self):
        return self.nome

class PlayerHabilidade(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mochila_eventos')
    habilidade = models.ForeignKey(Habilidade, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(null=True, blank=True, default=None)

    def pode_usar(self):
        return self.quantidade is None or self.quantidade > 0

    def registrar_uso(self):
        if self.quantidade is not None and self.quantidade > 0:
            self.quantidade -= 1
            self.save()
