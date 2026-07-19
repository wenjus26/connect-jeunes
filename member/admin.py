from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    Department, Commune, Arrondissement, Neighborhood,
    Partenaire, Member, BadgeMembre,
    Pilier, Temoignage, Projet, Evenement, Article, GalerieMedia,
    Newsletter, ContactMessage
)

# Geographic Admin configuration
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)

@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name',)

@admin.register(Arrondissement)
class ArrondissementAdmin(admin.ModelAdmin):
    list_display = ('name', 'commune')
    list_filter = ('commune__department', 'commune')
    search_fields = ('name',)

@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'arrondissement')
    list_filter = ('arrondissement__commune',)
    search_fields = ('name',)


# Partenaire Admin
@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ('nom_entite', 'sigle', 'type_entite', 'zone_geographique', 'statut_partenariat')
    list_filter = ('type_entite', 'statut_partenariat')
    search_fields = ('nom_entite', 'sigle', 'email_contact')
    prepopulated_fields = {'slug': ('nom_entite',)}


# Member Admin
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'nip', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'nip')
    list_filter = ('civility', 'country', 'department', 'commune', 'consent')


# Badge Admin
@admin.register(BadgeMembre)
class BadgeMembreAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'telephone', 'barcode_id', 'statut', 'date_creation')
    search_fields = ('nom_complet', 'telephone', 'barcode_id')
    list_filter = ('statut',)


# Models using Summernote rich editor
@admin.register(Pilier)
class PilierAdmin(SummernoteModelAdmin):
    list_display = ('titre', 'ordre', 'est_actif')
    summernote_fields = ('description',)

@admin.register(Projet)
class ProjetAdmin(SummernoteModelAdmin):
    list_display = ('titre', 'statut', 'lieu', 'avancement_label', 'actif')
    list_filter = ('statut', 'actif')
    search_fields = ('titre', 'lieu')
    prepopulated_fields = {'slug': ('titre',)}
    summernote_fields = ('description',)

@admin.register(Evenement)
class EvenementAdmin(SummernoteModelAdmin):
    list_display = ('titre', 'categorie', 'date_debut', 'lieu', 'est_a_ne_pas_manquer', 'actif')
    list_filter = ('categorie', 'date_debut', 'est_a_ne_pas_manquer', 'actif')
    search_fields = ('titre', 'lieu')
    prepopulated_fields = {'slug': ('titre',)}
    summernote_fields = ('contenu',)

@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('titre', 'auteur', 'date_publication', 'actif')
    list_filter = ('date_publication', 'actif')
    search_fields = ('titre', 'auteur')
    prepopulated_fields = {'slug': ('titre',)}
    summernote_fields = ('contenu',)


# Simple model registration
@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'fonction', 'ville', 'est_actif', 'ordre')
    list_filter = ('est_actif',)
    search_fields = ('auteur', 'ville')

@admin.register(GalerieMedia)
class GalerieMediaAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'date_creation', 'actif')
    list_filter = ('categorie', 'actif')
    search_fields = ('titre',)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'nom', 'status', 'date_subscription')
    list_filter = ('status',)
    search_fields = ('email', 'nom')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi', 'traite')
    list_filter = ('traite', 'date_envoi')
    search_fields = ('nom', 'email', 'sujet')
