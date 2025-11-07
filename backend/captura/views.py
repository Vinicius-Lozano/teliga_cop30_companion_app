from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from .models import (
    MochilaItem, MochilaEvento, MochilaPocao,
    ConversaQuestoes, CapturaProgresso
)
from .serializers import (
    MochilaItemSerializer, MochilaEventoSerializer, MochilaPocaoSerializer,
    ConversaQuestoesSerializer, RespostaSerializer, CapturaProgressoSerializer
)
from item.models import Item


# ===========================
# 🧳 MOCHILA
# ===========================

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


class MochilaPocaoListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MochilaPocaoSerializer

    def get_queryset(self):
        return MochilaPocao.objects.filter(user=self.request.user).select_related('item')

    def create(self, request, *args, **kwargs):
        pocao_id = request.data.get('pocao_id') or request.data.get('item_id')
        if not pocao_id:
            return Response({"detail": "Campo 'pocao_id' ou 'item_id' é obrigatório."},
                            status=status.HTTP_400_BAD_REQUEST)

        item = get_object_or_404(Item, pk=pocao_id)

        # Cria também na mochila principal (para aparecer na UI)
        mochila_item, created = MochilaItem.objects.get_or_create(user=request.user, item=item)

        # Mantém registro separado (opcional, para rastrear poções)
        MochilaPocao.objects.get_or_create(user=request.user, item=item)

        out = MochilaItemSerializer(mochila_item)
        return Response(out.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# ===========================
# ❓ QUESTÕES
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
# 🧪 CAPTURA
# ===========================

@method_decorator(csrf_exempt, name='dispatch')
class CapturaView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, item_id):
        progresso, _ = CapturaProgresso.objects.get_or_create(user=request.user, item_id=item_id)
        serializer = CapturaProgressoSerializer(progresso)
        return Response(serializer.data)

    def post(self, request, item_id):
        acao = request.data.get('acao')
        valores = {'atacar': 20, 'conversar': 10, 'investigar': 15}
        if acao not in valores:
            return Response({"error": "Ação inválida."}, status=status.HTTP_400_BAD_REQUEST)

        progresso, _ = CapturaProgresso.objects.get_or_create(user=request.user, item_id=item_id)
        nova_chance = progresso.aumentar_chance(valores[acao])
        return Response({"chance": nova_chance, "acao": acao})


@method_decorator(csrf_exempt, name='dispatch')
class ConfirmarCapturaView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, item_id):
        # Busca o progresso do usuário para esse item
        progresso = CapturaProgresso.objects.filter(user=request.user, item_id=item_id).first()
        if not progresso:
            return Response({"error": "Progresso não encontrado."}, status=404)
        
        # Verifica se a chance de captura atingiu 100%
        if progresso.chance < 100:
            return Response({"error": "Chance insuficiente para capturar."}, status=400)

        # Marca como capturado
        progresso.capturado = True
        progresso.save()

        # Adiciona à mochila principal garantindo o valor do campo obrigatório
        mochila_item, created = MochilaItem.objects.get_or_create(
            user=request.user,
            item_id=item_id,
            defaults={'foi_captura_forcada': False}  # ⚡ valor padrão para não quebrar o NOT NULL
        )

        # Reseta o progresso para nova captura
        progresso.chance = 0
        progresso.capturado = False
        progresso.save()

        return Response({
            "mensagem": "Item capturado com sucesso! Chance resetada para 0%."
        })