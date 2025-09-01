from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Assumindo que sua view para eventos fixos se chama FixedEventViewSet
from .views import EventoViewSet

router = DefaultRouter()

# CORRIGIDO: Registrando a rota 'fixed' para corresponder ao que o frontend espera.
# Isso irá criar a URL /api/events/fixed/
router.register(r'fixed', EventoViewSet, basename='fixed-event')

# Se no futuro você tiver eventos aleatórios com outra ViewSet,
# você pode adicionar outra linha aqui.
# Ex: router.register(r'random', RandomEventViewSet, basename='random-event')

urlpatterns = [
    path('', include(router.urls)),
]