"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Imports necessários para servir arquivos de mídia em desenvolvimento
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.views.generic.base import RedirectView

def teste_rota(request):
    """View simples que retorna um JSON para testar a conexão com backend."""
    return JsonResponse({"status": "ok", "message": "Conexão com o backend bem-sucedida!"})

urlpatterns = [

    path('', RedirectView.as_view(url='/api/swagger/', permanent=False)),

    path('admin/', admin.site.urls),

    # Rotas de Autenticação (Login, Logout, Registro, etc.)
    # O login (em /api/auth/login/) já retorna os tokens JWT.
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),

    # Rotas da Documentação (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # APPS locais
    path('api/', include('users.urls')),
    path('api/', include('events.urls')),
    path('api/', include('item.urls')),

    # teste rota
    path('api/teste_rota_back/', teste_rota, name='teste_rota_back'),
]

# Adiciona a rota para servir arquivos de mídia quando DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
