import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django_summernote.fields import SummernoteTextField

# -------------------------------
# Localisation & Géographie
# -------------------------------

class Department(models.Model):
    country = CountryField(default='BJ')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.country})"


class Commune(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='communes')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Arrondissement(models.Model):
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='arrondissements')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    arrondissement = models.ForeignKey(Arrondissement, on_delete=models.CASCADE, related_name='neighborhoods')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def validate_file_size(value):
    max_size = 2 * 1024 * 1024  # 2 Mo
    if value.size > max_size:
        raise ValidationError("Le fichier est trop volumineux (max 2 Mo autorisé).")


# -------------------------------
# Partenaires
# -------------------------------

class Partenaire(models.Model):
    nom_entite = models.CharField(
        max_length=255, 
        verbose_name=_("Nom de l'Entité/Organisation")
    )
    sigle = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name=_("Sigle / Acronyme")
    )
    TYPE_CHOICES = [
        ('ONG', 'ONG'),
        ('Association', 'Association de Jeunesse'),
        ('Mouvement', 'Mouvement Partenaire (ex: MMT)'),
        ('Institution', 'Institution / Organisation Publique'),
        ('Privé', 'Secteur Privé'),
    ]
    type_entite = models.CharField(
        max_length=50, 
        choices=TYPE_CHOICES, 
        default='Association', 
        verbose_name=_("Type de Partenaire")
    )
    logo = models.ImageField(
        upload_to='partenaires_logos/',
        blank=True, 
        null=True, 
        validators=[validate_file_size],
        verbose_name=_("Logo ou Image du Partenaire")
    )
    nom_contact_principal = models.CharField(
        max_length=100, 
        verbose_name=_("Nom du Contact Principal")
    )
    fonction_contact = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_("Fonction du Contact")
    )
    email_contact = models.EmailField(
        max_length=100, 
        unique=True, 
        verbose_name=_("Email (Principal)")
    )
    telephone_contact = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name=_("Téléphone")
    )
    domaine_action = models.CharField(
        max_length=255, 
        help_text=_("Ex: Artisanat, Citoyenneté, Environnement..."),
        verbose_name=_("Domaine d'Action Principal")
    )
    zone_geographique = models.CharField(
        max_length=255, 
        verbose_name=_("Zone Géographique d'Opération (Ex: Ouémé)")
    )
    nombre_membres = models.IntegerField(
        blank=True, 
        null=True, 
        verbose_name=_("Nombre de Membres / Bénéficiaires")
    )
    date_debut_partenariat = models.DateField(
        verbose_name=_("Date de Début du Partenariat")
    )
    STATUT_CHOICES = [
        ('Actif', 'Actif'),
        ('Veille', 'En Veille / Latent'),
        ('Terminé', 'Terminé'),
        ('Nego', 'En Négociation'),
    ]
    statut_partenariat = models.CharField(
        max_length=50, 
        choices=STATUT_CHOICES, 
        default='Veille', 
        verbose_name=_("Statut Actuel du Partenariat")
    )
    meta_title = models.CharField(max_length=255, blank=True, null=True, help_text="Titre SEO")
    meta_description = models.TextField(blank=True, null=True, help_text="Description SEO")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    
    objectifs_collaboration = models.TextField(
        verbose_name=_("Objectifs de la Collaboration"), 
        help_text=_("Description détaillée de la synergie et des buts communs.")
    )
    notes_suivi = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_("Notes de Suivi et Historique")
    )

    class Meta:
        verbose_name = _("Partenaire et Collaboration")
        verbose_name_plural = _("Partenaires et Collaborations")
        ordering = ['nom_entite']

    def __str__(self):
        return f"{self.nom_entite} ({self.sigle or self.type_entite})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom_entite)
        super().save(*args, **kwargs)


# -------------------------------
# Membres & Badges
# -------------------------------

CIVILITY_CHOICES = [
    ('Homme', 'Monsieur'),
    ('Femme', 'Madame'),
]

MOVEMENT_CHOICES = [
    ('aucun', 'Aucun'),
    ('caev', 'CAEV'),
]

name_validator = RegexValidator(
    regex=r'^[A-Za-zÀ-ÖØ-öø-ÿ \'-]+$',
    message="Ce champ ne peut contenir que des lettres, espaces ou tirets."
)

class Member(models.Model):
    civility = models.CharField(max_length=10, choices=CIVILITY_CHOICES)
    last_name = models.CharField(max_length=150, validators=[name_validator])
    first_name = models.CharField(max_length=150, validators=[name_validator])
    email = models.EmailField(
        unique=False,
        blank=True,
        null=True,
        error_messages={'unique': "Cet email est déjà utilisé."}
    )
    phone = PhoneNumberField(
        region='BJ',
        unique=False,
        blank=True,
        null=True,
        help_text="Numéro de téléphone (format international conseillé, ex: +22990000000)"
    )
    birth_date = models.DateField()
    profession = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    country = CountryField(default='BJ')

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)
    arrondissement = models.ForeignKey(Arrondissement, on_delete=models.SET_NULL, null=True, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.SET_NULL, null=True, blank=True)
    influence_zone = models.CharField(max_length=100, blank=True, null=True)
    recommende_par = models.ForeignKey(
        'Partenaire',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members_recommended",
        verbose_name="Qui vous a affilié ou parlé de Connect Jeunes ?"
    )
    nip = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(r'^[0-9]+$', 'Le NIP doit contenir uniquement des chiffres.')],
        error_messages={'unique': "Ce NIP existe déjà dans la base des adhérents."}
    )
    id_document = models.FileField(
        upload_to='members/id_documents/',
        validators=[validate_file_size],
        blank=True,
        null=True
    )
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('last_name', 'first_name', 'phone')
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        ordering = ['last_name', 'first_name']

    def clean(self):
        if not self.consent:
            raise ValidationError("Vous devez accepter les conditions pour soumettre le formulaire.")
        if self.country.code == 'BJ':
            if not self.department or not self.commune:
                raise ValidationError("Pour le Bénin, veuillez sélectionner le Département et la Commune.")

    def __str__(self):
        return f"{self.civility} {self.first_name} {self.last_name}"


class BadgeMembre(models.Model):
    nom_complet = models.CharField(
        max_length=200,
        verbose_name="Nom complet",
        db_index=True,
        unique=True
    )
    telephone = models.CharField(
        max_length=20,
        verbose_name="Numéro de téléphone",
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-\(\)]{8,20}$',
                message="Format de téléphone invalide"
            )
        ],
        db_index=True,
        unique=True
    )
    adresse = models.TextField(verbose_name="Adresse")
    barcode_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="ID Code-barres"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_confirmation = models.DateTimeField(auto_now=True, verbose_name="Date de confirmation")
    STATUT_CHOICES = (
        ('brouillon', 'Brouillon'),
        ('confirme', 'Confirmé'),
        ('telecharge', 'Téléchargé'),
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='brouillon',
        verbose_name="Statut"
    )
    telechargements_png = models.PositiveIntegerField(default=0, verbose_name="Téléchargements PNG")
    telechargements_pdf = models.PositiveIntegerField(default=0, verbose_name="Téléchargements PDF")
    session_id = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = "Badge Membre"
        verbose_name_plural = "Badges Membres"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.nom_complet} - {self.telephone}"


# -------------------------------
# Piliers d'Action (`programmes.html` & `index.html`)
# -------------------------------

class Pilier(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre du pilier")
    icone = models.CharField(
        max_length=100, 
        default="school", 
        help_text="Nom de l'icône Material Symbols Outlined (ex: school, diversity_3, payments, hub, science)"
    )
    description = SummernoteTextField(verbose_name="Description")
    ordre = models.IntegerField(default=1, verbose_name="Ordre d'affichage")
    est_actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Pilier d'Action"
        verbose_name_plural = "Piliers d'Action"
        ordering = ['ordre']

    def __str__(self):
        return self.titre


# -------------------------------
# Success Stories / Témoignages (`index.html`)
# -------------------------------

class Temoignage(models.Model):
    auteur = models.CharField(max_length=100, verbose_name="Nom de l'auteur")
    fonction = models.CharField(max_length=100, verbose_name="Fonction/Métier", blank=True)
    ville = models.CharField(max_length=100, verbose_name="Ville", blank=True)
    citation = models.TextField(verbose_name="Témoignage / Citation")
    photo = models.ImageField(upload_to='temoignages/', blank=True, null=True, verbose_name="Photo")
    est_actif = models.BooleanField(default=True, verbose_name="Afficher ce témoignage")
    ordre = models.IntegerField(default=1, verbose_name="Ordre d'affichage")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['ordre', '-date_creation']

    def __str__(self):
        return f"{self.auteur} ({self.ville})"


# -------------------------------
# Projets (`projets.html`)
# -------------------------------

class Projet(models.Model):
    STATUT_CHOICES = [
        ('avenir', 'À venir'),
        ('encours', 'En cours'),
        ('realise', 'Réalisé'),
    ]

    titre = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='realise')
    lieu = models.CharField(max_length=255, default="Savè, Bénin")
    description = SummernoteTextField(verbose_name="Description détaillée")
    image = models.ImageField(upload_to="projets/", blank=True, null=True)
    avancement = models.PositiveIntegerField(default=100, help_text="Pourcentage d'avancement (0 à 100)")
    avancement_label = models.CharField(max_length=100, default="100% Réalisé", help_text="Ex: 100+ jeunes formés")
    layout_large = models.BooleanField(default=False, help_text="Cochez pour afficher cette carte en format large (span 8 colonnes) au lieu de normal (span 4 colonnes)")
    actif = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True, help_text="Titre SEO")
    meta_description = models.TextField(blank=True, null=True, help_text="Description SEO")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)


# -------------------------------
# Événements (`evenements.html`)
# -------------------------------

class Evenement(models.Model):
    CATEGORIE_CHOICES = [
        ('solidarite', 'Solidarité'),
        ('exploration', 'Exploration'),
        ('inclusion', 'Inclusion'),
        ('orientation', 'Orientation'),
        ('autre', 'Autre'),
    ]

    titre = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES, default='orientation')
    date_debut = models.DateField()
    heure_debut = models.TimeField(blank=True, null=True)
    heure_fin = models.TimeField(blank=True, null=True)
    lieu = models.CharField(max_length=255, default="Savè, Bénin")
    image_principale = models.ImageField(upload_to="evenements/", blank=True, null=True)
    description_courte = models.TextField(help_text="Résumé rapide s'affichant sur les cartes de listing")
    contenu = SummernoteTextField(verbose_name="Contenu de l'événement (Summernote)")
    est_a_ne_pas_manquer = models.BooleanField(default=False, verbose_name="À la une / À ne pas manquer")
    actif = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True, help_text="Titre SEO")
    meta_description = models.TextField(blank=True, null=True, help_text="Description SEO")

    class Meta:
        ordering = ["-date_debut"]

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)


# -------------------------------
# Blog / Actualités (`blog.html`)
# -------------------------------

class Article(models.Model):
    titre = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    auteur = models.CharField(max_length=150, default="Équipe Connect Jeunes")
    description_courte = models.TextField(help_text="Résumé de l'article")
    contenu = SummernoteTextField(verbose_name="Contenu de l'article (Summernote)")
    image_principale = models.ImageField(upload_to="blog/", blank=True, null=True)
    date_publication = models.DateTimeField(default=timezone.now)
    actif = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True, help_text="Titre SEO")
    meta_description = models.TextField(blank=True, null=True, help_text="Description SEO")

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["-date_publication"]

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)


# -------------------------------
# Médiathèque / Galerie (`galerie.html`)
# -------------------------------

class GalerieMedia(models.Model):
    CATEGORIE_CHOICES = [
        ('orientation', 'Orientation'),
        ('formation', 'Formation'),
        ('solidarite', 'Solidarité'),
        ('exploration', 'Exploration'),
        ('inclusion', 'Inclusion'),
        ('autre', 'Autre'),
    ]

    titre = models.CharField(max_length=255)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES, default='orientation')
    image = models.ImageField(upload_to="galerie/")
    date_creation = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Média de la Galerie"
        verbose_name_plural = "Médias de la Galerie"
        ordering = ["-date_creation"]

    def __str__(self):
        return f"{self.titre} ({self.get_categorie_display()})"


# -------------------------------
# Newsletter & Contact
# -------------------------------

class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Adresse email")
    nom = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nom complet")
    consent_marketing = models.BooleanField(default=True, verbose_name="Accepte de recevoir des emails")
    consent_data_processing = models.BooleanField(default=True, verbose_name="Accepte le traitement des données")
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'En attente'), ('subscribed', 'Abonné'), ('unsubscribed', 'Désinscrit')], 
        default='subscribed'
    )
    date_subscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Abonnement Newsletter"
        verbose_name_plural = "Abonnements Newsletter"

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    nom = models.CharField(max_length=150, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Adresse email")
    sujet = models.CharField(max_length=255, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    date_envoi = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False, verbose_name="Message traité")

    class Meta:
        verbose_name = "Message de Contact"
        verbose_name_plural = "Messages de Contact"
        ordering = ["-date_envoi"]

    def __str__(self):
        return f"{self.nom} - {self.sujet}"
