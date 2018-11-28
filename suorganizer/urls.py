"""suorganizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from blog import urls as blog_urls
from organizer import urls as organizer_urls

from .views import redirect_root
from cestmoilechef.views import (
        pronunciamento, \
        imagePorte, \
        vignettes, \
        exportePosts, \
        creeCategories, \
        listeCategories, \
        creePhotos, \
        listePhotos, \
        purgePhotos, \
        listeCategories2, \
        listePhotos2, \
        categorie_detail_pabon, \
        categorie_detail_pabon2, \
        categorie_detail, \
        categorie_detail_shortcut, \
        montrePhotoPrecise, \
     )

urlpatterns = [
    url(r'^$', redirect_root),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include(blog_urls)),
    url(r'^cestmoilechef/',
        pronunciamento,
        name='pro_nun_cia_men_to'),
    url(r'^image-porte/', imagePorte, name='ima_geport_te'),
    url(r'^vignettes/', vignettes, name='vig_net_tes'),
    url(r'^exporte-posts/', exportePosts, name='exp_ort_eposts'),
    url(r'^cree-categories/', creeCategories, name='cree_cate_go_ries'),
    url(r'^liste-categories/', listeCategories, name='liste_cate_gories'),
    url(r'^cree-photos/', creePhotos, name='cree_pho_tos'),
    url(r'^liste-photos/', listePhotos, name='liste_pho_tos'),
    url(r'^purge-photos/', purgePhotos, name='purge_pho_tos'),
    url(r'^liste-categories2/', listeCategories2, name='liste_cate_gories_2'),
    url(r'^liste-photos2/', listePhotos2, name='liste_pho_tos_2'),
    url(r'^categorie-pabon/[\w\-]+/$', categorie_detail_pabon, name='pabon'), # Pas recommande mais possible
    url(r'^categorie-pabon2/(?P<slug>[\w\-]+)/$', categorie_detail_pabon2, name='pabon2'),
    url(r'^categorie/(?P<slug>[\w\-]+)/$',
        categorie_detail,
        name='cestmoilechef_categorie_detail'), # p. 131 et 132 de Pinkham
    url(r'^categorie-shortcut/(?P<slug>[\w\-]+)/$',
        categorie_detail_shortcut,
        name='cestmoilechef_categorie_detail_shorcut'), # p. 137 de Pinkham
    url(r'^photo-precise/(?P<nomPhoto>[\w\-]+)/$',
        montrePhotoPrecise,
        name='montre_photo_precise'),
    url(r'^', include(organizer_urls)),
]
