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
    chance = models.FloatField(default=50.0)
    sucesso = models.SmallIntegerField(default=10)
    fracasso = models.SmallIntegerField(default=-5)
    som = models.URLField(blank=True, null=True)
    animacao = models.URLField(blank=True, null=True)
    karma = models.SmallIntegerField(default=0)
    icone = models.URLField(blank=True, null=True)
    
    
    def aplicar(self, progresso):
        """
        Aplica o efeito da habilidade.
        Exemplo: aumentar chance de captura.
        """
        if self.nome.lower() == "ovo":
            progresso.aumentar_chance(30)
        elif self.nome.lower() == "soco":
            progresso.aumentar_chance(10)
        else:
            progresso.aumentar_chance(5)
        progresso.save()
        return True

    
    def __str__(self):
        return self.nome

class PlayerHabilidade(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habilidades_player')
    habilidade = models.ForeignKey(Habilidade, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(null=True, blank=True, default=None)

    def pode_usar(self):
        return self.quantidade is None or self.quantidade > 0

    def registrar_uso(self):
        if self.quantidade is None:
            return True
        if self.quantidade > 0:
            self.quantidade -= 1
            self.save()
            return True
        return False

