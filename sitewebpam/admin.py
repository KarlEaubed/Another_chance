from django.contrib import admin
from .models import Plan, Abonement, Sitewebpam, Info_utilisateurs

# Register your models here.

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')

@admin.register(Abonement)
class AbonementAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'type_abonnement', 'date_debut', 'date_fin')

@admin.register(Sitewebpam)
class SitewebpamAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_abonnement', 'domaine', 'nom_site', 'type', 'stockage')

@admin.register(Info_utilisateurs)
class InfoUtilisateursAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'adresse', 'ville', 'state', 'zip_code', 'country', 'terms_conditions', 'image', 'initials')
