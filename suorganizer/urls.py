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
     )

urlpatterns = [
    url(r'^$', redirect_root),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include(blog_urls)),
    url(r'^cestmoilechef/', pronunciamento),
    url(r'^image-porte/', imagePorte),
    url(r'^vignettes/', vignettes),
    url(r'^exporte-posts/', exportePosts),
    url(r'^cree-categories/', creeCategories),
    url(r'^liste-categories/', listeCategories),
    url(r'^cree-photos/', creePhotos),
    url(r'^liste-photos/', listePhotos),
    url(r'^purge-photos/', purgePhotos),
    url(r'^liste-categories2/', listeCategories2),
    url(r'^liste-photos2/', listePhotos2),
    url(r'^categorie-pabon/[\w\-]+/$', categorie_detail_pabon), # Pas recommande mais possible
    url(r'^categorie-pabon2/(?P<slug>[\w\-]+)/$', categorie_detail_pabon2),
    url(r'^categorie/(?P<slug>[\w\-]+)/$',
        categorie_detail,
        name='cestmoilechef_categorie_detail'), # p. 131 et 132 de Pinkham
    url(r'^', include(organizer_urls)),
]
