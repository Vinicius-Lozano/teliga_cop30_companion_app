from rest_framework import generics, permissions, views
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Habilidade, PlayerHabilidade
from captura.models import CapturaProgresso
from captura.serializers import CapturaProgressoSerializer
from .serializers import (
    HabilidadeListSerializer,
    PlayerHabilidadeSerializer,
)


# -- ADMIN: CRUD de habilidades gerais -----------------------------------------
class HabilidadesListCreateView(generics.ListCreateAPIView):
    queryset = Habilidade.objects.all()
    serializer_class = HabilidadeListSerializer
    permission_classes = [permissions.IsAdminUser]


class HabilidadesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Habilidade.objects.all()
    serializer_class = HabilidadeListSerializer
    permission_classes = [permissions.IsAdminUser]


# -- JOGADOR: listar habilidades disponíveis ------------------------------------
class CapturaHabilidadesView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, item_id):
        """
        Retorna todas as habilidades existentes, 
        incluindo a quantidade (se houver) para o player logado.
        """
        habilidades = Habilidade.objects.all()
        saida = []

        for h in habilidades:
            player_hab = PlayerHabilidade.objects.filter(
                user=request.user, habilidade=h
            ).first()

            saida.append({
                "id": h.id,
                "nome": h.nome,
                "icone": h.icone,
                "som": h.som,
                "animacao": h.animacao,
                "quantidade": player_hab.quantidade if player_hab else None,
                "usavel": (player_hab is None) or (player_hab.quantidade > 0)
            })

        return Response(saida)


# -- JOGADOR: usar uma habilidade no monstro ------------------------------------
class CapturaView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, item_id):
        progresso, _ = CapturaProgresso.objects.get_or_create(
            user=request.user, item_id=item_id
        )
        serializer = CapturaProgressoSerializer(progresso)
        return Response(serializer.data)

    def post(self, request, item_id):
        habilidade_id = request.data.get("habilidade_id")
        if not habilidade_id:
            return Response({"detail": "Campo 'habilidade_id' é obrigatório."}, status=400)

        habilidade = get_object_or_404(Habilidade, pk=habilidade_id)
        progresso, _ = CapturaProgresso.objects.get_or_create(
            user=request.user, item_id=item_id
        )

        player_hab = PlayerHabilidade.objects.filter(
            user=request.user, habilidade=habilidade
        ).first()

        # checa se ainda tem usos
        if player_hab and not player_hab.pode_usar():
            return Response({"detail": "Sem usos restantes dessa habilidade."}, status=400)


        # aplica a habilidade
        with transaction.atomic():
            sucesso = habilidade.aplicar(progresso)

            # consome 1 uso (se for individual)
            if player_hab:
                ok = player_hab.registrar_uso()
                if not ok:
                    return Response({"detail": "Sem usos restantes dessa habilidade."}, status=400)

        player_hab.refresh_from_db() if player_hab else None
        progresso.refresh_from_db()

        return Response({
            "chance": progresso.chance,
            "habilidade": {
                "id": habilidade.id,
                "quantidade": player_hab.quantidade if player_hab else None
            },
            "todas": [
                {
                    "id": h.id,
                    "nome": h.nome,
                    "quantidade": (
                        PlayerHabilidade.objects.filter(user=request.user, habilidade=h)
                        .first()
                        .quantidade if PlayerHabilidade.objects.filter(user=request.user, habilidade=h).exists() else None
                    )
                }
                for h in Habilidade.objects.all()
            ]
        })

