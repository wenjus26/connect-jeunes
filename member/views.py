import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import (
    Pilier, Temoignage, Projet, Evenement, Article, GalerieMedia,
    Partenaire, Member, BadgeMembre, ContactMessage, Newsletter,
    Department, Commune, Arrondissement, Neighborhood
)
from .forms import MemberForm, ContactForm, NewsletterForm

# -------------------------------
# Page Views
# -------------------------------

def index(request):
    context = {
        'piliers': Pilier.objects.filter(est_actif=True)[:4],
        'temoignages': Temoignage.objects.filter(est_actif=True)[:3],
        'articles': Article.objects.filter(actif=True)[:3],
        'featured_event': Evenement.objects.filter(actif=True, est_a_ne_pas_manquer=True).first(),
        'partenaires': Partenaire.objects.filter(statut_partenariat='Actif')[:6],
    }
    return render(request, 'index.html', context)


def blog(request):
    context = {
        'articles': Article.objects.filter(actif=True),
    }
    return render(request, 'blog.html', context)


def evenements(request):
    context = {
        'featured_event': Evenement.objects.filter(actif=True, est_a_ne_pas_manquer=True).first(),
        'evenements': Evenement.objects.filter(actif=True),
    }
    return render(request, 'evenements.html', context)


def partenaires(request):
    context = {
        'partenaires': Partenaire.objects.filter(statut_partenariat='Actif'),
    }
    return render(request, 'partenaires.html', context)


def programmes(request):
    context = {
        'piliers': Pilier.objects.filter(est_actif=True),
    }
    return render(request, 'programmes.html', context)


def projets(request):
    context = {
        'projets': Projet.objects.filter(actif=True),
    }
    return render(request, 'projets.html', context)


def galerie(request):
    context = {
        'medias': GalerieMedia.objects.filter(actif=True),
    }
    return render(request, 'galerie.html', context)


def don(request):
    return render(request, 'don.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Votre message a été envoyé avec succès !'})
            messages.success(request, 'Votre message a été envoyé avec succès !')
            return redirect('contact')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def inscription_sommet(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.first_name = form.cleaned_data.get('first_name')
            member.last_name = form.cleaned_data.get('last_name')
            member.save()

            # Auto-générer un BadgeMembre pour ce membre
            nom_complet = f"{member.first_name} {member.last_name}"
            barcode_id = f"CJ-{uuid.uuid4().hex[:8].upper()}"
            badge, _ = BadgeMembre.objects.get_or_create(
                nom_complet=nom_complet,
                telephone=str(member.phone) if member.phone else f"N/A-{barcode_id}",
                defaults={
                    'adresse': member.address or "Bénin",
                    'barcode_id': barcode_id,
                    'statut': 'confirme'
                }
            )

            # Stocker les infos dans la session pour la page de confirmation
            request.session['registered_member_name'] = nom_complet
            request.session['registered_member_phone'] = badge.telephone
            request.session['registered_member_barcode'] = badge.barcode_id

            return redirect('confirmation_inscription')
        else:
            # En cas d'erreur de formulaire
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = MemberForm()
    
    # Pré-charger tous les départements pour le sélecteur
    departments = Department.objects.all().order_by('name')
    partenaires_mouvements = Partenaire.objects.all().order_by('nom_entite')
    
    return render(request, 'inscription-sommet.html', {
        'form': form,
        'departments': departments,
        'partenaires_mouvements': partenaires_mouvements
    })


def confirmation_inscription(request):
    # Récupérer les infos de la session
    nom_complet = request.session.get('registered_member_name', 'Visiteur')
    telephone = request.session.get('registered_member_phone', '')
    barcode_id = request.session.get('registered_member_barcode', '')
    
    context = {
        'nom_complet': nom_complet,
        'telephone': telephone,
        'barcode_id': barcode_id,
    }
    return render(request, 'confirmation-inscription.html', context)


# -------------------------------
# AJAX Location Endpoints
# -------------------------------

def get_communes(request):
    department_id = request.GET.get('department_id')
    communes = Commune.objects.filter(department_id=department_id).order_by('name')
    return JsonResponse(list(communes.values('id', 'name')), safe=False)


def get_arrondissements(request):
    commune_id = request.GET.get('commune_id')
    arrondissements = Arrondissement.objects.filter(commune_id=commune_id).order_by('name')
    return JsonResponse(list(arrondissements.values('id', 'name')), safe=False)


def get_neighborhoods(request):
    arrondissement_id = request.GET.get('arrondissement_id')
    neighborhoods = Neighborhood.objects.filter(arrondissement_id=arrondissement_id).order_by('name')
    return JsonResponse(list(neighborhoods.values('id', 'name')), safe=False)


# -------------------------------
# Newsletter Handler
# -------------------------------

@require_POST
def subscribe_newsletter(request):
    email = request.POST.get('email', '').strip()
    nom = request.POST.get('nom', '').strip()
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Adresse email manquante.'})
    
    subscription, created = Newsletter.objects.get_or_create(
        email=email,
        defaults={
            'nom': nom or None,
            'status': 'subscribed',
            'consent_marketing': True,
            'consent_data_processing': True
        }
    )
    if not created:
        if subscription.status == 'unsubscribed':
            subscription.status = 'subscribed'
            subscription.save()
            return JsonResponse({'status': 'success', 'message': 'Votre abonnement a été réactivé !'})
        return JsonResponse({'status': 'info', 'message': 'Vous êtes déjà inscrit à notre newsletter.'})
        
    return JsonResponse({'status': 'success', 'message': 'Merci de votre inscription à la newsletter !'})


def article_detail(request, uuid):
    article = get_object_or_404(Article, uuid=uuid, actif=True)
    recent_articles = Article.objects.filter(actif=True).exclude(uuid=uuid)[:3]
    return render(request, 'article_detail.html', {'article': article, 'recent_articles': recent_articles})


def projet_detail(request, uuid):
    projet = get_object_or_404(Projet, uuid=uuid, actif=True)
    other_projets = Projet.objects.filter(actif=True).exclude(uuid=uuid)[:3]
    return render(request, 'projet_detail.html', {'projet': projet, 'other_projets': other_projets})


def evenement_detail(request, uuid):
    evenement = get_object_or_404(Evenement, uuid=uuid, actif=True)
    other_events = Evenement.objects.filter(actif=True).exclude(uuid=uuid)[:3]
    return render(request, 'evenement_detail.html', {'evenement': evenement, 'other_events': other_events})


# -------------------------------
# Member Dashboard Views
# -------------------------------

def member_dashboard(request):
    member_id = request.session.get('member_id')
    member = None
    if member_id:
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            request.session.pop('member_id', None)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Login
        if action == 'login':
            email = request.POST.get('email', '').strip()
            nip_or_phone = request.POST.get('nip_or_phone', '').strip()
            
            member_found = Member.objects.filter(
                Q(email__iexact=email) & (Q(nip=nip_or_phone) | Q(phone=nip_or_phone))
            ).first()
            
            if member_found:
                request.session['member_id'] = member_found.id
                messages.success(request, f"Ravi de vous revoir, {member_found.first_name} !")
                return redirect('member_dashboard')
            else:
                messages.error(request, "Aucun membre trouvé avec ces identifiants de connexion.")
                
        # Profile Update
        elif action == 'update_profile' and member:
            profession = request.POST.get('profession', '').strip()
            address = request.POST.get('address', '').strip()
            
            member.profession = profession
            member.address = address
            member.save()
            
            # Update badge address if it exists
            badge = BadgeMembre.objects.filter(telephone=str(member.phone)).first()
            if badge:
                badge.adresse = address
                badge.save()
                
            messages.success(request, "Votre profil a été mis à jour avec succès !")
            return redirect('member_dashboard')

    if member:
        badge = BadgeMembre.objects.filter(telephone=str(member.phone)).first()
        upcoming_events = Evenement.objects.filter(actif=True).order_by('date_debut')[:3]
        active_projects = Projet.objects.filter(actif=True)[:3]
        
        return render(request, 'dashboard.html', {
            'member': member,
            'badge': badge,
            'upcoming_events': upcoming_events,
            'active_projects': active_projects
        })

    return render(request, 'dashboard_login.html')


def member_logout(request):
    request.session.pop('member_id', None)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('member_dashboard')
