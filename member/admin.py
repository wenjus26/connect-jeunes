import csv
from django.contrib import admin
from django.http import HttpResponse
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    Department, Commune, Arrondissement, Neighborhood,
    Partenaire, Member, BadgeMembre,
    Pilier, Temoignage, Projet, Evenement, Article, GalerieMedia,
    Newsletter, ContactMessage
)

# Custom admin site headers
admin.site.site_header = "Administration Connect Jeunes"
admin.site.site_title = "Portail Connect Jeunes Admin"
admin.site.index_title = "Tableau de Bord Administratif"


# CSV Export Action
def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename={meta.object_name.lower()}_export.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = []
        for field in field_names:
            val = getattr(obj, field)
            if hasattr(val, 'name'):  # Pour les clés étrangères ou pays
                row.append(str(val))
            else:
                row.append(val)
        writer.writerow(row)

    return response

export_as_csv.short_description = "Exporter la sélection en CSV"


# Inlines



# Geographic Admin configuration
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name',)
    ordering = ('department', 'name')


@admin.register(Arrondissement)
class ArrondissementAdmin(admin.ModelAdmin):
    list_display = ('name', 'commune')
    list_filter = ('commune__department', 'commune')
    search_fields = ('name',)
    ordering = ('commune', 'name')


@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'arrondissement')
    list_filter = ('arrondissement__commune',)
    search_fields = ('name',)
    ordering = ('arrondissement', 'name')


# Partenaire Admin
@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ('nom_entite', 'sigle', 'type_entite', 'zone_geographique', 'statut_partenariat')
    list_filter = ('type_entite', 'statut_partenariat')
    search_fields = ('nom_entite', 'sigle', 'email_contact', 'telephone')
    prepopulated_fields = {'slug': ('nom_entite',)}
    actions = [export_as_csv]


# Member Admin
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'nip', 'recommende_par', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'nip')
    list_filter = ('civility', 'country', 'department', 'commune', 'consent', 'created_at')
    readonly_fields = ('created_at',)
    actions = [export_as_csv]

    fieldsets = (
        ('Informations Personnelles', {
            'fields': ('civility', 'first_name', 'last_name', 'birth_date', 'profession')
        }),
        ('Coordonnées & Contact', {
            'fields': ('email', 'phone')
        }),
        ('Adresse & Origine', {
            'fields': ('country', 'department', 'commune', 'arrondissement', 'neighborhood', 'address', 'influence_zone')
        }),
        ('Parrainage & Consentements', {
            'fields': ('recommende_par', 'nip', 'consent')
        }),
        ('Métadonnées', {
            'classes': ('collapse',),
            'fields': ('created_at',)
        }),
    )


# Badge Admin
@admin.register(BadgeMembre)
class BadgeMembreAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'telephone', 'barcode_id', 'statut', 'date_creation')
    search_fields = ('nom_complet', 'telephone', 'barcode_id')
    list_filter = ('statut', 'date_creation')
    readonly_fields = ('date_creation',)
    actions = [export_as_csv]


# Models using Summernote rich editor
@admin.register(Pilier)
class PilierAdmin(SummernoteModelAdmin):
    list_display = ('titre', 'ordre', 'est_actif')
    list_editable = ('ordre', 'est_actif')
    summernote_fields = ('description',)


@admin.register(Projet)
class ProjetAdmin(SummernoteModelAdmin):
    list_display = ('titre', 'statut', 'lieu', 'avancement', 'actif')
    list_filter = ('statut', 'actif')
    list_editable = ('statut', 'avancement', 'actif')
    search_fields = ('titre', 'lieu')
    prepopulated_fields = {'slug': ('titre',)}
    summernote_fields = ('description',)
    actions = [export_as_csv]


@admin.register(Evenement)
class EvenementAdmin(SummernoteModelAdmin):
    list_display = ('titre', 'categorie', 'date_debut', 'lieu', 'est_a_ne_pas_manquer', 'actif')
    list_filter = ('categorie', 'date_debut', 'est_a_ne_pas_manquer', 'actif')
    list_editable = ('est_a_ne_pas_manquer', 'actif')
    search_fields = ('titre', 'lieu')
    prepopulated_fields = {'slug': ('titre',)}
    summernote_fields = ('contenu',)
    actions = [export_as_csv]


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('titre', 'auteur', 'date_publication', 'actif')
    list_filter = ('date_publication', 'actif')
    list_editable = ('actif',)
    search_fields = ('titre', 'auteur')
    prepopulated_fields = {'slug': ('titre',)}
    summernote_fields = ('contenu',)
    actions = [export_as_csv]


# Simple model registration
@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'fonction', 'ville', 'est_actif', 'ordre')
    list_filter = ('est_actif',)
    list_editable = ('est_actif', 'ordre')
    search_fields = ('auteur', 'ville')


@admin.register(GalerieMedia)
class GalerieMediaAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'date_creation', 'actif')
    list_filter = ('categorie', 'actif')
    list_editable = ('actif',)
    search_fields = ('titre',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'nom', 'status', 'date_subscription')
    list_filter = ('status', 'date_subscription')
    search_fields = ('email', 'nom')
    actions = [export_as_csv]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi', 'traite')
    list_filter = ('traite', 'date_envoi')
    list_editable = ('traite',)
    search_fields = ('nom', 'email', 'sujet')
    actions = [export_as_csv, 'mark_as_treated']

    def mark_as_treated(self, request, queryset):
        queryset.update(traite=True)
    mark_as_treated.short_description = "Marquer les messages sélectionnés comme traités"
