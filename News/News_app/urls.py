from django.urls import path
from . import views

urlpatterns = [
   path('', views.article_misc, name='article-misc'),
   path('pol/', views.article_pol, name='article-pol'),
   path('world/', views.article_world, name='article-world'),
   path('tech/', views.article_tech, name='article-tech'),
]