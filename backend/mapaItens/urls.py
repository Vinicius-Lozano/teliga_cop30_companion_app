from django.urls import path
from .views import ItensProximosView

urlpatterns = [
    path('itens_proximos/', ItensProximosView.as_view(), name='itens-proximos'),
]
