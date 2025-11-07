from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.views import APIView
# Import da main (necessário para o novo sistema)
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


# ===========================
#  MOCHILAS (Versão do HEAD, com novas views)
# ===========================

# --- NOVAS VIEWS SEPARADAS ---

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
        # Filtra apenas por itens do tipo 'NEN' (itens comuns)
        return MochilaItem.objects.filter(
            user=self.request.user,
            item__tipo=Item.Tipo.NEN
        ).select_related('item')


# --- VIEWS ANTIGAS (COM AJUSTES) ---

class MochilaItemListCreateView(generics.ListCreateAPIView):
    """ 
    View original - Agora funciona como um 'adicionar genérico' 
    (Não será mais usada para LISTAR, usaremos as views acima)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MochilaItemSerializer

    def get_queryset(self):
        return MochilaItem.objects.filter(user=self.request.user).select_related('item')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.validated_data['item']
        
        # O 'foi_captura_forcada' é setado pelo ConfirmarCapturaView
        # (Mantendo a variável 'captura' do HEAD)
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
    """ Lista e cria Poções (Versão do HEAD, que está correta) """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MochilaPocaoSerializer # Serializer correto

    def get_queryset(self):
        # Filtra para trazer apenas poções
        return MochilaPocao.objects.filter(
            user=self.request.user, 
            item__tipo=Item.Tipo.POC
        ).select_related('item')

    def create(self, request, *args, **kwargs):
        pocao_id = request.data.get('pocao_id') or request.data.get('item_id')
        if not pocao_id:
            return Response({"detail": "Campo 'pocao_id' ou 'item_id' é obrigatório."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Garante que o item é uma poção
        item = get_object_or_404(Item, pk=pocao_id, tipo=Item.Tipo.POC)

        # Adiciona na mochila de poções
        mochila_pocao, created = MochilaPocao.objects.get_or_create(user=request.user, item=item)

        # Opcional: Adiciona na mochila principal também se sua lógica depender disso
        # MochilaItem.objects.get_or_create(user=request.user, item=item)

        out = self.get_serializer(mochila_pocao)
        return Response(out.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# ===========================
#  QUESTÕES
# ===========================

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


# ===========================
#  🧪 CAPTURA MODULAR (Versão da MAIN)
# ===========================

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
        """Aplica uma habilidade do jogador ao item durante a captura."""
        habilidade_id = request.data.get("habilidade_id")
        if not habilidade_id:
            return Response({"error": "Habilidade não informada."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Esta é a nova lógica da MAIN, que vamos adotar
        item = get_object_or_404(Item, id=item_id)
        habilidade = get_object_or_404(Habilidade, id=habilidade_id)
        progresso, _ = CapturaProgresso.objects.get_or_create(user=request.user, item=item)

        # Valida se o jogador possui essa habilidade e se ainda pode usá-la
        from habilidades.models import PlayerHabilidade
        player_hab = PlayerHabilidade.objects.filter(user=request.user, habilidade=habilidade).first()
        if not player_hab:
            return Response({"error": "Você não possui essa habilidade."}, status=400)
        if not player_hab.pode_usar():
            return Response({"error": "Sem usos restantes dessa habilidade."}, status=400)

        # Aplica o efeito da habilidade
        habilidade.aplicar(progresso)

        # Registra o uso da habilidade
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

        # A lógica do HEAD (foi_ataque_usado) não é mais compatível com o sistema de Habilidades
        # Então, adotamos a lógica da MAIN, que é mais simples
        mochila_item, created = MochilaItem.objects.get_or_create(
            user=request.user,
            item_id=item_id,
            defaults={'foi_captura_forcada': False} # Versão da MAIN
        )

        progresso.chance = 0
        progresso.capturado = False
        # A linha abaixo (do HEAD) foi removida pois progresso.foi_ataque_usado não existe mais
        # progresso.foi_ataque_usado = False 
        progresso.save()

        return Response({"mensagem": "Item capturado com sucesso! Chance resetada para 0%."})