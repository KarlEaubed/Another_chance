from django.urls import path, include
from blog.views import DownloadResourcesView, delete_post, edit_post, edit_post_logic, like_post, menu, dashboard_blog, logout_blog, manage, pricing, remove_like, signin_blog, submit_comment, marketplace, view_site, create_category, create_post, create_tag, post_detail, register_blog
from utilisateurs import views as utilisateurs_views  # Alias pour les vues de l'application "utilisateurs"
from portofolio.views import *

urlpatterns = [
    path('', utilisateurs_views.home, name="home"),
    path('signup', utilisateurs_views.signup, name="signup"),
    path('signin', utilisateurs_views.signin, name="signin"),
    path('logout', utilisateurs_views.logOut, name="logout"),
    path('setup_account', utilisateurs_views.setup_account, name="setup_account"),
    path('activate/<uidb64>/<token>', utilisateurs_views.activate, name='activate'),
    path('site_creation/', utilisateurs_views.site_creation, name='site_creation'),
    
    path('create_admin_blog/<int:site_id>/', utilisateurs_views.create_admin_blog, name='create_admin_blog'),

    path('create_site_blog/<int:site_id>/<int:admin_id>/', utilisateurs_views.create_site_blog, name='create_site_blog'),
    path('dashboard_blog/<str:domaine>/', dashboard_blog, name='dashboard_blog'),
    path('marketplace/', marketplace, name='marketplace'),
    path('menu/<str:domaine>/', menu, name='menu'),
    path('manage/', manage, name='manage'),
    path('<str:domaine>/', view_site, name='view_site'),
    path('create_post/<int:site_id>/', create_post, name="create_post"),
    
 

    path('create_category/<int:site_id>/', create_category, name='create_category'),
    path('create_tag/<int:site_id>/', create_tag, name='create_tag'),
    path('<str:domaine>/<str:post_title>/<int:site_id>/<int:post_id>/', post_detail, name='post_detail'),
    path('submit_comment/<str:domaine>/<str:post_title>/<int:site_id>/<int:post_id>/', submit_comment, name='submit_comment'),

    path('<str:domaine>/<int:site_id>/register_blog', register_blog, name="register_blog"),
    path('<str:domaine>/<int:site_id>/signin_blog', signin_blog, name="signin_blog"),
    path('logout/', logout_blog, name='logout'),
    path('DownloadResourcesView', DownloadResourcesView.as_view(), name='DownloadResourcesView'),
    path('payment', utilisateurs_views.payment, name="payment"),
    path('payment_moncash', utilisateurs_views.payment_moncash, name="payment_moncash"),
    # path('paypal/', include('paypal.standard.ipn.urls')),
    
    
    
    path('create_site_portofolio/<int:site_id>/', create_site_portofolio, name='create_site_portofolio'),
    path('dashboardportoo/<str:domaine>/', dashboardportofolio, name='dashboardportofolio'),
    path('view_site_portofolio/<str:domaine>/', view_site_portofolio, name='view_site_portofolio'),
    path('add_service/<int:site_id>/', add_service, name='add_service'),
    path('modif_service/<int:service_id>/', modif_service, name='modif_service'),
    path('add_info/<int:site_id>/',add_info, name='add_info'),
    path('add_about/<int:site_id>/',add_about, name='add_about'),
    path('add_pro/<int:site_id>/',add_pro, name='add_pro'),
    path('add_hero/<int:site_id>/',add_hero, name='add_hero'),

    path('checkout/<int:plan_id>/', utilisateurs_views.checkout, name='checkout'),
    path('complete/<int:plan_id>/', utilisateurs_views.paymentcomplete, name="complete"),
    path('pricing', pricing, name="pricing"),
    path('edit_post/<int:post_id>/', edit_post, name="edit_post"),
    path('edit_post_logic/<int:post_id>/', edit_post_logic, name='edit_post_logic'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('remove_like/<int:post_id>/', remove_like, name='remove_like'),


]



    


    # path('accounts/', include('allauth.urls')),