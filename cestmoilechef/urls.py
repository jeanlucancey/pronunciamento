from django.conf.urls import url

# L'ordre suivi dans ce listing, tant pour les imports que pour les
# urlpatterns, est celui du template pronunciamento.html, c'est-à-dire
# L-CRUD-PIE (list, create, read, update, purge, import, export), avec
# les merdasses sans rapport direct avec le projet à la toute fin.
# Je recommande de ne pas effacer les lignes neutralisées, car elles
# correspondent à des bouts de listings qui seraient susceptibles de
# servir comme modèles s'il était nécessaire d'y intercaler des lignes,
# ce qui n'est souvent pas possible avec les syntaxes abrégées et pleines
# de shortcuts préconisées par Pinkham.

from .views import (
        pronunciamento,
        listeCategories,
        # listeCategories2, # Ligne neutralisee because shortcut
        # listeCategories4, # Ligne neutralisee because remplacement par la class-based view CategorieList
        CategorieList,
        # categorieCreate, # remplacé par la class-based view CategorieCreate
        CategorieCreate,
        categorieDetailPabon,
        categorieDetailPabon2,
        categorieDetail,
        # categorieDetailShortcut, # Neutralise because shortcut once more...
        categorieDetailShortcut2,
        CategorieUpdate,
        CategorieDelete,
        purgeCategories,
        importeCategories,
        exporteCategories,
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

# Voir plus haut pour l'ordre d'appel de toutes ces choses et la nécessité
# de conserver les lignes neutralisées. Le mode d'indentation n'est pas celui
# que j'utilise ordinairement, mais il est bien utile pour s'assurer de la
# cohérence des syntaxes: traits d'union dans les URL, camelCase pour les
# fonctions et les class-based views, snake_case pour les noms à reprendre
# dans les templates, ma hantise étant de ne pas avoir des syntaxes différentes
# dans ces trois cas si différents.
urlpatterns = [
    url(r'^cestmoilechef/$',
            pronunciamento,
                name='cestmoilechef_pronunciamento'),
    url(r'^cestmoilechef/liste-categories-moche/$',
            listeCategories,
                name='liste_categories_moche'),
    # url(r'^liste-categories2/',
    #        listeCategories3,
    #            name='liste_cate_gories_2'),
    # url(r'^cestmoilechef/liste-categories2/$',
    #         listeCategories4,
    #             name='liste_cate_gories_2'),
    url(r'^cestmoilechef/liste-categories/$',
            CategorieList.as_view(),
                name='liste_categories'),
    # L'URL qui suit (categorie/create) doit impérativement venir avant categorie/<slug>,
    # sans quoi "create" sera considéré comme un slug banal
    url(r'^cestmoilechef/categorie/create/$',
            # categorie_create, # remplacé par une class-based view
            CategorieCreate.as_view(),
                name='categorie_create'),
    url(r'^cestmoilechef/categorie-pabon/[\w\-]+/$',
            categorieDetailPabon,
                name='pabon'), # Pas recommande mais possible
    url(r'^cestmoilechef/categorie-pabon2/(?P<slugUrl>[\w\-]+)/$',
            categorieDetailPabon2,
                name='pabon2'),
    url(r'^cestmoilechef/categorie/(?P<slugUrl>[\w\-]+)/$',
            categorieDetail,
                name='categorie_detail'), # p. 131 et 132 de Pinkham
    url(r'^cestmoilechef/categorie-shortcut/(?P<slugUrl>[\w\-]+)/$',
            categorieDetailShortcut2,
                name='categorie_detail_shorcut'), # p. 137, puis 139 de Pinkham
    url(r'^cestmoilechef/categorie-update/(?P<slugUrl>[\w\-]+)/$',
            CategorieUpdate.as_view(),
                name='categorie_update'),
    url(r'^cestmoilechef/categorie/(?P<slugUrl>[\w\-]+)/delete/$',
            CategorieDelete.as_view(),
                name='detruit_une_categorie'),
    url(r'^cestmoilechef/importe-categories/$',
            importeCategories,
                name='importe_categories'),
    url(r'^cestmoilechef/exporte-categories/$',
            exporteCategories,
                name='exporte_categories'),
    url(r'^cestmoilechef/purge-categories/$',
            purgeCategories,
                name='purge_categories'),
    url(r'^cestmoilechef/liste-photos-moche/$',
            listePhotos,
                name='liste_photos_moche'),
    # url(r'^cestmoilechef/liste-photos2/$',
    #         listePhotos2,
    #             name='liste_photos_2'),
    # url(r'^cestmoilechef/liste-photos2/$',
    #         listePhotos4,
    #             name='liste_photos_2'),
    url(r'^cestmoilechef/liste-photos/$',
            PhotoList.as_view(),
                name='liste_photos'),
    url(r'^cestmoilechef/photo/create/$',
            PhotoCreate.as_view(),
                name='photo_create'),
    url(r'^cestmoilechef/photo-precise/(?P<nomPhotoUrl>[\w\-]+)/$',
            montrePhotoPrecise,
                name='montre_photo_precise'),
    url(r'^cestmoilechef/photo-update/(?P<nomPhotoUrl>[\w\-]+)/$', # Nota 2018/12/12: pas de flexe en haut de la p. 258. Why?
            PhotoUpdate.as_view(),
                name='photo_update'),
    url(r'^cestmoilechef/photo-precise/(?P<nomPhotoUrl>[\w\-]+)/delete/$',
            PhotoDelete.as_view(),
                name='detruit_une_photo'),
    url(r'^cestmoilechef/purge-photos/$',
            purgePhotos,
                name='purge_photos'),
    url(r'^cestmoilechef/importe-photos/$',
            importePhotos,
                name='importe_photos'),
    url(r'^cestmoilechef/exporte-photos/$',
            exportePhotos,
                name='exporte_photos'),
    url(r'^cestmoilechef/path/$',
            echoPath,
                name='cestmoilechef_path'),
    url(r'^cestmoilechef/ls-long/$',
            lsLong,
                name='cestmoilechef_lslong'),
    url(r'^cestmoilechef/multiplication/$',
            multiplication,
                name='cestmoilechef_multiplication'),
    url(r'^cestmoilechef/image-porte/$',
            imagePorte,
                name='image_porte'),
    url(r'^cestmoilechef/vignettes/$',
            vignettes,
                name='cestmoilechef_vignettes'),
    url(r'^cestmoilechef/exporte-posts/$',
            exportePosts,
                name='exporte_posts'),
]
