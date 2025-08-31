from rest_framework import generics
from .models import Evento
from .serializers import EventoSerializer

class EventoListView(generics.ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

class EventoDetailView(generics.RetrieveAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    lookup_field = "id"
