from django.urls import path
from .views import MochilaItemListCreateView, MochilaEventoListCreateView

urlpatterns = [
    path('capturas/items/', MochilaItemListCreateView.as_view(), name='captura-items'),
    path('capturas/eventos/', MochilaEventoListCreateView.as_view(), name='captura-eventos'),
]
