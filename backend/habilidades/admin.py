from django.contrib import admin
from .models import Habilidade, PlayerHabilidade


@admin.register(Habilidade)
class HabilidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)


@admin.register(PlayerHabilidade)
class PlayerHabilidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'habilidade', 'quantidade')
    search_fields = ('user__username', 'habilidade__nome')
    list_filter = ('habilidade',)
