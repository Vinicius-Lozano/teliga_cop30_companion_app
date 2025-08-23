from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'telefone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'telefone')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'telefone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'telefone', 'is_staff', 'is_active')}
        ),
    )
