from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import MochilaItem, MochilaEvento
from .serializers import MochilaItemSerializer, MochilaEventoSerializer

class MochilaItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MochilaItemSerializer

    def get_queryset(self):
        return MochilaItem.objects.filter(user=self.request.user).select_related('item')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.validated_data['item']
        captura, created = MochilaItem.objects.get_or_create(user=request.user, item=item)
        out = self.get_serializer(captura)
        return Response(out.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class MochilaEventoListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MochilaEventoSerializer

    def get_queryset(self):
        return MochilaEvento.objects.filter(user=self.request.user).select_related('evento')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        evento = serializer.validated_data['evento']
        captura, created = MochilaEvento.objects.get_or_create(user=request.user, evento=evento)
        out = self.get_serializer(captura)
        return Response(out.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
