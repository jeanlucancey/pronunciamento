from django.conf.urls import url

from .views import (
        accueilDvd,
        DvdList,
        DvdCreate,
        dvdDetail,
        DvdUpdate,
        DvdDelete,
        purgeDvd,
        importeDvd,
        exporteDvd,
)

urlpatterns = [
    url(r'^dvd/$',
            accueilDvd,
                name='dvd_accueil'),
    url(r'^dvd/liste/$',
            DvdList.as_view(),
                name='dvd_liste'),
    url(r'^dvd/create/$',
            DvdCreate.as_view(),
                name='dvd_create'),
    url(r'^dvd/element/(?P<slugUrl>[\w\-]+)/$',
            dvdDetail,
                name='dvd_detail'),
    url(r'^dvd/element-update/(?P<slugUrl>[\w\-]+)/$',
            DvdUpdate.as_view(),
                name='dvd_update'),
    url(r'^dvd/element/(?P<slugUrl>[\w\-]+)/delete/$',
            DvdDelete.as_view(),
                name='dvd_delete'),
    url(r'^dvd/purge-dvd/$',
            purgeDvd,
                name='purge_dvd'),
    url(r'^dvd/importe-dvd/$',
            importeDvd,
                name='importe_dvd'),
    url(r'^dvd/exporte-dvd/$',
            exporteDvd,
                name='exporte_dvd'),
]
