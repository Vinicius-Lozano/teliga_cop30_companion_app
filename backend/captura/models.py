from django.conf import settings
from django.db import models
from item.models import Item
from events.models import Evento

class MochilaItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mochila_itens')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='capturado_por')
    captured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')
        ordering = ['-captured_at']

    def __str__(self):
        return f'{self.user} -> {self.item}'


class MochilaEvento(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mochila_eventos')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='capturado_por')
    captured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'evento')
        ordering = ['-captured_at']

    def __str__(self):
        return f'{self.user} -> {self.evento}'


class MochilaPocao(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mochila_pocoes')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='pocoes_capturadas')
    captured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-captured_at']
        verbose_name = 'Mochila - Poção'
        verbose_name_plural = 'Mochilas - Poções'

    def __str__(self):
        return f'{self.user} -> {self.item} (poção)'


class CapturaProgresso(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    chance = models.FloatField(default=0)  # porcentagem (0–100)
    capturado = models.BooleanField(default=False)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'item')

    def aumentar_chance(self, valor):
        """Aumenta a chance de captura sem ultrapassar 100."""
        self.chance = min(100, self.chance + valor)
        self.save()
        return self.chance

    def mudar_chance(self, valor):
        """Modifica a chance sem ultrapassar 0–1."""
        self.chance = max(0, min(1, self.chance + valor))
        self.save()
        return self.chance
    
class ConversaQuestoes(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='conversa_questoes')
    pergunta = models.CharField(max_length=255)
    escolha_a = models.CharField(max_length=100)
    escolha_b = models.CharField(max_length=100)
    escolha_c = models.CharField(max_length=100)
    resposta_correta = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C')],
    )

    def checar_resposta(self, resposta: str) -> bool:
        return resposta.strip().upper() == self.resposta_correta

    def __str__(self):
        return f"Pergunta para {self.item.nome}"

    class Meta:
        ordering = ['id']
        verbose_name = 'Questão de Conversa'
        verbose_name_plural = 'Questões de Conversa'