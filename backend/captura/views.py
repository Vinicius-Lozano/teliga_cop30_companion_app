from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.views import APIView
from habilidades.models import Habilidade
import random
from captura.models import Captura, CapturaProgresso, MochilaItem, MochilaEvento, MochilaPocao, ConversaQuestoes
from drf_spectacular.utils import extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from item.models import Item
from .serializers import (
    MochilaItemSerializer, MochilaEventoSerializer, MochilaPocaoSerializer,
    ConversaQuestoesSerializer, RespostaSerializer
)


class MochilaFaunaListView(generics.ListAPIView):
    """ Retorna apenas os itens do tipo 'Animal' (Fauna) da mochila """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MochilaItemSerializer

    def get_queryset(self):
        return MochilaItem.objects.filter(
            user=self.request.user, 
            item__tipo=Item.Tipo.ANI
        ).select_related('item')


class MochilaFloraListView(generics.ListAPIView):
    """ Retorna apenas os itens do tipo 'Planta' (Flora) da mochila """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MochilaItemSerializer

    def get_queryset(self):
        return MochilaItem.objects.filter(
            user=self.request.user, 
            item__tipo=Item.Tipo.PLA
        ).select_related('item')


class MochilaItensListView(generics.ListAPIView):
    """ Retorna apenas itens 'Sem Tipo' (NEN) da mochila """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MochilaItemSerializer

    def get_queryset(self):
        return MochilaItem.objects.filter(
            user=self.request.user,
            item__tipo=Item.Tipo.NEN
        ).select_related('item')


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
        mochila, created = MochilaEvento.objects.get_or_create(user=request.user, evento=evento)
        out = self.get_serializer(mochila)
        return Response(out.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class MochilaPocaoListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MochilaPocaoSerializer 

    def get_queryset(self):
        return MochilaPocao.objects.filter(
            user=self.request.user, 
            item__tipo=Item.Tipo.POC
        ).select_related('item')

    def create(self, request, *args, **kwargs):
        pocao_id = request.data.get('pocao_id') or request.data.get('item_id')
        if not pocao_id:
            return Response({"detail": "Campo 'pocao_id' ou 'item_id' é obrigatório."},
                            status=status.HTTP_400_BAD_REQUEST)

        item = get_object_or_404(Item, pk=pocao_id, tipo=Item.Tipo.POC)

        mochila_pocao, created = MochilaPocao.objects.get_or_create(user=request.user, item=item)


        out = self.get_serializer(mochila_pocao)
        return Response(out.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class QuestaoView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=ConversaQuestoesSerializer)
    def get(self, request, pk):
        questao = get_object_or_404(ConversaQuestoes, pk=pk)
        serializer = ConversaQuestoesSerializer(questao)
        return Response(serializer.data)

    @extend_schema(request=RespostaSerializer)
    def post(self, request, pk):
        questao = get_object_or_404(ConversaQuestoes, pk=pk)
        serializer = RespostaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resposta = serializer.validated_data['resposta']
        acertou = questao.checar_resposta(resposta)
        return Response({
            "id": questao.id,
            "pergunta": questao.pergunta,
            "acertou": acertou,
            "resposta_correta": questao.resposta_correta if not acertou else None
        })


class QuestaoAleatoriaView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        questao = ConversaQuestoes.objects.order_by("?").first()
        if not questao:
            return Response({"error": "Nenhuma questão cadastrada."}, status=404)
        serializer = ConversaQuestoesSerializer(questao)
        return Response(serializer.data)


class QuestaoPorItemView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, item_id):
        questao = ConversaQuestoes.objects.filter(item_id=item_id).order_by("?").first()
        if not questao:
            return Response({"error": "Nenhuma questão disponível para este item."}, status=404)
        serializer = ConversaQuestoesSerializer(questao)
        return Response(serializer.data)



@method_decorator(csrf_exempt, name='dispatch')
class CapturaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, item_id):
        """Retorna o progresso atual do jogador com relação ao item."""
        item = get_object_or_404(Item, id=item_id)

        progresso, _ = CapturaProgresso.objects.get_or_create(
            user=request.user,
            item=item,
            defaults={"chance": 0, "capturado": False}
        )

        return Response({
            "item_id": item.id,
            "chance": progresso.chance,
            "capturado": progresso.capturado
        })

    def post(self, request, item_id):
        """Aplica uma habilidade ou ação (como conversar) ao item."""
        
        habilidade_id = request.data.get("habilidade_id")
        if not habilidade_id:
            return Response({"error": "Habilidade não informada."},
                            status=status.HTTP_400_BAD_REQUEST)

        item = get_object_or_404(Item, id=item_id)
        progresso, _ = CapturaProgresso.objects.get_or_create(user=request.user, item=item)

        if habilidade_id == 'conversar':
            progresso.chance += 20 
            if progresso.chance > 100:
                progresso.chance = 100
            
            progresso.save()
            
            return Response({
                "success": True,
                "chance": progresso.chance,
                "mensagem": "Bônus de conversa aplicado!"
            }, status=status.HTTP_200_OK)

        else:
            try:
                habilidade = get_object_or_404(Habilidade, id=int(habilidade_id))
            except (ValueError, Habilidade.DoesNotExist):
                return Response({"error": f"Habilidade com ID '{habilidade_id}' não encontrada."}, status=404)
            from habilidades.models import PlayerHabilidade
            player_hab = PlayerHabilidade.objects.filter(user=request.user, habilidade=habilidade).first()
            if not player_hab:
                return Response({"error": f"Você não possui a habilidade '{habilidade.nome}'."}, status=400)
            if not player_hab.pode_usar():
                return Response({"error": f"Sem usos restantes da habilidade '{habilidade.nome}'."}, status=400)

            habilidade.aplicar(progresso)

            player_hab.registrar_uso()

            progresso.save()
            return Response({
                "success": True,
                "chance": progresso.chance,
                "habilidade": {
                    "id": habilidade.id,
                    "nome": habilidade.nome,
                    "quantidade": player_hab.quantidade,
                },
                "mensagem": f"{habilidade.nome} usada com sucesso! Chance atual: {progresso.chance}%"
            }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class ConfirmarCapturaView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, item_id):
        progresso = CapturaProgresso.objects.filter(user=request.user, item_id=item_id).first()
        if not progresso:
            return Response({"error": "Progresso não encontrado."}, status=404)
        
        if progresso.chance < 100:
            return Response({"error": "Chance insuficiente para capturar."}, status=400)

        progresso.capturado = True
        progresso.save()

        mochila_item, created = MochilaItem.objects.get_or_create(
            user=request.user,
            item_id=item_id,
            defaults={'foi_captura_forcada': False} 
        )

        progresso.chance = 0
        progresso.capturado = False
        progresso.save()

        return Response({"mensagem": "Item capturado com sucesso! Chance resetada para 0%."})