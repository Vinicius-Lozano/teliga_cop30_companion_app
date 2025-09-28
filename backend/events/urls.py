from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventoViewSet

# Cria um roteador padrão
router = DefaultRouter()

# CORREÇÃO: Registra a ViewSet na raiz ('') do app de eventos.
# Isso fará com que as rotas sejam:
# /api/events/ (para a lista de eventos - GET, POST)
# /api/events/{id}/ (para um evento específico - GET, PUT, PATCH, DELETE)
router.register(r'', EventoViewSet, basename='evento')

# Inclui as URLs geradas pelo roteador
urlpatterns = [
    path('', include(router.urls)),
]
