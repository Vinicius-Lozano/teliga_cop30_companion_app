from django.contrib import admin
from .models import Evento

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "descricao", "latitude", "longitude", "data", "icone")
    search_fields = ("titulo", "descricao")
    list_filter = ("data",)
