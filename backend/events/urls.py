# backend/events/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventoViewSet, SupabaseUploadView


router = DefaultRouter()
router.register(r'', EventoViewSet, basename='evento')


# Lista de URLs para o app de eventos
urlpatterns = [
    path('upload-image/', SupabaseUploadView.as_view(), name='event-upload-image'),
    path('', include(router.urls)),
]