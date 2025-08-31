from django.urls import path
from .views import ItemListView, ItemDetailView

app_name = 'item'

urlpatterns = [
    path('itens/', ItemListView.as_view(), name='item-list'),
    path('item/<int:id>/', ItemDetailView.as_view(), name='item-detail')
]
