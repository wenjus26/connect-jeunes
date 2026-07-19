from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('blog/<uuid:uuid>/', views.article_detail, name='article_detail'),
    path('evenements/', views.evenements, name='evenements'),
    path('evenements/<uuid:uuid>/', views.evenement_detail, name='evenement_detail'),
    path('partenaires/', views.partenaires, name='partenaires'),
    path('programmes/', views.programmes, name='programmes'),
    path('projets/', views.projets, name='projets'),
    path('projets/<uuid:uuid>/', views.projet_detail, name='projet_detail'),
    path('galerie/', views.galerie, name='galerie'),
    path('don/', views.don, name='don'),
    path('contact/', views.contact, name='contact'),
    path('inscription-sommet/', views.inscription_sommet, name='inscription_sommet'),
    path('confirmation-inscription/', views.confirmation_inscription, name='confirmation_inscription'),

    # Location APIs
    path('ajax/get-communes/', views.get_communes, name='get_communes'),
    path('ajax/get-arrondissements/', views.get_arrondissements, name='get_arrondissements'),
    path('ajax/get-neighborhoods/', views.get_neighborhoods, name='get_neighborhoods'),

    # Newsletter subscription API
    path('ajax/subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
]
