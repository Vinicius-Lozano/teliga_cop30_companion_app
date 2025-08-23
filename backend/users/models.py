from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("O usuário deve ter um username")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    telefone = models.CharField(max_length=13, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'         
    REQUIRED_FIELDS = ['telefone']     
