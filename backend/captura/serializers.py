from rest_framework import serializers
from .models import MochilaItem, MochilaEvento, ConversaQuestoes, CapturaProgresso
from item.serializers import ItemSerializer
from events.serializers import EventoSerializer
from item.models import Item
from events.models import Evento

class MochilaItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(write_only=True, source='item', queryset=Item.objects.all())

    class Meta:
        model = MochilaItem
        fields = ['id', 'item', 'item_id', 'captured_at']

class MochilaEventoSerializer(serializers.ModelSerializer):
    evento = EventoSerializer(read_only=True)
    evento_id = serializers.PrimaryKeyRelatedField(write_only=True, source='evento', queryset=Evento.objects.all())

    class Meta:
        model = MochilaEvento
        fields = ['id', 'evento', 'evento_id', 'captured_at']

class ConversaQuestoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversaQuestoes
        fields = ['id', 'item', 'pergunta', 'escolha_a', 'escolha_b', 'escolha_c']

class RespostaSerializer(serializers.Serializer):
    resposta = serializers.CharField(max_length=1)

class CapturaProgressoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapturaProgresso
        fields = ['id', 'user', 'item', 'chance', 'capturado']
        read_only_fields = ['user', 'chance', 'capturado']
