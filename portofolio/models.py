from django.db import models
from utilisateurs.models import User_Main,CustomUserManager
from sitewebpam.models import*

# Create your models here.

# Create your models here.

class Site_Portofolio(models.Model):
    title = models.CharField(max_length=200)
    id_sitepam = models.ForeignKey(Sitewebpam, on_delete=models.CASCADE)
    couleur = models.CharField(max_length=50)
    logo = models.CharField(max_length=50)
    site = models.ForeignKey(Sitewebpam, on_delete=models.CASCADE, related_name='portofolios')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    
class User_Standard(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50) 
    nom_utilisateur = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255)
    mot_de_passe = models.CharField(max_length=255)
    id_sitepam = models.ForeignKey(Sitewebpam, on_delete=models.CASCADE)
    id_sitepam = models.ForeignKey(Sitewebpam, on_delete=models.CASCADE, related_name='blog_users')
    site = models.ForeignKey(Site_Portofolio, on_delete=models.CASCADE, related_name='blog_users')
    
class Infos_Portofolio(models.Model):
    site=models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE )
    nom = models.TextField(max_length=50)
    prenom = models.TextField(max_length=50)
    phone = models.TextField(max_length=50)
    email = models.CharField(max_length=100)
    adresse = models.TextField(max_length=50)
    location = models.TextField(max_length=50)
    
class About_Portofolio(models.Model):
    site=models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE )
    texte = models.CharField(max_length=255)
    autre = models.TextField(null=True,max_length=255)
    image = models.ImageField(upload_to='static/images/', null=True)
    
# class Category_Portofolio(models.Model):
#     site=models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE )
#     name = models.CharField(max_length=100)
#     description = models.TextField()

# class Project_Portofolio(models.Model):
#     site=models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE )
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     # categories = models.ManyToManyField(Category_Portofolio)
#     created_at = models.DateTimeField(auto_now_add=True)
#     links = models.TextField()

class Pro_Portofolio(models.Model):
    site = models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE)
    titre = models.CharField( max_length=50 )
    image = models.ImageField(upload_to='static/images/', null=True)
    descriptions = models.CharField(null=True, max_length=255 )
    created_at = models.DateTimeField(auto_now_add=True)
    links = models.CharField(null=True, max_length=255 )
    categorie = models.CharField(null=True, max_length=100 )


class Like_Portofolio(models.Model):
    site=models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE )
    post = models.ForeignKey(Pro_Portofolio, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User_Standard, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Follower_Portofolio(models.Model):
    site = models.ForeignKey(Site_Portofolio, on_delete=models.CASCADE)
    User_Standard = models.ForeignKey(User_Standard,null=True, on_delete=models.CASCADE)
    user_livreur = models.ForeignKey(User_Livreur, null=True, on_delete=models.CASCADE)
    user_main = models.ForeignKey(User_Main, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Note_Portofolio(models.Model):
    site = models.ForeignKey(Site_Portofolio, on_delete=models.CASCADE)
    User_Standard = models.ForeignKey(User_Standard,null=True, on_delete=models.CASCADE)
    user_livreur = models.ForeignKey(User_Livreur, null=True, on_delete=models.CASCADE)
    valeur = models.CharField( max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Partage_Portofolio(models.Model):
    site=models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE )
    data_post = models.ForeignKey(Pro_Portofolio,null=True, on_delete=models.CASCADE)
    data_site = models.ForeignKey(Sitewebpam,null=True, on_delete=models.CASCADE)
    user_Standard = models.ForeignKey(User_Standard,null=True, on_delete=models.CASCADE)
    user_livreur = models.ForeignKey(User_Livreur, null=True, on_delete=models.CASCADE)
    user_main = models.ForeignKey(User_Main, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Message_Portofolio(models.Model):
    site = models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE)
    object =  models.CharField( max_length=50 , null=True)
    content =  models.CharField( max_length=255 )
    user_Standard = models.ForeignKey(User_Standard,null=True, on_delete=models.CASCADE)
    user_main = models.ForeignKey(User_Main, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    statut = models.CharField( max_length=50)
    
    
class Services_Portofolio(models.Model):
    site = models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE)
    titre = models.CharField( max_length=50 )
    image = models.ImageField(upload_to='static/images/', null=True)
    descriptions = models.CharField(null=True, max_length=255 )
    autres = models.CharField(null=True, max_length=255 )

    
class Heroes_Portofolio(models.Model):
    site = models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE)
    titre1 = models.CharField( max_length=50 )
    titre2 = models.CharField(null=True, max_length=50 )
    paragraphe = models.CharField(null=True, max_length=255 )
    cv = models.CharField(null=True, max_length=255 )
    image = models.ImageField(upload_to='static/images/', null=True)
   