# Model utilisateurs
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self._create_user(email, password, **extra_fields)

class User_Main(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    portable = models.CharField(max_length=20)
    date_de_nais = models.DateField(blank=False, null=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Ajout du champ is_staff
    is_superuser = models.BooleanField(default=False)  # Ajout du champ is_superuser

    date_joined = models.DateTimeField(default=timezone.now)
    
    


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'username', 'portable', 'date_de_nais']

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"





#############################################################################################



class User_Livreur(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    nom_utilisateur = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255)
    mot_de_passe = models.CharField(max_length=255)
    portable = models.CharField(max_length=20)
    location = models.CharField(max_length=55)
    date_de_nais = models.DateField()
    date_creation = models.DateField()
    statu = models.BooleanField(default = False)

    def __str__(self):
        return str(self.nom_utilisateur)