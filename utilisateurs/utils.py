from django.shortcuts import redirect

def redirect_to_site(request):
    if request.user.is_authenticated:
        return redirect('site_creation')  # Rediriger vers la page de création de site si l'utilisateur est connecté
    else:
        return redirect('signin')  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
