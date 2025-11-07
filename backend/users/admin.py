from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    model = Usuario
    list_display = (
        'username',
        'email',
        'telefone',
        'genero',
        'karma',
        'is_staff',
        'is_active'
    )
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'telefone')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {
            'fields': ('email', 'genero', 'data_nas', 'telefone', 'karma')
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'genero',
                'data_nas',
                'telefone',
                'karma',
                'is_active',
                'is_staff'
            ),
        }),
    )
