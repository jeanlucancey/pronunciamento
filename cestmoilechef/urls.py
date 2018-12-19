from django.conf.urls import url

from .views import (
        pronunciamento,
        listeCategories,
        # listeCategories2, # Ligne neutralisee because shortcut
        # listeCategories4, # Ligne neutralisee because remplacement par une class-based view
        # categorie_list, # Remplacé par la class-based view CategorieList
        CategorieList,
        # categorie_create, # remplacé par la class-based view categorie_create
        CategorieCreate,
        categorie_detail_pabon,
        categorie_detail_pabon2,
        categorie_detail,
        # categorie_detail_shortcut, # Neutralise because shortcut once more...
        categorie_detail_shortcut2,
        CategorieUpdate,
        CategorieDelete,
        importeCategories,
        exporteCategories,
        purgeCategories,
        listePhotos,
        # listePhotos2, # Ligne neutralisee because shortcut
        # listePhotos3, # Ligne neutralisee because autre shortcut !
        # listePhotos4, # Remplacée par la class-based view PhotoList
        PhotoList,
        PhotoCreate,
        montrePhotoPrecise,
        PhotoUpdate,
        PhotoDelete,
        purgePhotos,
        importePhotos,
        exportePhotos,
        echoPath,
        lsLong,
        multiplication,
        imagePorte,
        vignettes,
        exportePosts,
)

urlpatterns = [
    url(r'^cestmoilechef/$', pronunciamento, name='pro_nun_cia_men_to'),
    url(r'^cestmoilechef/liste-categories/$', listeCategories, name='liste_cate_gories'),
    # url(r'^liste-categories2/', listeCategories3, name='liste_cate_gories_2'),
    # url(r'^cestmoilechef/liste-categories2/$', listeCategories4, name='liste_cate_gories_2'),
    url(r'^cestmoilechef/liste-categories2/$', CategorieList.as_view(), name='liste_cate_gories_2'),
    # L'URL qui suit (categorie/create) doit impérativement venir avant categorie/<slug>,
    # sans quoi "create" sera considéré comme un slug banal
    url(r'^cestmoilechef/categorie/create/$',
        # categorie_create, # remplacé par une class-based view
        CategorieCreate.as_view(),
        name='cestmoilechef_categorie_create'),
    url(r'^cestmoilechef/categorie-pabon/[\w\-]+/$', categorie_detail_pabon, name='pabon'), # Pas recommande mais possible
    url(r'^cestmoilechef/categorie-pabon2/(?P<slugUrl>[\w\-]+)/$', categorie_detail_pabon2, name='pabon2'),
    url(r'^cestmoilechef/categorie/(?P<slugUrl>[\w\-]+)/$', categorie_detail, name='cestmoilechef_categorie_detail'), # p. 131 et 132 de Pinkham
    url(r'^cestmoilechef/categorie-shortcut/(?P<slugUrl>[\w\-]+)/$', categorie_detail_shortcut2, name='cestmoilechef/cestmoilechef_categorie_detail_shorcut'), # p. 137, puis 139 de Pinkham
    url(r'^cestmoilechef/categorie-update/(?P<slugUrl>[\w\-]+)/$', CategorieUpdate.as_view(), name='categorie_update'),
    url(r'^cestmoilechef/categorie/(?P<slugUrl>[\w\-]+)/delete/$', CategorieDelete.as_view(), name='detruit_une_categorie'),
    url(r'^cestmoilechef/importe-categories/$', importeCategories, name='importe_cate_go_ries'),
    url(r'^cestmoilechef/exporte-categories/$', exporteCategories, name='exporte_categories'),
    url(r'^cestmoilechef/purge-categories/$', purgeCategories, name='purge_categories'),
    url(r'^cestmoilechef/liste-photos/$', listePhotos, name='liste_pho_tos'),
    # url(r'^cestmoilechef/liste-photos2/$', listePhotos2, name='liste_pho_tos_2'),
    # url(r'^cestmoilechef/liste-photos2/$', listePhotos4, name='liste_pho_tos_2'),
    url(r'^cestmoilechef/liste-photos2/$', PhotoList.as_view(), name='liste_pho_tos_2'),
    url(r'^cestmoilechef/photo/create/$', PhotoCreate.as_view(), name='cestmoilechef_photo_create'),
    url(r'^cestmoilechef/photo-precise/(?P<nomPhotoUrl>[\w\-]+)/$', montrePhotoPrecise, name='montre_photo_precise'),
    url(r'^cestmoilechef/photo-update/(?P<nomPhotoUrl>[\w\-]+)/$', # Nota 2018/12/12: pas de flexe en haut de la p. 258. Why?
        PhotoUpdate.as_view(),
        name='photo_update'),
    url(r'^cestmoilechef/photo-precise/(?P<nomPhotoUrl>[\w\-]+)/delete/$', PhotoDelete.as_view(), name='detruit_une_photo'),
    url(r'^cestmoilechef/purge-photos/$', purgePhotos, name='purge_pho_tos'),
    url(r'^cestmoilechef/importe-photos/$', importePhotos, name='importe_pho_tos'),
    url(r'^cestmoilechef/exporte-photos/$', exportePhotos, name='exporte_photos'),
    url(r'^cestmoilechef/path/$', echoPath, name='cestmoilechef_path'),
    url(r'^cestmoilechef/ls-long/$', lsLong, name='cestmoilechef_lslong'),
    url(r'^cestmoilechef/multiplication/$', multiplication, name='cestmoilechef_multiplication'),
    url(r'^cestmoilechef/image-porte/$', imagePorte, name='ima_geport_te'),
    url(r'^cestmoilechef/vignettes/$', vignettes, name='vig_net_tes'),
    url(r'^cestmoilechef/exporte-posts/$', exportePosts, name='exp_ort_eposts'),
]
