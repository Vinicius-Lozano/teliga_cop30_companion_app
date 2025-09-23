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
