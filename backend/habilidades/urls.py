from django.urls import path
from .views import HabilidadesListCreateView, HabilidadesRetrieveUpdateDestroyView

app_name = 'habilidades'

urlpatterns = [
    path("habilidade/", HabilidadesListCreateView.as_view(), name="habilidade-list"),
    path("habilidade/<int:pk>/", HabilidadesRetrieveUpdateDestroyView.as_view(), name="habilidade-detail")
]
