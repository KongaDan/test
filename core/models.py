from django.db import models
from datetime import date
from django.urls import reverse
from math import pow
OK = {
    'Yes': 'oui',
    'No': 'non',
}
SEX = {
        'M': 'Masculin',
        'F': 'Feminin'
    }
class Province(models.Model):
    code_province = models.BigAutoField(primary_key=True)
    nom_province = models.CharField(max_length=20, null=False)

    def __str__(self) -> str:
        return self.nom_province
    
class ZoneSanitaire(models.Model):
    code_zone = models.BigAutoField(primary_key=True)
    nom_zone = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=30, null=False)
    code_province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nom_zone

class AireSanitaire(models.Model):
    code_aire = models.BigAutoField(primary_key=True)
    nom_aire = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=20, null=True)
    code_zone = models.ForeignKey(ZoneSanitaire, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.nom_aire

class Enfant(models.Model):
    code_id = models.BigAutoField(primary_key=True)
    SEX = {
        'M': 'Masculin',
        'F': 'Feminin'
    }
    nom = models.CharField(max_length=25, null=True)
    postnom = models.CharField(max_length=25, null=False)
    prenom = models.CharField(max_length=25, null=True)
    sex = models.CharField(choices=SEX, max_length=10)
    date_naissance = models.DateField(blank=True,null=True)
    jour = models.IntegerField(null=False, blank=True)
    mois = models.IntegerField(null=False, blank=True)
    annee = models.IntegerField(null=False, blank=True)
    age_en_mois = models.IntegerField(null=True, blank=True)
    age_en_annee = models.IntegerField(null=False, blank=True)
    age_en_annee_mois = models.CharField(max_length=30, null=True, blank=True)
    age_en_annee_mois_jour = models.CharField(max_length=30, null=True, blank=True)
    age_inconnu = models.CharField(max_length=20, choices=OK)
    avenue = models.CharField(max_length=20, null=False)
    quartier = models.CharField(max_length=50, null=False)
    commune = models.CharField(max_length=20, null=True)
    ville = models.CharField(max_length=20, null=True)
    code_aire = models.ForeignKey(AireSanitaire, on_delete=models.CASCADE, null=True, blank=True)

    def age_in_years(self):
        today = date.today()
        self.age_en_annee = today.year - self.annee - ((today.month, today.day) < (self.mois, self.jour))
        return self.age_en_annee

    def age_in_months(self):
        today = date.today()
        self.age_en_mois = (today.year - self.annee) * 12 + today.month - self.mois - (
                today.day < self.jour)
        return self.age_en_mois

    def age_in_years_months(self):
        years = self.age_in_years()
        months = self.age_in_months() - years * 12
        self.age_en_annee_mois = f"{years} ans, {months} mois"

    def age_in_years_months_days(self):
        today = date.today()
        birthdate = date(self.annee, self.mois, self.jour)
        age = today - birthdate
        years = age.days // 365
        months = (age.days % 365) // 30
        days = (age.days % 365) % 30
        self.age_en_annee_mois_jour = f"{years} ans, {months} mois, {days} jours"

    def save(self, *args, **kwargs):
        # Extraire le jour, le mois et l'année de my_date_field
        if self.date_naissance:
            self.jour = self.date_naissance.day
            self.mois = self.date_naissance.month
            self.annee = self.date_naissance.year
            self.age_in_years_months()
            self.age_in_years_months_days()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class EtatInital(models.Model):
    numero = models.BigAutoField(primary_key=True)
    date_prelevement = models.DateField(null=False,auto_now=True)
    annee = models.IntegerField(null=False)
    mois = models.CharField(max_length=15)
    poids = models.FloatField(null=False)
    taille_en_cm = models.FloatField(null=False)
    taille_en_m = models.FloatField(null=False)
    z_score_pt = models.FloatField(null=False)
    imc = models.FloatField(null=False)
    z_score_imc_age = models.FloatField(null=False)
    pa = models.FloatField(null=False)
    pb = models.FloatField(null=True)
    oedeme_nutri = models.CharField(max_length=5, choices=OK)
    classification = models.CharField(max_length=20)
    code_id = models.ForeignKey(Enfant, on_delete=models.CASCADE)

    def __str__(self):
        return self.code_id.nom
    

    def calculate_imc(self):
        imc = self.poids / pow(int(self.taille_en_m),2 )
        self.imc = imc

    def calculate_z_score_pt(self):
        z_score = self.poids / self.taille_en_m
        self.z_score_pt = z_score

    def calculate_Z_score_imc_age(self):
        enfant = self.code_id
        if enfant.age_en_annee > 0:
            z_score = self.imc / enfant.age_en_annee
        else:
            z_score=0
        self.z_score_imc_age = z_score

    def calculate_pa(self):
        enfant = self.code_id
        pa = self.poids / enfant.age_en_annee
        self.pa = pa
    
    def get_absolute_url(self):
        return reverse("etat_initial_detail", kwargs={"pk": self.pk})
    
    def calculate_taille_m(self):
        cm = self.taille_en_cm
        self.taille_en_m = cm* 0.01
    
    def save(self, *args, **kwargs):
        self.calculate_imc()
        self.annee = date.today().year
        self.mois = date.today().month
        self.calculate_z_score_pt()
        self.calculate_Z_score_imc_age()
        super().save(*args, **kwargs)


class AnalyseSanguine(models.Model):
    date = models.DateField(null=False, auto_now_add=True)
    annee = models.IntegerField(null=False)
    mois = models.IntegerField(null=True)
    hemoglobine = models.FloatField(null=False)
    albumine = models.FloatField(null=False)
    azote_urique_sang = models.FloatField(null=False)
    creatinine = models.FloatField(null=False)
    uree_creatinine = models.FloatField(null=False)
    fer_serique = models.FloatField(null=False)
    ge = models.CharField(null=True, max_length=20)
    code_aire = models.ForeignKey(AireSanitaire, on_delete=models.CASCADE)
    code_id = models.ForeignKey(Enfant, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("analyse_sanguine_detail", kwargs={"pk": self.pk})
    
    

    def save(self, *args, **kwargs):
        self.annee = date.today().year
        self.mois = date.today().month
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.date}"


class Prelevement(models.Model):
    qte_spiruline_recue = models.FloatField(null=False)
    code_aire = models.ForeignKey(AireSanitaire, on_delete=models.CASCADE)
    numero = models.BigAutoField(primary_key=True)
    date_prelevement = models.DateField(null=False, auto_now=True)
    annee = models.IntegerField(null=True)
    mois = models.CharField(max_length=15)
    poids = models.FloatField(null=False)
    taille_en_cm = models.FloatField(null=False)
    taille_en_m = models.FloatField(null=False)
    z_score_pt = models.FloatField(null=True)
    imc = models.FloatField(null=False)
    z_score_imc_age = models.FloatField(null=True)
    pa = models.FloatField(null=False)
    pb = models.FloatField(null=True)
    oedeme_nutri = models.CharField(max_length=5, choices=OK)
    classification = models.CharField(max_length=20)
    code_id = models.ForeignKey(Enfant, on_delete=models.CASCADE)

    def calculate_imc(self):
        imc = self.poids / pow(int(self.taille_en_m) , 2)
        self.imc = imc

    def calculate_z_score_pt(self):
        z_score = self.poids / self.taille_en_m
        self.z_score_pt = z_score

    def calculate_Z_score_imc_age(self):
        enfant = self.code_id
        if enfant.age_en_annee > 0:
            z_score = self.imc / enfant.age_en_annee
        else:
            z_score=0
        self.z_score_imc_age = z_score

    def calculate_pa(self):
        enfant = self.code_id
        self.pa = self.poids / enfant.age_en_annee
    
    def get_absolute_url(self):
        return reverse("prelevement_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.code_id.nom
    
    def calculate_taille_m(self):
        cm = self.taille_en_cm
        self.taille_en_m = cm * 0.01

    def save(self, *args, **kwargs):
        self.calculate_imc()
        self.calculate_z_score_pt()
        self.calculate_Z_score_imc_age()
        self.annee = date.today().year
        self.mois = date.today().month
        super().save(*args, **kwargs)
            
            
        

