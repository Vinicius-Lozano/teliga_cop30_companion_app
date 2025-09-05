from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Usuario

# Serializer for displaying and updating user data (e.g., on a profile page)
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # List only the fields that are safe to expose in an API
        fields = (
            'id', 'username', 'email', 'genero', 'data_nas',
            'telefone', 'date_joined', 'is_staff', 'is_superuser'
        )
        read_only_fields = ('username', 'email', 'date_joined', 'is_staff', 'is_superuser')

# Custom serializer for user registration, required by your settings.py
class CustomRegisterSerializer(RegisterSerializer):
    genero = serializers.ChoiceField(choices=Usuario.Genero.choices, required=False, allow_blank=True)
    data_nas = serializers.DateField(required=False, allow_null=True)
    telefone = serializers.CharField(max_length=15,required=False, allow_null=True, allow_blank=True)

    def custom_signup(self, request, user):
        user.genero = self.validated_data.get('genero', '')
        user.data_nas = self.validated_data.get('data_nas', None)
        user.telefone = self.validated_data.get('telefone', '')
        user.save()
        
    def validate_email(self, email):
        if Usuario.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return email

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token

