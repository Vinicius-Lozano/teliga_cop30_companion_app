from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Usuario

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        fields = '__all__'
        
    def create(self, validated_data):
        user = Usuario(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token