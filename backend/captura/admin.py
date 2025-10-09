from django.contrib import admin
from .models import MochilaItem, MochilaEvento, ConversaQuestoes

@admin.register(MochilaItem)
class MochilaItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'captured_at')
    list_filter = ('user', 'captured_at')
    search_fields = ('user__username', 'item__nome')

@admin.register(MochilaEvento)
class MochilaEventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'evento', 'captured_at')
    search_fields = ('user__username', 'evento__titulo')

@admin.register(ConversaQuestoes)
class ConversaQuestoesAdmin(admin.ModelAdmin):
    list_display = ('item', 'pergunta', 'resposta_correta')
    search_fields = ('pergunta', 'item__nome')

