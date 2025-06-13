from django.urls import path

from App_Posts import views

app_name= 'App_Posts'

urlpatterns = [
    path('', views.home, name='home'),
    path('liked/<pk>/', views.liked, name='liked'),
    path('unliked/<pk>/',views.unliked, name='unliked'),
    path('delete/<pk>/', views.delete_post, name='delete_post'),
]

# path('profile/',views.profile, name='profile')