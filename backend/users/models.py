from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None, email=None, **extra_fields):
        if not username:
            raise ValueError(_("O usuário deve ter um username"))


        if not extra_fields.get("is_superuser") and not email:
            raise ValueError(_("O email é obrigatório para usuários."))

        if email:
            email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(username, password, email, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    class Genero(models.TextChoices):
        MASCULINO = "M", _("Masculino")
        FEMININO = "F", _("Feminino")
        OUTRO = "O", _("Outro")

    username = models.CharField(_("username"), max_length=50, unique=True)
    email = models.EmailField(
        _("endereço de email"), max_length=254, unique=True
    )
    genero = models.CharField(
        _("gênero"), max_length=1, choices=Genero.choices, blank=True
    )
    data_nas = models.DateField(_("data de nascimento"), unique=True, null=True, blank=True)
    telefone = models.CharField(
        _("telefone"), max_length=15, unique=True, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_("data de cadastro"), default=timezone.now)


    objects = UsuarioManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']
