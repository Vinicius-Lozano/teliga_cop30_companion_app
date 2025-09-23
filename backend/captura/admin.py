from django.contrib import admin
from .models import MochilaItem, MochilaEvento

@admin.register(MochilaItem)
class MochilaItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item', 'captured_at')
    search_fields = ('user__username', 'item__nome')

@admin.register(MochilaEvento)
class MochilaEventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'evento', 'captured_at')
    search_fields = ('user__username', 'evento__titulo')
