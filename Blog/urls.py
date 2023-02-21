
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('signout/', views.signout, name="signout"),
    path('login/',
         LoginView.as_view(template_name='Blog/login.html'),
         name='login'),
    path('create_post/', views.CreatePost, name='CreatePost'),
    path('single_post/<int:pk>/', views.single_post, name="single_post"),
    path('search_results/', views.search_results, name='search_results'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('delete_post/<int:pk>/', views.delete_post, name="delete_post"),
    path('edit_post/<int:pk>/', views.edit_post, name="edit_post"),
    path('edit_post_images/<int:pk>/', views.edit_post_images, name="edit_post_images"),
    path('delete_comment/<int:pk>/', views.delete_comment, name="delete_comment"),
    path('delete_post_image/<int:pk>/', views.delete_post_image, name="delete_post_image"),
    
]
