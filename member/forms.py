from django import forms
from .models import Member, ContactMessage, Newsletter, Department, Commune, Arrondissement, Neighborhood

class MemberForm(forms.ModelForm):
    nom_complet = forms.CharField(
        max_length=300,
        required=True,
        label="Nom Complet",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
            'placeholder': 'Ex: Jean Mukendi'
        })
    )

    class Meta:
        model = Member
        fields = [
            'civility', 'email', 'phone', 'birth_date', 'profession',
            'country', 'department', 'commune', 'arrondissement',
            'neighborhood',
            'nip', 'consent'
        ]
        widgets = {
            'civility': forms.Select(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'placeholder': 'jean.mukendi@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'placeholder': '+229 01 46 17 16 60'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'type': 'date'
            }),
            'profession': forms.TextInput(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'placeholder': 'Ex: Étudiant, Entrepreneur...'
            }),
            'country': forms.Select(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input'
            }),
            'department': forms.Select(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'id': 'id_department'
            }),
            'commune': forms.Select(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'id': 'id_commune'
            }),
            'arrondissement': forms.Select(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'id': 'id_arrondissement'
            }),
            'neighborhood': forms.Select(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'id': 'id_neighborhood'
            }),
            'nip': forms.TextInput(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'placeholder': 'Numéro d\'Identification Personnel (chiffres uniquement)'
            }),
            'consent': forms.CheckboxInput(attrs={
                'class': 'mt-1 w-5 h-5 rounded text-primary focus:ring-primary border-outline-variant'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On rend les listes vides au départ pour les filtres AJAX
        self.fields['department'].queryset = Department.objects.none()
        self.fields['commune'].queryset = Commune.objects.none()
        self.fields['arrondissement'].queryset = Arrondissement.objects.none()
        self.fields['neighborhood'].queryset = Neighborhood.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['department'].queryset = Department.objects.filter(id=department_id)
            except (ValueError, TypeError):
                pass
        else:
            self.fields['department'].queryset = Department.objects.all()

        if 'commune' in self.data:
            try:
                commune_id = int(self.data.get('commune'))
                self.fields['commune'].queryset = Commune.objects.filter(id=commune_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.department:
            self.fields['commune'].queryset = self.instance.department.communes.all()

        if 'arrondissement' in self.data:
            try:
                arrondissement_id = int(self.data.get('arrondissement'))
                self.fields['arrondissement'].queryset = Arrondissement.objects.filter(id=arrondissement_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.commune:
            self.fields['arrondissement'].queryset = self.instance.commune.arrondissements.all()

        if 'neighborhood' in self.data:
            try:
                neighborhood_id = int(self.data.get('neighborhood'))
                self.fields['neighborhood'].queryset = Neighborhood.objects.filter(id=neighborhood_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.arrondissement:
            self.fields['neighborhood'].queryset = self.instance.arrondissement.neighborhoods.all()

    def clean(self):
        cleaned_data = super().clean()
        nom_complet = cleaned_data.get('nom_complet')
        if nom_complet:
            parts = nom_complet.strip().split(' ', 1)
            if len(parts) == 2:
                cleaned_data['first_name'] = parts[0]
                cleaned_data['last_name'] = parts[1]
            else:
                cleaned_data['first_name'] = nom_complet
                cleaned_data['last_name'] = nom_complet
        return cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['nom', 'email', 'sujet', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'placeholder': 'Ex: Jean Dupont'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'placeholder': 'jean.dupont@email.com'
            }),
            'sujet': forms.TextInput(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'placeholder': 'Comment pouvons-nous vous aider ?'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input resize-none',
                'placeholder': 'Saisissez votre message...',
                'rows': 5
            })
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email', 'nom', 'consent_marketing', 'consent_data_processing']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'placeholder': 'Votre adresse email'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'w-full bg-surface-light border-outline-variant rounded-lg p-3 focus:border-primary focus:ring-0 transition-all outline-none form-input',
                'placeholder': 'Votre nom (optionnel)'
            }),
            'consent_marketing': forms.CheckboxInput(attrs={
                'class': 'mt-1 w-5 h-5 rounded text-primary focus:ring-primary border-outline-variant'
            }),
            'consent_data_processing': forms.CheckboxInput(attrs={
                'class': 'mt-1 w-5 h-5 rounded text-primary focus:ring-primary border-outline-variant'
            })
        }
