from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import password_validation
from .models import Usuario

# Serializer para exibir e atualizar dados do usuário (perfil)
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id', 'username', 'email', 'genero', 'data_nas',
            'telefone', 'date_joined', 'is_staff', 'is_superuser'
        )
        read_only_fields = ('username', 'email', 'date_joined', 'is_staff', 'is_superuser')

# Serializer de registro
class CustomRegisterSerializer(RegisterSerializer):
    genero = serializers.ChoiceField(choices=Usuario.Genero.choices, required=False, allow_blank=True)
    data_nas = serializers.DateField(required=False, allow_null=True)
    telefone = serializers.CharField(max_length=15, required=False, allow_null=True, allow_blank=True)

    def custom_signup(self, request, user):
        user.genero = self.validated_data.get('genero', '')
        user.data_nas = self.validated_data.get('data_nas', None)
        user.telefone = self.validated_data.get('telefone', '')
        user.save()
        
    def validate_email(self, email):
        if Usuario.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return email

# JWT personalizado
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token

# serializer pra troca de senha
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Senha atual incorreta.")
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value



