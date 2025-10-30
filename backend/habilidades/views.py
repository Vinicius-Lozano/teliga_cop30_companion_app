from rest_framework import generics, permissions
from .models import Habilidade
from .serializers import HabilidadeSerializer

class HabilidadesListCreateView(generics.ListCreateAPIView):
    queryset = Habilidade.objects.all()
    serializer_class = HabilidadeSerializer
    permission_classes = [permissions.IsAdminUser]

class HabilidadesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Habilidade.objects.all()
    serializer_class = HabilidadeSerializer
    permission_classes = [permissions.IsAdminUser]