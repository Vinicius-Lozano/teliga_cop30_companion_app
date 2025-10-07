from django.urls import path
from .views import (
    MochilaItemListCreateView, MochilaEventoListCreateView,
    QuestaoView, QuestaoAleatoriaView,
    CapturaView, ConfirmarCapturaView, QuestaoPorItemView
)

urlpatterns = [
    path('capturas/items/', MochilaItemListCreateView.as_view(), name='captura-items'),
    path('capturas/eventos/', MochilaEventoListCreateView.as_view(), name='captura-eventos'),

    path('captura/<int:item_id>/', CapturaView.as_view(), name='captura'),
    path('captura/<int:item_id>/confirmar/', ConfirmarCapturaView.as_view(), name='confirmar-captura'),

    path('questao/<int:pk>/', QuestaoView.as_view(), name='questao_view'),
    path('questao/aleatoria/', QuestaoAleatoriaView.as_view(), name='questao-aleatoria'),
    path('questao/item/<int:item_id>/', QuestaoPorItemView.as_view(), name='questao-por-item'),
]
