from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .serializers import CustomRegisterSerializer, MyTokenObtainPairSerializer
from .models import Usuario

class RegisterView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserListView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = [permissions.IsAdminUser]

class UserMeView(generics.RetrieveAPIView):
    """
    Retorna os dados do usuário autenticado (o próprio usuário).
    """
    serializer_class = CustomRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
