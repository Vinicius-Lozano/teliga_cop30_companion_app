from django.urls import path
from .views import (
    MochilaItemListCreateView, MochilaEventoListCreateView, MochilaPocaoListCreateView,
    QuestaoView, QuestaoAleatoriaView,
    CapturaView, ConfirmarCapturaView, QuestaoPorItemView,

    # --- IMPORTS NOVOS ---
    MochilaFaunaListView, MochilaFloraListView, MochilaItensListView 
)

urlpatterns = [
    # --- URLS NOVAS ---
    path('capturas/fauna/', MochilaFaunaListView.as_view(), name='captura-fauna'),
    path('capturas/flora/', MochilaFloraListView.as_view(), name='captura-flora'),
    path('capturas/itens/', MochilaItensListView.as_view(), name='captura-itens'), 
    
    # --- URLS ANTIGAS ---
    # path('capturas/items/', MochilaItemListCreateView.as_view(), name='captura-items'), # Comentada
    path('capturas/eventos/', MochilaEventoListCreateView.as_view(), name='captura-eventos'),
    path('capturas/pocoes/', MochilaPocaoListCreateView.as_view(), name='captura-pocoes'),

    # URL para ADICIONAR item (caso ainda precise)
    path('capturas/add-item/', MochilaItemListCreateView.as_view(), name='add-item'),

    path('captura/<int:item_id>/', CapturaView.as_view(), name='captura'),
    path('captura/<int:item_id>/confirmar/', ConfirmarCapturaView.as_view(), name='confirmar-captura'),

    path('questao/<int:pk>/', QuestaoView.as_view(), name='questao_view'),
    path('questao/aleatoria/', QuestaoAleatoriaView.as_view(), name='questao-aleatoria'),
    path('questao/item/<int:item_id>/', QuestaoPorItemView.as_view(), name='questao-por-item'),
]