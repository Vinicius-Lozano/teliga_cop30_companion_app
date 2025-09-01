from rest_framework import viewsets, permissions
from .models import Evento
from .serializers import EventoSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite leitura para qualquer um, mas escrita apenas para admin.
    """
    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS liberado para todos
        if request.method in permissions.SAFE_METHODS:
            return True
        # POST, PUT, DELETE só para admins
        return request.user and request.user.is_staff

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAdminOrReadOnly]