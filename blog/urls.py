# urls.py de l'application "blog"
from django.urls import path

from . import views
from blog.views import view_site, create_post, create_category, create_tag, post_detail, submit_comment, register_blog, signin_blog, logout_blog

urlpatterns = [
    path('dashboard_blog/', views.dashboard_blog, name='dashboard_blog'),
    path('chat/', views.chat, name='chat'),
    path('theme', views.theme, name="theme"),
    path('manage', views.manage, name="manage"),
    path('<str:domaine>/', view_site, name='view_site'),
    path('create_post/<int:site_id>/', create_post, name="create_post"),
    
 

    path('create_category/<int:site_id>/', create_category, name='create_category'),
    path('create_tag/<int:site_id>/', create_tag, name='create_tag'),
    path('post/<str:domain>/<int:post_id>/', post_detail, name='post_detail'),
    path('submit_comment/<int:post_id>/', submit_comment, name='submit_comment'),
    path('<str:domain>/register_blog', register_blog, name="register_blog"),
    path('<str:domain>/signin_blog', signin_blog, name="signin_blog"),
    path('logout/', logout_blog, name='logout'),



]
