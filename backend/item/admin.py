from django.contrib import admin
from django.utils.html import format_html
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'peso', 'latitude', 'longitude') 
    list_filter = ('tipo',)
    search_fields = ('nome', 'descricao')
    readonly_fields = ('imagem_preview',)

    fieldsets = (
        (None, {
            'fields': ('nome', 'tipo','descricao','curiosidades' , 'peso', 'latitude', 'longitude', 'imagem', 'imagem_preview')
        }),
    )

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="100" height="100" />', obj.imagem)
        return "(Sem imagem)"
    imagem_preview.short_description = "Imagem"