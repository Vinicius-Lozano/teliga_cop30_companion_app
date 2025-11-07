from rest_framework import serializers
from .models import Habilidade, PlayerHabilidade

class HabilidadeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habilidade
        fields = ('id', 'nome', 'icone', 'som', 'animacao')

class PlayerHabilidadeSerializer(serializers.ModelSerializer):
    habilidade = HabilidadeListSerializer()
    class Meta:
        model = PlayerHabilidade
        fields = ('habilidade', 'quantidade')
