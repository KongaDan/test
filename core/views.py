from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import login,authenticate,logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta
date_actuelle = datetime.now().date()
deux_semaines= timedelta(weeks=2)


@login_required
def index(request):
    return render(request,'index.html')

@login_required
def stat_province(request):
    provinces = Province.objects.all()
    return render(request,'stat_province.html',{'provinces':provinces})


@login_required
def stat_zone(request):
    zone_sanitaires = ZoneSanitaire.objects.all()
    return render(request,'stat_zone.html',{'zone_sanitaires':zone_sanitaires})

@login_required
def stat_aire(request):
    aire_sanitaires = AireSanitaire.objects.all()
    return render(request,'stat_aire.html',{'aire_sanitaires':aire_sanitaires})

def login_page(request):
    if request.method=='POST':
        name=request.POST['username']
        pword=request.POST['password']
        user=authenticate(request,username=name,password=pword)
        if user is not  None:
            login(request,user )
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            message='l\'email ou le mot de passe est incorrecte '
            return render(request,'login.html',{'message':message})
    return render(request,'login.html')

@login_required
def logout_page(request):
    logout(request)
    return redirect(settings.LOGIN_URL)

@login_required
def province_list(request):
    provinces = Province.objects.all()
    return render(request,'province_list.html',{'provinces':provinces})

@login_required
def zone_sanitaire_list(request): 
    zone_sanitaires = ZoneSanitaire.objects.all()
    return render(request,'zone_sanitaire_list.html',{'zone_sanitaires':zone_sanitaires,'view':'create'})

@login_required
def aire_sanitaire_list(request):
    aire_sanitaires = AireSanitaire.objects.all()
    return render(request,'aire_sanitaire_list.html',{'aire_sanitaires':aire_sanitaires})

@login_required
def province_create(request):
    view = 'Nouvelle'
    form = ProvinceForm()
    if request.method =="POST":
        form = ProvinceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:province_list')
    return render(request,'province_create.html',{'form':form,'view':view})

@login_required
def zone_sanitaire_create(request):
    view = 'Nouvelle'
    form = ZoneSanitaireForm()
    if request.method=="POST":
        form = ZoneSanitaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:zone_sanitaire_list')
    return render(request,'zone_sanitaire_create.html',{'form':form,'view':view})

@login_required
def aire_sanitaire_create(request):
    form = AireSanitaireForm()
    view = 'Nouvelle'
    if request.method == "POST":
        form = AireSanitaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:aire_sanitaire_list')
    return render(request,'aire_sanitaire_create.html',{'form':form,'view':view})

@login_required
def province_update(request, pk):
    view='Modifier'
    province = Province.objects.get(pk=pk)
    form = ProvinceForm(instance = province)
    if request.method == "POST":
        form = ProvinceForm(request.POST,instance = province)
        if form.is_valid():
            form.save()
        return redirect('core:province_list')
    return render(request,'province_create.html',{'form':form,'view':view})

@login_required
def zone_sanitaire_update(request, pk):
    view = 'Modifier'
    zone_sanitaire = ZoneSanitaire.objects.get(pk=pk)
    form = ZoneSanitaireForm(instance = zone_sanitaire)
    if request.method == "POST":
        form = ZoneSanitaireForm(request.POST,instance = zone_sanitaire)
        if form.is_valid():
            form.save()
        return redirect('core:zone_sanitaire_list')
    return render(request,'zone_sanitaire_create.html',{'form':form,'view':view})

@login_required
def aire_sanitaire_update(request, pk):
    view = 'Modifier'
    aire_sanitaire = AireSanitaire.objects.get(pk=pk)
    form = AireSanitaireForm(instance = aire_sanitaire)
    if request.method == "POST":
        form = AireSanitaireForm(request.POST,instance = aire_sanitaire)
        if form.is_valid():
            form.save()
        return redirect('core:aire_sanitaire_list')
    return render(request,'aire_sanitaire_create.html',{'form':form,'view':view})

def enfant_create(request):
    view='Entrer'
    form = EnfantForm()
    if request.method =="POST":
        form = EnfantForm(request.POST)
        if form.is_valid():
            enfant = form.save()
            context={
                'enfant':enfant
            }
            return render(request,'enfant_suite.html',context)
    return render(request,'enfant_create.html',{'form':form,'view':view})

def etat_initial_create(request,pk):
    view="Nouveau Prelevement"
    enfant = Enfant.objects.get(pk=pk)
    form = PrelevementForm()
    context={
        'form':form,
        'enfant':enfant,
        'view':view
    }
    if request.method=="POST":
        form = PrelevementForm(request.POST)
        if form.is_valid():
            prelevement= form.save(commit=False)

            #methode modele

            taille_en_cm = form.cleaned_data['taille_en_cm']
            taille_en_m= taille_en_cm/100
            poids = form.cleaned_data['poids']
            if enfant.age_en_annee > 0:
                pa= poids/enfant.age_en_annee
            else :
                pa= 1
            prelevement.code_id = enfant
            prelevement.code_aire = enfant.code_aire
            prelevement.taille_en_m = taille_en_m
            prelevement.pa = pa
            prelevement.save()
            EtatInital.objects.create(
                taille_en_m= taille_en_m,
                pa=pa,
                poids=prelevement.poids,
                taille_en_cm=prelevement.taille_en_cm,
                pb=prelevement.pb,
                oedeme_nutri=prelevement.oedeme_nutri,
                classification=prelevement.classification,
                code_id=enfant
            )
            context={
                'enfant':enfant,
                'prelevement':prelevement,
                'view':view
            }
            return render(request,'enfant_suite.html',context)
    return render(request,'prelevement_create.html',context)

def prelevement_create(request,pk):
    view="Nouveau Prelevement"
    enfant = Enfant.objects.get(pk=pk)
    form = PrelevementForm()
    prelevement_last= Prelevement.objects.filter(code_id=enfant).last()
    if prelevement_last:
        if date_actuelle - prelevement_last.date_prelevement >= deux_semaines:
            permis = True
        else :
            permis = False
    else :
        permis = True
    context={
        'form':form,
        'enfant':enfant,
        'view':view,
        'prelevement_last':prelevement_last,
        'permis':permis,
    }
    if request.method=="POST":
        form = PrelevementForm(request.POST)
        if form.is_valid():
            prelevement= form.save(commit=False)
             #methode modele

            taille_en_cm = form.cleaned_data['taille_en_cm']
            taille_en_m= taille_en_cm/100
            poids = form.cleaned_data['poids']
            if enfant.age_en_annee > 0:
                pa= poids/enfant.age_en_annee
            else :
                pa= 1
            prelevement.code_id = enfant
            prelevement.code_aire = enfant.code_aire
            prelevement.taille_en_m = taille_en_m
            prelevement.pa = pa
            prelevement.save()
            context={
                'enfant':enfant,
                'prelevement':prelevement,
                'view':view
            }
            return redirect('core:prelevement_list', enfant.code_id)
    return render(request,'prelevement_create.html',context)

def analyse_sanguine_create(request,pk):
    view ="Nouvelle analyse"
    enfant = Enfant.objects.get(pk=pk)
    form = AnalyseSanguineForm()
    analyse_sanguine_last = AnalyseSanguine.objects.filter(code_id = enfant).last()
    if analyse_sanguine_last:
        if date_actuelle.month > analyse_sanguine_last.date.month:
            if date_actuelle.day >= analyse_sanguine_last.date.day:
                permis=True
            else:
                permis= False
        else:
            permis=False
    else:
        permis=True
    context ={
        'form':form,
        'enfant':enfant,
        'view':view,
        'analyse_sanguine_last':analyse_sanguine_last,
        'permis':permis,
    }
    if request.method=="POST":
        form = AnalyseSanguineForm(request.POST)
        if form.is_valid():
            analyse_sanguine = form.save(commit=False)
            analyse_sanguine.code_id = enfant
            analyse_sanguine.code_aire = enfant.code_aire
            analyse_sanguine.save()
            context={
                'enfant':enfant,
                'analyse_sanguine':analyse_sanguine,
                'view':view,
            }
            return render(request,'enfant_suite.html',context)
    return render(request,'analyse_sanguine_create.html',context)

def enfant_search(request):
    form= EnfantSearchForm()
    context={
        'form':form
    }
    if request.method=="POST":
        form = EnfantSearchForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['name']
            prenom = form.cleaned_data['prenom']
            postnom = form.cleaned_data['postnom']
            enfants = Enfant.objects.filter(nom=nom, prenom=prenom,postnom=postnom)
            context = {
                'enfants':enfants,
                'form':form,
            }
            return render(request,'enfant_search.html',context)
    return render(request,'enfant_search.html',context)

def prelevement_list(request,pk):
    enfant = Enfant.objects.get(pk=pk)
    prelevements = Prelevement.objects.filter(code_id = enfant)
    context = {
        'prelevements':prelevements,
        'enfant':enfant,
    }
    return render(request,'prelevement_list.html',context)

def prelevement_delete(request,pk,id):
    enfant = Enfant.objects.get(pk=pk)
    prelevement = Prelevement.objects.get(pk=id)
    context={
        'enfant':enfant,
        'prelevement':prelevement,
    }
    if request.method=="POST":
        prelevement.delete()
        return redirect('core:prelevement_list',enfant.code_id)
    return render(request,'prelevement_delete.html',context)

def analyse_sanguine_list(request,pk):
    enfant = Enfant.objects.get(pk=pk)
    analyse_sanguines = AnalyseSanguine.objects.filter(code_id = enfant)
    context = {
        'analyse_sanguines':analyse_sanguines,
        'enfant':enfant,
    }
    return render(request,'analyse_sanguine_list.html',context)   

def analyse_sanguine_delete(request,pk,id):
    enfant = Enfant.objects.get(pk=pk)
    analyse_sanguine = AnalyseSanguine.objects.get(pk=id)
    context={
        'enfant':enfant,
        'analyse_sanguine':analyse_sanguine,
    }
    if request.method=="POST":
        analyse_sanguine.delete()
        return redirect('core:analyse_sanguine_list',enfant.code_id)
    return render(request,'analyse_sanguine_delete.html',context)