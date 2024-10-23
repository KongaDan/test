from django import forms
from .models import *

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ['nom_province']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom_province'].widget.attrs.update({'class':'form-control',})

class ZoneSanitaireForm(forms.ModelForm):
    class Meta:
        model = ZoneSanitaire
        fields = ['nom_zone', 'address','code_province']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom_zone'].widget.attrs.update({'class':'form-control',})
        self.fields['address'].widget.attrs.update({'class':'form-control',})
        self.fields['code_province'].widget.attrs.update({'class':'form-control',})

class AireSanitaireForm(forms.ModelForm):
    class Meta:
        model = AireSanitaire
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom_aire'].widget.attrs.update({'class':'form-control',})
        self.fields['address'].widget.attrs.update({'class':'form-control',})
        self.fields['code_zone'].widget.attrs.update({'class':'form-control',})

class EnfantForm(forms.ModelForm):
    class Meta:
        model = Enfant
        fields = ['nom', 'postnom', 'prenom', 'sex', 'date_naissance', 'avenue', 'quartier', 'commune', 'ville','code_aire']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom'].widget.attrs.update({'class':'form-control','placeholder':'Nom'})
        self.fields['prenom'].widget.attrs.update({'class':'form-control','placeholder':'Prenom'})
        self.fields['postnom'].widget.attrs.update({'class':'form-control','placeholder':'Postnom'})
        self.fields['sex'].widget.attrs.update({'class':'form-control','placeholder':'Prenom'})
        self.fields['date_naissance'].widget.attrs.update({'class':'form-control','placeholder':'Date naissance'})
        self.fields['avenue'].widget.attrs.update({'class':'form-control','placeholder':'Avenue'})
        self.fields['quartier'].widget.attrs.update({'class':'form-control','placeholder':'Quartier'})
        self.fields['commune'].widget.attrs.update({'class':'form-control','placeholder':'Commune'})
        self.fields['ville'].widget.attrs.update({'class':'form-control','placeholder':'Ville'})
        self.fields['code_aire'].widget.attrs.update({'class':'form-control','placeholder':'Aire Sanitaire'})


class PrelevementForm(forms.ModelForm):
    class Meta:
        model = Prelevement
        fields = [ 'poids', 'taille_en_cm', 'oedeme_nutri', 'classification','qte_spiruline_recue']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['poids'].widget.attrs.update({'class':'form-control','placeholder':'poids'})
        self.fields['taille_en_cm'].widget.attrs.update({'class':'form-control','placeholder':'taille_en_cm'})
        self.fields['oedeme_nutri'].widget.attrs.update({'class':'form-control','placeholder':'oedeme_nutri'})
        self.fields['classification'].widget.attrs.update({'class':'form-control','placeholder':'classification'})
        self.fields['qte_spiruline_recue'].widget.attrs.update({'class':'form-control','placeholder':'qte_spiruline_recue'})

class AnalyseSanguineForm(forms.ModelForm):
    class Meta:
        model = AnalyseSanguine
        fields = [ 'hemoglobine', 'albumine', 'azote_urique_sang', 'creatinine', 'uree_creatinine','fer_serique', 'ge']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hemoglobine'].widget.attrs.update({'class':'form-control','placeholder':'hemoglobine'})
        self.fields['albumine'].widget.attrs.update({'class':'form-control','placeholder':'albumine'})
        self.fields['azote_urique_sang'].widget.attrs.update({'class':'form-control','placeholder':'azote_urique_sang'})
        self.fields['creatinine'].widget.attrs.update({'class':'form-control','placeholder':'creatinine'})
        self.fields['uree_creatinine'].widget.attrs.update({'class':'form-control','placeholder':'uree_creatinine'})
        self.fields['fer_serique'].widget.attrs.update({'class':'form-control','placeholder':'fer_serique'})
        self.fields['ge'].widget.attrs.update({'class':'form-control','placeholder':'ge'})

class EnfantSearchForm(forms.Form):
   name = forms.CharField(max_length=50, required=True)
   prenom = forms.CharField(max_length=40, required=True)
   postnom = forms.CharField(max_length=40,required=True)
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-control','placeholder':'name'})
        self.fields['prenom'].widget.attrs.update({'class':'form-control','placeholder':'prenom'})
        self.fields['postnom'].widget.attrs.update({'class':'form-control','placeholder':'postnom'})