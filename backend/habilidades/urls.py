from django.urls import path
from .views import (
    HabilidadesListCreateView,
    HabilidadesRetrieveUpdateDestroyView,
    CapturaView,
    CapturaHabilidadesView
)

app_name = 'habilidades'

urlpatterns = [
    path("habilidade/", HabilidadesListCreateView.as_view(), name="habilidade-list"),
    path("habilidade/<int:pk>/", HabilidadesRetrieveUpdateDestroyView.as_view(), name="habilidade-detail"),
    path("<int:item_id>/", CapturaView.as_view(), name="captura-detail"),
    path("<int:item_id>/habilidades/", CapturaHabilidadesView.as_view(), name="captura-habilidades"),
]
