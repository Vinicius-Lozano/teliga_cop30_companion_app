from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .serializers import (
    CustomRegisterSerializer, MyTokenObtainPairSerializer, 
    UsuarioSerializer, ChangePasswordSerializer
)
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
    serializer_class = CustomRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()  
        return Response({"detail": "Conta excluída com sucesso."}, status=status.HTTP_204_NO_CONTENT)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Usuario
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.object.set_password(serializer.validated_data['new_password'])
        self.object.save()
        return Response({"detail": "Senha alterada com sucesso"}, status=status.HTTP_200_OK)







