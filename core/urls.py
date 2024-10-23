from django.urls import path
from .views import *

app_name ='core'

urlpatterns = [
    path('login/',login_page,name='login'),
    path("logout/",logout_page, name="logout"),
    path('index/',index,name='index'),
    path("index/stat/province", stat_province, name="stat_province"),
    path("index/stat/zone", stat_zone, name="stat_zone"),
    path("index/stat/aire", stat_aire, name="stat_aire"),
    path('index/province/list/',province_list,name='province_list'),
    path("index/provine/add/",province_create, name="province_create"),
    path("index/province/<int:pk>/update/", province_update, name="province_update"),
    path('index/zone-sanitaire/list/',zone_sanitaire_list,name='zone_sanitaire_list'),
    path("index/zone-sanitaire/add/", zone_sanitaire_create, name="zone_sanitaire_create"),
    path("index/zone-sanitaire/<int:pk>/update/", zone_sanitaire_update, name="zone_sanitaire_update"),
    path('index/aire-sanitaire/list/',aire_sanitaire_list,name='aire_sanitaire_list'),
    path("index/aire-sanitaire/add/", aire_sanitaire_create, name="aire_sanitaire_create"),
    path("index/aire-sanitaire/<int:pk>/update", aire_sanitaire_update, name="aire_sanitaire_update"),
    path("index/Enfant/add/", enfant_create, name="enfant_create"),
    path("index/Enfant/<int:pk>/Etat-initial/add/",etat_initial_create, name="etat_initial_create"),
    path("index/Enfant/<int:pk>/analyse-sanguine/add/",analyse_sanguine_create, name="analyse_sanguine_create"),
    path("index/Enfant/search/",enfant_search, name="enfant_search"),
    path("index/Enfant/<int:pk>/prelevement/list/",prelevement_list, name="prelevement_list"),
    path("index/Enfant/<int:pk>/prelevement/add/",prelevement_create, name="prelevement_create"),
    path("index/Enfant/<int:pk>/prelevement/<int:id>/delete/",prelevement_delete, name="prelevement_delete"),
    path("index/Enfant/<int:pk>/analyse-sanguine/list/",analyse_sanguine_list, name="analyse_sanguine_list"),
    path("index/Enfant/<int:pk>/analyse-sanguine/<int:id>/delete/",analyse_sanguine_delete, name="analyse_sanguine_delete"),
]

