from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from .models import Usuario

class RegisterView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserListView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]