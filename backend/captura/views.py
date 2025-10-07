from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import MochilaItem, MochilaEvento, ConversaQuestoes, CapturaProgresso
from .serializers import (
    MochilaItemSerializer, MochilaEventoSerializer,
    ConversaQuestoesSerializer, RespostaSerializer, CapturaProgressoSerializer
)


# MOCHILA


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



# QUESTÕES


class QuestaoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses=ConversaQuestoesSerializer,
        description="Retorna a questão pelo ID"
    )
    def get(self, request, pk):
        try:
            questao = ConversaQuestoes.objects.get(pk=pk)
        except ConversaQuestoes.DoesNotExist:
            return Response({"error": "Questão não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ConversaQuestoesSerializer(questao)
        return Response(serializer.data)

    @extend_schema(
        request=RespostaSerializer,
        responses={200: ConversaQuestoesSerializer},
        description="Envie a resposta e receba o resultado"
    )
    def post(self, request, pk):
        try:
            questao = ConversaQuestoes.objects.get(pk=pk)
        except ConversaQuestoes.DoesNotExist:
            return Response({"error": "Questão não encontrada."}, status=status.HTTP_404_NOT_FOUND)

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


class QuestaoAleatoriaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total = ConversaQuestoes.objects.count()
        if total == 0:
            return Response({"error": "Nenhuma questão cadastrada."}, status=404)

        questao = ConversaQuestoes.objects.order_by("?").first()
        serializer = ConversaQuestoesSerializer(questao)
        return Response(serializer.data)

class QuestaoPorItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, item_id):
        questao = ConversaQuestoes.objects.filter(item_id=item_id).order_by("?").first()
        if not questao:
            return Response({"error": "Nenhuma questão disponível para este item."}, status=404)
        serializer = ConversaQuestoesSerializer(questao)
        return Response(serializer.data)




# CAPTURA


class CapturaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, item_id):
        """Ver progresso de captura"""
        progresso, _ = CapturaProgresso.objects.get_or_create(
            user=request.user,
            item_id=item_id
        )
        serializer = CapturaProgressoSerializer(progresso)
        return Response(serializer.data)

    def post(self, request, item_id):
        """Executar uma ação (conversar, atacar, etc.)"""
        acao = request.data.get('acao')
        valores = {
            'atacar': 20,
            'conversar': 10,
            'investigar': 15
        }
        if acao not in valores:
            return Response({"error": "Ação inválida."}, status=status.HTTP_400_BAD_REQUEST)

        progresso, _ = CapturaProgresso.objects.get_or_create(
            user=request.user,
            item_id=item_id
        )
        nova_chance = progresso.aumentar_chance(valores[acao])
        return Response({"chance": nova_chance, "acao": acao})


class ConfirmarCapturaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, item_id):
        progresso = CapturaProgresso.objects.filter(
            user=request.user, item_id=item_id
        ).first()
        if not progresso:
            return Response({"error": "Progresso não encontrado."}, status=404)
        if progresso.chance < 100:
            return Response({"error": "Chance insuficiente para capturar."}, status=400)

        # Marca como capturado
        progresso.capturado = True
        progresso.save()

        # Adiciona à mochila
        from .models import MochilaItem
        MochilaItem.objects.get_or_create(user=request.user, item_id=item_id)

        # Resetar a chance para poder capturar de novo
        progresso.chance = 0
        progresso.capturado = False
        progresso.save()

        return Response({"mensagem": "Item capturado com sucesso! Chance resetada para 0%."})
