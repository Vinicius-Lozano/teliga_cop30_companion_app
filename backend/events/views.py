# backend/events/views.py

from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Evento
from .serializers import EventoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from supabase import create_client, Client
from decouple import config
import time

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite leitura para qualquer um, mas escrita apenas para admin (staff).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class EventoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar, criar, atualizar e deletar Eventos.
    """
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAdminOrReadOnly]

class SupabaseUploadView(APIView):
    """
    Endpoint para fazer upload de uma imagem para o Supabase Storage.
    Apenas administradores (staff) podem acessar este endpoint.
    """
    permission_classes = [IsAdminUser] 

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')

        if not image_file:
            return Response(
                {"error": "Nenhum arquivo de imagem foi enviado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Inicializa o cliente Supabase usando a chave de SERVIÇO 
            supabase_url = config("SUPABASE_URL")
            supabase_key = config("SUPABASE_SERVICE_KEY") 
            supabase: Client = create_client(supabase_url, supabase_key)

            # Cria um nome de arquivo único usando o timestamp para evitar conflitos
            file_ext = image_file.name.split('.')[-1]
            file_name = f"event-{int(time.time())}.{file_ext}"
            bucket_name = "imagens-eventos"

            # Faz o upload do arquivo para o bucket no Supabase
            supabase.storage.from_(bucket_name).upload(
                file=image_file.read(),
                path=file_name,
                file_options={"content-type": image_file.content_type}
            )

            # Obtém a URL pública do arquivo 
            public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
            return Response({"imageUrl": public_url}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Erro no upload para o Supabase: {e}")
            return Response(
                {"error": "Ocorreu um erro interno ao processar o upload."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )