from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.urls import reverse

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import redirect, render,get_object_or_404
from WebPam import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from datetime import datetime
from sitewebpam.models import Info_utilisateurs, Sitewebpam
from blog.models import *
from portofolio.models import *
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.

def create_site_portofolio(request, site_id):
    if request.method == "POST":
        title = request.POST.get('title')
        couleur = request.POST.get('couleur')
        logo = request.FILES.get('logo')

        # Récupérer l'instance de Sitewebpam correspondante
        sitewebpam = Sitewebpam.objects.get(id=site_id)
        
        # Créer une instance de Site_Portofolio avec les données du formulaire
        site_portofolio = Site_Portofolio.objects.create(
            title=title,
            id_sitepam=sitewebpam,
            couleur=couleur,
            logo=logo,
            site_id=site_id  # Assurez-vous d'inclure la valeur de site_id ici
        )

        # Rediriger vers le tableau de bord du portefeuille
        return redirect('dashboardportofolio', domaine=sitewebpam.domaine)

    return render(request, 'create_site_portofolio.html', {'site_id': site_id})



# Dashboard portofolio


    





def dashboardportofolio(request, domaine):
    portofolios = Site_Portofolio.objects.filter(id_sitepam__domaine=domaine)
    if portofolios.exists():
        portofolio = portofolios.first()
        sitewebpam = portofolio.id_sitepam
        site_id = sitewebpam.id  # Récupérer l'ID du site
        return render(request, 'dashboardportoo.html', {'domaine': domaine, 'portofolio': portofolio, 'sitewebpam': sitewebpam, 'site_id': site_id})
    else:
        return render(request, 'erreur.html', {'message': 'Aucun portefeuille trouvé pour ce domaine.'})


    
    
    
def view_site_portofolio(request, domaine):
    # Récupérer le site portofolio à partir du domaine donné
    site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam__domaine=domaine)

    # Récupérer les informations nécessaires sur le site portofolio
    title = site_portofolio.title
    couleur = site_portofolio.couleur
    logo = site_portofolio.logo

    # Récupérer les informations additionnelles du site portofolio
    infos = Infos_Portofolio.objects.filter(site=site_portofolio)
    about = About_Portofolio.objects.filter(site=site_portofolio).first()  
    services = Services_Portofolio.objects.filter(site=site_portofolio)
    heroes = Heroes_Portofolio.objects.filter(site=site_portofolio)

    # Récupérer les projets portofolio associés à ce site
    pro = Pro_Portofolio.objects.filter(site=site_portofolio)

    # Passer les données au template
    return render(request, 'view_site_portofolio.html', {
        'title': title,
        'logo': logo,
        'couleur': couleur,
        'sitewebpam': site_portofolio.id_sitepam,  # Passer l'instance de Sitewebpam associée
        'infos': infos,
        'about': about,
        'services': services,
        'heroes' : heroes,
        'pro': pro,
    })
    
    
    # Ajouter service portofolio
    

from django.shortcuts import get_object_or_404
from .models import Site_Portofolio
from sitewebpam.models import Sitewebpam
from django.shortcuts import render, redirect, get_object_or_404
from .models import Site_Portofolio, Services_Portofolio
from sitewebpam.models import Sitewebpam
from utilisateurs.models import User_Main  # Assurez-vous d'importer correctement le modèle d'utilisateur

from django.shortcuts import render, redirect

def add_service(request, site_id):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        image = request.FILES.get('image')
        descriptions = request.POST.get('descriptions')
        autres = request.POST.get('autres')

        # Obtenez l'instance de Sitewebpam correspondant à partir de site_id
        sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

        # Obtenez l'instance de SitePortofolio associée au Sitewebpam
        site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)

        # Créez le service en l'associant au SitePortofolio correspondant
        service = Services_Portofolio.objects.create(
            site=site_portofolio,
            titre=titre,
            image=image,
            descriptions=descriptions,
            autres=autres
        )
        service.save()
        # Rediriger vers la page de détail du site_portofolio
        return redirect('add_service', site_id=site_portofolio.pk)
    else:
        # Obtenez tous les services associés au site_portofolio actuel
        services = Services_Portofolio.objects.filter(site__id_sitepam=site_id)

        # Renvoyer le formulaire d'ajout de service et la liste des services existants
        return render(request, 'add_service.html', {'site_id': site_id, 'services': services})
    
    
    
    
    
def modif_service(request, service_id):
    # Récupérer le service à modifier
    service = get_object_or_404(Services_Portofolio, pk=service_id)

    if request.method == 'POST':
        # Traiter le formulaire de modification du service
        # Ici, vous pouvez récupérer les données du formulaire et les mettre à jour dans la base de données
        # Par exemple :
        service.titre = request.POST.get('titre')
        service.descriptions = request.POST.get('descriptions')
        service.image = request.FILES.get('image')
        service.save()

        # Rediriger vers une page de confirmation ou vers une autre vue
        return redirect('add_service')

    # Si la méthode HTTP est GET, afficher le formulaire de modification du service
    return render(request, 'modifservice.html', {'service': service})



from django.shortcuts import render, redirect, get_object_or_404
from .models import Infos_Portofolio, About_Portofolio, Pro_Portofolio, Heroes_Portofolio



# Def pou Infos #########################################################3
def add_info(request, site_id):
    info_exists = Infos_Portofolio.objects.filter(site__id_sitepam=site_id).exists()

    if request.method == 'POST':
        if not info_exists:
            # Récupérer les données du formulaire
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            adresse = request.POST.get('adresse')
            location = request.POST.get('location')

            sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

            # Obtenez l'instance de SitePortofolio associée au Sitewebpam
            site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)

            # Créer une nouvelle instance d'Infos_Portofolio en utilisant l'instance site_portofolio
            infos = Infos_Portofolio.objects.create(
                site=site_portofolio,  # Utilisez l'instance site_portofolio ici
                nom=nom,
                prenom=prenom,
                phone=phone,
                email=email,
                adresse=adresse,
                location=location
            )
            # Rediriger vers une autre vue ou une page de confirmation
            return redirect('add_info', site_id=site_id)
        else:
            # Afficher un message d'erreur
            messages.error(request, "Un objet Info_Portofolio existe déjà pour ce Site_Portofolio.")
            # Rediriger vers la même vue
            return redirect('add_info', site_id=site_id)
    else:
        # Obtenez tous les services associés au site_portofolio actuel
        infos = Infos_Portofolio.objects.filter(site__id_sitepam=site_id)

        # Renvoyer le formulaire d'ajout de service et la liste des services existants
        return render(request, 'add_info.html', {'site_id': site_id, 'infos': infos})





# def pour l'About  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4

def add_about(request, site_id):
    # Vérifier s'il existe déjà un objet About_Portofolio associé à ce Site_Portofolio
    about_exists = About_Portofolio.objects.filter(site__id_sitepam=site_id).exists()
    
    if request.method == 'POST':
        if not about_exists:  # Vérifier s'il n'existe pas déjà d'objet About_Portofolio
            # Récupérer les données du formulaire
            texte = request.POST.get('texte')
            autre = request.POST.get('autre')
            image = request.FILES.get('image')

            # Obtenez l'instance de Sitewebpam correspondant à partir de site_id
            sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

            # Obtenez l'instance de SitePortofolio associée au Sitewebpam
            site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)

            # Créer une nouvelle instance d'About_Portofolio en utilisant l'instance site_portofolio
            about = About_Portofolio.objects.create(
                site=site_portofolio,  # Utilisez site_portofolio au lieu de site_id
                texte=texte,
                autre=autre,
                image=image
            )
            about.save()
            # Rediriger vers une autre vue ou une page de confirmation
            return redirect('add_about', site_id=site_id)
        else:
                        # Afficher un message d'erreur
            messages.error(request, "Un objet About_Portofolio existe déjà pour ce Site_Portofolio.")
            # Rediriger vers la même vue
            return redirect('add_about', site_id=site_id)

    else:
                # Obtenez tous les services associés au site_portofolio actuel
        abouts = About_Portofolio.objects.filter(site__id_sitepam=site_id)

        # Renvoyer le formulaire d'ajout de service et la liste des services existants
        return render(request, 'add_about.html', {'site_id': site_id, 'abouts': abouts})




    




# Ajoute projet ##################################################################################################
def add_pro(request, site_id):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        titre = request.POST.get('titre')
        descriptions = request.POST.get('descriptions')
        image = request.FILES.get('image')
        created_at = request.POST.get('created_at')
        links = request.POST.get('links')
        categorie = request.POST.get('categorie')
        
        # Obtenez l'instance de Sitewebpam correspondant à partir de site_id
        sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

        # Obtenez l'instance de SitePortofolio associée au Sitewebpam
        site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)
        
        # Créer une nouvelle instance de Pro_Portofolio en utilisant l'instance site_portofolio
        pro = Pro_Portofolio.objects.create(
            site=site_portofolio,  # Utilisez site_portofolio au lieu de site_id
            titre=titre,
            descriptions=descriptions,
            image=image,
            created_at=created_at,
            links=links,
            categorie=categorie
        )
        # Rediriger vers une autre vue ou une page de confirmation
        return redirect('add_pro', site_id=site_id)
    else:
                # Obtenez tous les services associés au site_portofolio actuel
        pros = Pro_Portofolio.objects.filter(site__id_sitepam=site_id)

        # Renvoyer le formulaire d'ajout de service et la liste des services existants
        return render(request, 'add_pro.html', {'site_id': site_id, 'pros': pros})

    
    
    
    
    
# pou heroooooooo
def add_hero(request, site_id):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        titre1 = request.POST.get('titre1')
        titre2 = request.POST.get('titre2')
        paragraphe = request.POST.get('paragraphe')
        cv = request.POST.get('cv')
        image = request.FILES.get('image')
        
        # Obtenez l'instance de Sitewebpam correspondant à partir de site_id
        sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

        # Obtenez l'instance de SitePortofolio associée au Sitewebpam
        site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)

        # Créer une nouvelle instance de Heroes_Portofolio en utilisant l'instance site_portofolio
        hero = Heroes_Portofolio.objects.create(
            site=site_portofolio,  # Utilisez l'instance site_portofolio ici
            titre1=titre1,
            titre2=titre2,
            paragraphe=paragraphe,
            cv=cv,
            image=image
        )
        # Rediriger vers une autre vue ou une page de confirmation
        return redirect('add_hero', site_id=site_id)
    else:
        # Afficher le formulaire d'ajout d'infos
        return render(request, 'add_hero.html', {'site_id': site_id})




