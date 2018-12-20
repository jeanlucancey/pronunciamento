from django.conf.urls import url

from .views import (
        accueilDialogue,
        DialogueList,
        ElementDialogueCreate,
        elementDialogueDetail,
        ElementDialogueUpdate,
        ElementDialogueDelete,
)

urlpatterns = [
    url(r'^dialogue/$',
            accueilDialogue,
                name='dialogue_accueil'),
    url(r'^dialogue/liste/$',
            DialogueList.as_view(),
                name='dialogue_liste'),
    url(r'^dialogue/element/create/$',
            ElementDialogueCreate.as_view(),
                name='dialogue_element_create'),
    url(r'^dialogue/element/(?P<nomUrl>[\w\-]+)/$',
            elementDialogueDetail,
                name='dialogue_detail'),
    url(r'^dialogue/element-update/(?P<nomUrl>[\w\-]+)/$',
            ElementDialogueUpdate.as_view(),
                name='dialogue_update'),
    url(r'^dialogue/element/(?P<nomUrl>[\w\-]+)/delete/$',
            ElementDialogueDelete.as_view(),
                name='dialogue_delete'),
]
