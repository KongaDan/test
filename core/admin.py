from django.contrib import admin
from .models import *

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['code_province','nom_province']
    list_filter = ['code_province']

@admin.register(ZoneSanitaire)
class ZoneSanitaireAdmin(admin.ModelAdmin):
    list_display = ('code_zone','nom_zone','address','code_province')
    list_filter=['code_zone']

@admin.register(AireSanitaire)
class AireSanitaireAdmin(admin.ModelAdmin):
    list_display = ('code_aire','nom_aire','address','code_zone')
    list_filter = ['code_aire']

@admin.register(Enfant)
class EnfantAdmin(admin.ModelAdmin):
    list_display = ('code_id','nom', 'postnom', 'prenom', 'date_naissance', 'quartier')
    empty_value_display = '-empty-'
    list_filter = ['code_id']

@admin.register(Prelevement)
class PrelevementAdmin(admin.ModelAdmin):
    list_display =['numero',"qte_spiruline_recue",'date_prelevement','code_id']

@admin.register(AnalyseSanguine)
class AnalyseSanguineAdmin(admin.ModelAdmin):
    list_display=['date','hemoglobine','albumine','code_id','code_aire']

@admin.register(EtatInital)
class EtatInitialAdmin(admin.ModelAdmin):
    list_display=['numero','date_prelevement','code_id']