from django.db import models
from django.core.urlresolvers import reverse

class ElementDialogue(models.Model):
    nom = models.CharField(max_length=30, unique=True)
    param1 = models.CharField(max_length=80)
    param2 = models.CharField(max_length=80)
    param3 = models.CharField(max_length=80)

    class Meta:
        ordering = ['nom']

    def get_absolute_url(self):
        return reverse('dialogue_detail', kwargs={'nomUrl': self.nom})

    def get_update_url(self):
        return reverse('dialogue_update', kwargs={'nomUrl': self.nom})

    def get_delete_url(self):
        return reverse('dialogue_delete', kwargs={'nomUrl': self.nom})

    def __str__(self):
        return self.nom
