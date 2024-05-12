from django.db import models
from utilisateurs.models import *

# Create your models here.

class Plan(models.Model):
    name = models.CharField(max_length= 50)
    description = models.TextField(max_length= 255, blank= True, null=True)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Abonement(models.Model):
    id_user = models.ForeignKey(User_Main, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    type_abonnement = models.CharField(max_length=100)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    
class Sitewebpam(models.Model):
    id_user = models.ForeignKey(User_Main, on_delete=models.CASCADE)
    id_abonnement= models.ForeignKey(Abonement, on_delete=models.CASCADE, null=True)
    domaine = models.CharField(max_length = 100)
    nom_site = models.CharField(max_length = 150, null=True)
    type = models.CharField(max_length = 50)
    stockage = models.CharField(max_length = 150, null=True)
 
class Info_utilisateurs(models.Model):
    id_user = models.ForeignKey(User_Main, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    terms_conditions = models.BooleanField(default=False)
    image = models.ImageField(upload_to='static/images/', blank=True)
    initials = models.CharField(max_length=2, blank=True, null=True)  # Rendre le champ facultatif
