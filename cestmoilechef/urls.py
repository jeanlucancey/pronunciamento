from django.conf.urls import url

from .views import (
        pronunciamento, \
        imagePorte, \
        vignettes, \
        exportePosts, \
        creeCategories, \
        listeCategories, \
        creePhotos, \
        listePhotos, \
        purgePhotos, \
        # listeCategories2, \ # Ligne neutralisee because shortcut
        listeCategories4, \
        # listePhotos2, \ # Ligne neutralisee because shortcut
        # listePhotos3, \ # Ligne neutralisee because autre shortcut !
        listePhotos4, \
        categorie_detail_pabon, \
        categorie_detail_pabon2, \
        categorie_detail, \
        # categorie_detail_shortcut, \ # Neutralise because shortcut once more...
        categorie_detail_shortcut2, \
        montrePhotoPrecise, \
)

urlpatterns = [
    url(r'^cestmoilechef/$',
        pronunciamento,
        name='pro_nun_cia_men_to'),
    url(r'^cestmoilechef/image-porte/$', imagePorte, name='ima_geport_te'),
    url(r'^cestmoilechef/vignettes/$', vignettes, name='vig_net_tes'),
    url(r'^cestmoilechef/exporte-posts/$', exportePosts, name='exp_ort_eposts'),
    url(r'^cestmoilechef/cree-categories/$', creeCategories, name='cree_cate_go_ries'),
    url(r'^cestmoilechef/liste-categories/$', listeCategories, name='liste_cate_gories'),
    url(r'^cestmoilechef/cree-photos/$', creePhotos, name='cree_pho_tos'),
    url(r'^cestmoilechef/liste-photos/$', listePhotos, name='liste_pho_tos'),
    url(r'^cestmoilechef/purge-photos/$', purgePhotos, name='purge_pho_tos'),
    # url(r'^liste-categories2/', listeCategories3, name='liste_cate_gories_2'),
    # La ligne precedente a été remplacée par la suivante, because shortcuts
    url(r'^cestmoilechef/liste-categories2/$', listeCategories4, name='liste_cate_gories_2'),
    # url(r'^liste-photos2/', listePhotos2, name='liste_pho_tos_2'),
    # La ligne precedente a été remplacée par la suivante, because shortcuts
    url(r'^cestmoilechef/liste-photos2/$', listePhotos4, name='liste_pho_tos_2'),
    url(r'^cestmoilechef/categorie-pabon/[\w\-]+/$', categorie_detail_pabon, name='pabon'), # Pas recommande mais possible
    url(r'^cestmoilechef/categorie-pabon2/(?P<slug>[\w\-]+)/$', categorie_detail_pabon2, name='pabon2'),
    url(r'^cestmoilechef/categorie/(?P<slug>[\w\-]+)/$',
        categorie_detail,
        name='cestmoilechef_categorie_detail'), # p. 131 et 132 de Pinkham
    url(r'^cestmoilechef/categorie-shortcut/(?P<slug>[\w\-]+)/$',
        categorie_detail_shortcut2,
        name='cestmoilechef/cestmoilechef_categorie_detail_shorcut'), # p. 137, puis 139 de Pinkham
    url(r'^cestmoilechef/photo-precise/(?P<nomPhoto>[\w\-]+)/$',
        montrePhotoPrecise,
        name='montre_photo_precise'),
]
