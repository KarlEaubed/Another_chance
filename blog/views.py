from django.shortcuts import get_object_or_404, render, redirect

from WebPam import settings
from .models import Post_Blog
from sitewebpam.models import Sitewebpam
from blog.models import *
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

# Vue de l'application "blog"

def dashboard_blog(request, domaine):
    # Récupérer l'utilisateur connecté
    user = request.user

    # Récupérer les informations du site lié à l'utilisateur connecté
    site = Sitewebpam.objects.filter(id_user=user).first()

    # Vérifier si un site a été trouvé pour l'utilisateur
    if site:
        # Récupérer les informations spécifiques au site à afficher
        site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
        if site_blog_info:
            post_count = Post_Blog.objects.filter(author=site_blog_info.id_Admin_Blog).count()
            comment_count = Comment_Blog.objects.filter(post__author=site_blog_info.id_Admin_Blog).count()
            like_count = Like_Blog.objects.filter(post__author=site_blog_info.id_Admin_Blog).count()
            user_info = User_Main.objects.get(username=user.username)
            user_add = Info_utilisateurs.objects.get(id_user=user)

            # Ajouter site_id au contexte
            site_id = site_blog_info.id  # Assurez-vous d'ajuster cela selon votre modèle
            context = {
                'post_count': post_count,
                'comment_count': comment_count,
                'like_count': like_count,
                'site_title': site_blog_info.title,
                'domaine': site.domaine,
                'site_id': site_id,
                'user_info' : user_info,
                'user_add' : user_add,
            }
            return render(request, 'dashboard_blog.html', context)
        else:
            # Gérer le cas où aucune information sur le site n'est trouvée
            return HttpResponse("No site information found.")
    else:
        # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
        return HttpResponse("No site found for the user.")


#######################################################################################################

########################################################################################################
# fonction pou ale sou menu an
def menu(request, domaine):
    # Récupérer l'utilisateur connecté
    user = request.user

    # Récupérer les informations du site lié à l'utilisateur connecté
    site = Sitewebpam.objects.filter(id_user=user).first()

    # Vérifier si un site a été trouvé pour l'utilisateur
    if site:
        # Récupérer les informations spécifiques au site à afficher
        site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
        # Récupérez les informations de l'utilisateur à partir du modèle User_Main
        user_info = User_Main.objects.get(username=user.username)  # Changer pour correspondre à la façon dont vous identifiez un utilisateur
        site_id = site_blog_info.id

        # Récupérer les catégories et les tags
        categories = Category_Blog.objects.all()
        tags = Tag_Blog.objects.all()

        # Récupérer les articles de blog associés au site blog, triés par date de création
        posts = Post_Blog.objects.filter(site=site_blog_info).order_by('-created_at')


        # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
        context = {
            'user_info': user_info,
            'site_id': site_id,
            'site_title': site_blog_info.title,
            'categories': categories,  # Ajoutez les catégories au contexte
            'tags': tags,  # Ajoutez les tags au contexte
            'posts': posts,
            'domaine': site.domaine,
        }
        # Logique de vue pour afficher les messages
        return render(request, 'menu.html', context)
    else:
        # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
        return HttpResponse("No site found for the user.")



#######################################################################################################

# #######################################################################################################
# fonction pou ale sou theme la
def marketplace(request):
    # Obtenez l'utilisateur connecté
    user = request.user  # Assurez-vous que l'utilisateur est connecté

    # Récupérer les informations du site lié à l'utilisateur connecté
    site = Sitewebpam.objects.filter(id_user=user).first()

    # Vérifier si un site a été trouvé pour l'utilisateur
    if site:

        # Récupérez les informations de l'utilisateur à partir du modèle User_Main
        user_info = User_Main.objects.get(username=user.username)
        user_add = Info_utilisateurs.objects.get(id=user.id)
        site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()

        # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
        context = {
            'user_info': user_info,
            'user_add' : user_add,
            'site_title': site_blog_info.title,
        }
        return render(request, 'marketplace.html', context)
    else:
        # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
        return HttpResponse("No site found for the user.")


#######################################################################################################

# #######################################################################################################
# fonction pou ale sou manage la

def manage(request):
    # Récupérer l'utilisateur connecté
    user = request.user

    # Récupérer les informations du site lié à l'utilisateur connecté
    site = Sitewebpam.objects.filter(id_user=user).first()

    # Récupérer les informations spécifiques au site à afficher
    site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
    post_count = Post_Blog.objects.filter(author=site_blog_info.id_Admin_Blog).count()
    comment_count = Comment_Blog.objects.filter(post__author=site_blog_info.id_Admin_Blog).count()
    like_count = Like_Blog.objects.filter(post__author=site_blog_info.id_Admin_Blog).count()
    abonement = Abonement.objects.filter(id_user=user).first()
    user_info = User_Main.objects.get(username=user.username)

    context = {
        'site': site,
        'site_blog_info': site_blog_info,
        'post_count': post_count,
        'comment_count': comment_count,
        'like_count': like_count,
        'abonement': abonement,
        'user_info' : user_info,
    }
    return render(request, 'manage.html', context)


# #############################################################################################################################
# fonctiom pou mete domaine nan url
#############################################################################################################################

def view_site(request, domaine):

    categories = Category_Blog.objects.all()

    # Récupérer le site blog correspondant au domaine
    site_blog = get_object_or_404(Site_Blog, id_sitepam__domaine=domaine)

    # Récupérer les articles de blog associés au site blog, triés par date de création
    posts = Post_Blog.objects.filter(site=site_blog).order_by('-created_at')

    # Récupérer les titres des posts
    post_titles = [post.title for post in posts]

    # Récupérer les publications mises en avant
    featured_posts = Post_Blog.objects.filter(is_featured=True)
    featured_posts_titles = [featured_post.title for featured_post in featured_posts]

    # Récupérer les 5 derniers posts du site
    latest_posts = Post_Blog.objects.filter(site=site_blog).order_by('-created_at')[:5]

    # Pagination
    paginator = Paginator(posts, 4)  # 4 articles par page
    page_number = request.GET.get('page')
    try:
        paginated_posts = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)  # Afficher la première page si le paramètre de la page n'est pas un entier
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)  # Afficher la dernière page si la page demandée est vide

    # Récupérer la couleur du site à partir de la base de données
    site_color_name = site_blog.Couleur
    color_map = {
        'rouge': '#FF0000',
        'vert': '#00FF00',
        'bleu': '#0000FF',
        'rose': '#FFC0CB',
        'orange': '#FFA500'
    }

    site_color_hex = color_map.get(site_color_name.lower(), '#000000')


    context = {
        'site': site_blog.id_sitepam,
        'featured_posts' : featured_posts,
        'site_color': site_color_hex,
        'categories': categories,
        'site_blog': site_blog,
        'domaine': domaine,
        'posts': paginated_posts,
        'latest_posts': latest_posts,
        'site_id': site_blog.id,
        'post_titles': post_titles,
        'featured_posts_titles': featured_posts_titles,
    }

    # Rendre le modèle HTML avec le contexte
    return render(request, 'site_view.html', context)




# #############################################################################################################################
# fonctiom pou kreye yon post
#############################################################################################################################
def create_post(request, site_id):
    try:
        # Récupérer l'utilisateur connecté
        user = request.user
        # Récupérer les informations du site lié à l'utilisateur connecté
        site = Sitewebpam.objects.filter(id_user=user).first()

        if request.method == 'POST':
            title = request.POST['title']
            image = request.FILES['image']
            content = request.POST['content']
            selected_categories = request.POST.getlist('categories')
            tags = request.POST.getlist('tags')

            # Vérifie si la case à cocher est cochée dans la requête POST
            is_featured = 0
            if 'featured' in request.POST:
                is_featured = 1

            # Récupérer l'admin connecté
            admin_blog = Admin_Blog.objects.get(email=request.user.email)

            # Créer le post avec l'admin connecté comme auteur
            post = Post_Blog.objects.create(
                title=title,
                image=image,
                content=content,
                author=admin_blog,
                is_featured=is_featured,
                site_id=site_id
            )

            # Associer les catégories sélectionnées au post
            for category_id in selected_categories:
                category = Category_Blog.objects.get(pk=category_id)
                post.categories.add(category)

            # Récupérer les catégories et les tags depuis la base de données
            categories = Category_Blog.objects.all()
            tags = Tag_Blog.objects.all()

            # Ajouter les catégories et les tags au contexte
            context = {
                'categories': categories,
                'tags': tags,
            }

            # Rediriger après la création
            return redirect('dashboard_blog', {'domaine': site.domaine})

        else:
            # Si la méthode de requête n'est pas POST, renvoyer simplement le formulaire avec les catégories et les tags
            categories = Category_Blog.objects.all()
            tags = Tag_Blog.objects.all()
            return render(request, 'menu.html', {'categories': categories, 'tags': tags})

    except Exception as e:
        error_message = str(e)
        return redirect(reverse('dashboard_blog') + f'?message={error_message}')


############################################################################################################################
# fonction pou kreye categories
###############################################################################################################################
def create_category(request, site_id):
    # Récupérer l'utilisateur connecté
    user = request.user
    # Récupérer les informations du site lié à l'utilisateur connecté
    sitewebpam = Sitewebpam.objects.filter(id_user=user).first()
    if request.method == "POST":
        # Récupérer les données du formulaire
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Récupérer le site correspondant
        site = Site_Blog.objects.get(id=site_id)

        # Créer la catégorie
        category = Category_Blog.objects.create(name=name, description=description)

        # Ajouter la catégorie au site
        site.categories.add(category)

        # Rediriger vers une autre page ou retourner une réponse
        return redirect('dashboard_blog', {'domaine': sitewebpam.domaine})  # Redirection vers le tableau de bord par example

    return render(request, 'menu.html', {'site_id': site_id})



############################################################################################################################
# fonction pou kreye tags
###############################################################################################################################
def create_tag(request, site_id):
    # Récupérer l'utilisateur connecté
    user = request.user
    # Récupérer les informations du site lié à l'utilisateur connecté
    sitewebpam = Sitewebpam.objects.filter(id_user=user).first()

    if request.method == "POST":
        # Récupérer les données du formulaire
        name = request.POST.get('name')

        # Récupérer le site correspondant
        site = Site_Blog.objects.get(id=site_id)

        # Créer le tag
        tag = Tag_Blog.objects.create(name=name)

        # Ajouter le tag au site
        site.tags.add(tag)

        # Rediriger vers une autre page ou retourner une réponse
        return redirect('dashboard_blog', {'domaine': sitewebpam.domaine})  # Redirection vers le tableau de bord par exemple

    return render(request, 'menu.html', {'site_id': site_id})

############################################################
###########################################################


@csrf_protect
def register_blog(request, domaine, site_id):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        # Récupérer la première lettre du nom et du prénom
        first_letter_firstname = firstname[0].upper() if firstname else ''
        first_letter_lastname = lastname[0].upper() if lastname else ''

        initials = ''

        if firstname:
            initials += first_letter_firstname
        if lastname:
            initials += first_letter_lastname

        # Vérifications des données du formulaire
        if not all([firstname, lastname, username, email, password, confirmpassword]):
            messages.error(request, "Veuillez remplir tous les champs du formulaire.")
            return render(request, 'signup_blog.html')

        if password != confirmpassword:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'signup_blog.html')

        if User_Standard.objects.filter(username=username).exists():
            messages.error(request, "Nom d'utilisateur déjà utilisé.")
            return render(request, 'signup_blog.html')

        if User_Standard.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà associé à un compte.")
            return render(request, 'signup_blog.html')
        


        # Enregistrement de l'utilisateur
        user_standard = User_Standard.objects.create(
            nom=lastname,
            prenom=firstname,
            username=username,
            email=email,
            password=make_password(password),
            initials=initials,
            site_id=site_id,
        )
        user_standard.save()



        return render(request, 'signin_blog.html', {'site_id': site_id, 'domaine': domaine})

    return render(request, 'signup_blog.html', {'site_id': site_id, 'domaine': domaine})


def logout_blog(request):
    logout(request)
    return redirect('logout')




@csrf_protect
def signin_blog(request, domaine, site_id):
    if request.method == "POST":
        username = request.POST.get('username')  # Récupérez l'e-mail depuis le formulaire
        password = request.POST.get('password')

        # Recherchez l'utilisateur dans la table User_Standard par email
        try:
            user_standard = User_Standard.objects.get(username=username)
        except User_Standard.DoesNotExist:
            user_standard = None

        # Vérifiez si l'utilisateur existe et si le mot de passe est correct
        if user_standard is not None and user_standard.check_password(password):
            # Authentifiez l'utilisateur avec le backend d'authentification par défaut
            user_authenticated = authenticate(request, username=user_standard.username, password=password)
            if user_authenticated is not None:
                # Vérifiez si l'utilisateur est associé au site en question
                if user_standard.site_id == int(site_id):
                    # Connectez l'utilisateur
                    login(request, user_authenticated)
                    # Stocker l'ID de l'utilisateur dans la session
                    request.session['user_standard'] = user_standard.id
                    
                    # Récupérer les informations du site lié à l'utilisateur connecté
                    site_blog = get_object_or_404(Site_Blog, id_sitepam__domaine=domaine)
                    


                    categories = Category_Blog.objects.all()

                    # Récupérer les publications mises en avant
                    featured_posts = Post_Blog.objects.filter(is_featured=True)

                    # Récupérer les articles de blog associés au site blog, triés par date de création
                    posts = Post_Blog.objects.filter(site=site_blog).order_by('-created_at')

                    # Récupérer les 5 derniers posts du site
                    latest_posts = Post_Blog.objects.filter(site=site_blog).order_by('-created_at')[:5]

                    initials = user_standard.initials

                    # Pagination
                    paginator = Paginator(posts, 4)  # 4 articles par page
                    page_number = request.GET.get('page')
                    try:
                        paginated_posts = paginator.page(page_number)
                    except PageNotAnInteger:
                        paginated_posts = paginator.page(1)  # Afficher la première page si le paramètre de la page n'est pas un entier
                    except EmptyPage:
                        paginated_posts = paginator.page(paginator.num_pages)  # Afficher la dernière page si la page demandée est vide

                    # Récupérer la couleur du site à partir de la base de données
                    site_color_name = site_blog.Couleur
                    color_map = {
                        'rouge': '#FF0000',
                        'vert': '#00FF00',
                        'bleu': '#0000FF',
                        # Ajoutez d'autres couleurs selon vos besoins
                    }
                    site_color_hex = color_map.get(site_color_name.lower(), '#000000')



                    # Rendre le modèle HTML avec le contexte
                    return render(request, 'site_view.html', {'user_authenticated': user_authenticated, 'site_color': site_color_hex, 'categories': categories, 'featured_posts' : featured_posts, 'site_blog': site_blog, 'posts': paginated_posts, 'latest_posts': latest_posts,'initials': initials, 'site_id': site_blog.id, 'domaine': domaine})
                else:
                    return HttpResponse("No user found sorry")
            else:
                return HttpResponse("Failed to login")
        else:
            return HttpResponse("Failed to login")

    return render(request, 'signin_blog.html', {'site_id': site_id, 'domaine': domaine})



def post_detail(request, domaine, post_title, site_id, post_id):
    # Récupérer les informations du site lié à l'utilisateur connecté
    site_blog = Site_Blog.objects.get(id=site_id)
    latest_posts = Post_Blog.objects.filter(site=site_blog).order_by('-created_at')
    post = get_object_or_404(Post_Blog, pk=post_id)
    categories = Category_Blog.objects.all()
    tags = Tag_Blog.objects.all()
    site_color_name = site_blog.Couleur
    color_map = {
        'rouge': '#FF0000',
        'vert': '#00FF00',
        'bleu': '#0000FF',
    }
    site_color_hex = color_map.get(site_color_name.lower(), '#000000')
    # Récupérer les commentaires associés au post
    comments = Comment_Blog.objects.filter(post=post)

    # Récupérer l'ID de l'utilisateur à partir de la session avec la clé 'user_standard'
    user_standard_id = request.session.get('user_standard')
    if user_standard_id:
        # Récupérer l'utilisateur standard correspondant
        user_standard = get_object_or_404(User_Standard, pk=user_standard_id)
        # Obtenir les initiales de l'utilisateur
        initials = user_standard.initials
        return render(request, 'post_detail.html', {'domaine': domaine, 'site_blog': site_blog, 'post': post, 'tags': tags, 'categories': categories, 'site_color': site_color_hex, 'site_id': site_blog.id, 'latest_posts': latest_posts, 'user_standard': user_standard, 'comments': comments, 'initials': initials, 'post_titles': post_title})
    else:
        user_standard = None

    return render(request, 'post_detail.html', {'domaine': domaine, 'site_blog': site_blog, 'post': post, 'tags': tags, 'categories': categories, 'site_color': site_color_hex, 'site_id': site_blog.id, 'latest_posts': latest_posts, 'user_standard': user_standard, 'comments': comments, 'post_titles': post_title})





def submit_comment(request, domaine, post_title, site_id, post_id):
    if request.method == 'POST':
        # Récupérer l'utilisateur actuellement connecté (s'il y en a un)
        user_standard_id = request.session.get('user_standard')
        # Récupérer les informations du site lié à l'utilisateur connecté
        site_blog = Site_Blog.objects.get(id=site_id)
        latest_posts = Post_Blog.objects.filter(site=site_blog).order_by('-created_at')
        post = get_object_or_404(Post_Blog, pk=post_id)
        categories = Category_Blog.objects.all()
        tags = Tag_Blog.objects.all()
        site_color_name = site_blog.Couleur
        color_map = {
            'rouge': '#FF0000',
            'vert': '#00FF00',
            'bleu': '#0000FF',
        }
        site_color_hex = color_map.get(site_color_name.lower(), '#000000')
        # Récupérer les commentaires associés au post
        comments = Comment_Blog.objects.filter(post=post)

        # Récupérer le contenu du commentaire à partir du formulaire
        content = request.POST.get('comment_content')


        if user_standard_id:
            # Récupérer l'objet User_Standard associé à l'identifiant
            user_standard = get_object_or_404(User_Standard, pk=user_standard_id)
            # Créer et enregistrer le commentaire dans la base de données avec l'utilisateur connecté comme auteur
            comment = Comment_Blog.objects.create(post=post, author=user_standard, content=content)
            comment.save()

        # Rediriger l'utilisateur vers la page de détail du post après avoir soumis le formulaire
        return render(request, 'post_detail.html', {'domaine': domaine, 'site_blog': site_blog, 'post': post, 'tags': tags, 'categories': categories, 'site_color': site_color_hex, 'site_id': site_blog.id, 'latest_posts': latest_posts, 'user_standard': user_standard, 'comments': comments, 'post_titles': post_title})
    else:
        # Si la méthode de requête n'est pas POST, vous pouvez gérer cela selon vos besoins
        return render(request, 'post_detail.html', {'domaine': domaine, 'site_blog': site_blog, 'post': post, 'tags': tags, 'categories': categories, 'site_color': site_color_hex, 'site_id': site_blog.id, 'latest_posts': latest_posts, 'user_standard': user_standard, 'comments': comments, 'post_titles': post_title})


import os
import requests
from django.views import View
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import JsonResponse

class DownloadResourcesView(View):
    def download_resource(self, url, folder):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Obtenir le nom du fichier ou du répertoire à partir de l'URL
            filename = os.path.join(folder, os.path.basename(url.rstrip('/')))
            # Créer le dossier parent s'il n'existe pas déjà
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            # Si l'URL se termine par '/', il s'agit d'un répertoire
            if url.endswith('/'):
                # Créer le répertoire
                os.makedirs(filename, exist_ok=True)
            else:
                # Écrire le fichier
                with open(filename, 'wb') as f:
                    response.raw.decode_content = True
                    f.write(response.content)
            print(f"Resource téléchargée : {url}")

    def download_html(self, url, folder):
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(folder, "index.html")  # Nommez le fichier HTML index.html
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"HTML téléchargé : {url}")

            # Remplacer le contenu du fichier site_view.html avec le contenu téléchargé
            with open(os.path.join(settings.BASE_DIR, 'blog', 'templates', 'site_view.html'), 'wb') as f:
                f.write(response.content)

    def get(self, request):
        url = request.GET.get('url')
        if url:
            response = requests.get(url)
            if response.status_code == 200:
                # Créer un dossier pour sauvegarder les ressources
                folder = "ressources"
                os.makedirs(folder, exist_ok=True)

                # Télécharger le contenu HTML de la page principale
                self.download_html(url, folder)

                # Afficher un popup informant que le template est disponible
                return JsonResponse({'message': 'Le template est disponible.'})

        return HttpResponse('URL invalide ou impossible de télécharger les ressources', status=400)





def pricing(request):
    plans = Plan.objects.all()
    context = {'plans' : plans}
    return render(request, "pricing.html", context)


def edit_post(request, post_id):
    # Récupérer l'utilisateur connecté
    user = request.user

    # Récupérer les informations du site lié à l'utilisateur connecté
    site = Sitewebpam.objects.filter(id_user=user).first()

    

    if site:

        user_info = User_Main.objects.get(username=user.username)
        user_add = Info_utilisateurs.objects.get(id_user=user)
        # Récupérer le post à éditer
        post = Post_Blog.objects.get(pk=post_id)
        categories = Category_Blog.objects.all()
        tags = Tag_Blog.objects.all()

        # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
        context = {
            'user_info': user_info,
            'user_add': user_add,
            'post': post,
            'categories': categories,
            'tags': tags,
            'domaine': site.domaine,
        }
        return render(request, 'edit_post.html', context)
    else:
        # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
        return HttpResponse("No site found for the user.")


def edit_post_logic(request, post_id):
    try:
        # Récupérer le post à éditer
        post = Post_Blog.objects.get(pk=post_id)
        # Récupérer l'utilisateur connecté
        user = request.user
        # Récupérer les informations du site lié à l'utilisateur connecté
        sitewebpam = Sitewebpam.objects.filter(id_user=user).first()
        

        if request.method == 'POST':
            # Récupérer les données du formulaire POST
            title = request.POST['title']
            image = request.FILES.get('image', None)
            content = request.POST['content']
            selected_categories = request.POST.getlist('categories')
            tags = request.POST.getlist('tags')

            # Récupérer la valeur du champ "featured" de la requête POST
            is_featured = request.POST.get('featured', False) == 'on'

            # Mettre à jour les champs du post avec les nouvelles données
            post.title = title
            if image:
                post.image = image
            post.content = content
            post.is_featured = is_featured

            # Supprimer toutes les catégories associées au post
            post.categories.clear()
            # Ajouter les catégories sélectionnées au post
            for category_id in selected_categories:
                category = Category_Blog.objects.get(pk=category_id)
                post.categories.add(category)
            # Enregistrer les modifications du post
            post.save()

            # Rediriger après l'édition
            return redirect('dashboard_blog', {'domaine': sitewebpam.domaine})

        else:
            # Si la méthode de requête n'est pas POST, pré-remplir le formulaire avec les données du post
            categories = Category_Blog.objects.all()
            tags = Tag_Blog.objects.all()
            context = {
                'post': post,
                'categories': categories,
                'tags': tags,
            }
            return render(request, 'edit_post.html', context)

    except Post_Blog.DoesNotExist:
        # Gérer le cas où le post avec l'ID donné n'existe pas
        return HttpResponse("Post does not exist")



def delete_post(request, post_id):
    post = get_object_or_404(Post_Blog, pk=post_id)
    post.delete()
    return redirect('dashboard_blog')




def like_post(request, post_id):
    # Récupérer l'utilisateur actuellement connecté (s'il y en a un)
    user_standard_id = request.session.get('user_standard')
    if user_standard_id:
        user_standard = get_object_or_404(User_Standard, pk=user_standard_id)
        post = get_object_or_404(Post_Blog, id=post_id)
        if not Like_Blog.objects.filter(post=post, user=user_standard).exists():
            like = Like_Blog.objects.create(post=post, user=user_standard)
            return JsonResponse({'message': 'Post liked successfully', 'post_id': post_id})
        else:
            return JsonResponse({'message': 'You already liked this post', 'post_id': post_id})
    else:
        return JsonResponse({'message': 'Authentication required', 'post_id': post_id})


def remove_like(request, post_id):
    # Récupérer l'utilisateur actuellement connecté (s'il y en a un)
    user_standard_id = request.session.get('user_standard')
    if user_standard_id:
        user_standard = get_object_or_404(User_Standard, pk=user_standard_id)
        post = get_object_or_404(Post_Blog, id=post_id)
        # Vérifier si un like existe pour ce post et cet utilisateur
        like = Like_Blog.objects.filter(post=post, user=user_standard).first()
        if like:
            like.delete()  # Supprimer le like de la base de données
            return JsonResponse({'message': 'Like removed successfully', 'post_id': post_id})
        else:
            return JsonResponse({'message': 'User not authenticated', 'post_id': post_id})
    else:
        return JsonResponse({'message': 'User not authenticated', 'post_id': post_id})


