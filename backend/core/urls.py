"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def teste_rota(request):
    """View simples que retorna um JSON para testar a conexão com backend."""
    return JsonResponse({"status": "ok", "message": "Conexão com o backend bem-sucedida!"})

urlpatterns = [
    # APPS locais
    path('', include('users.urls')),
    
    # Redireciona a URL raiz ('/') para a página do Swagger UI
    path('', RedirectView.as_view(url='/api/swagger/', permanent=False)),

    path('admin/', admin.site.urls),

    # Rotas de Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rotas da Documentação (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Rota para teste de conexão
    path('api/teste_rota_back/', teste_rota, name='teste_rota_back'),
]
