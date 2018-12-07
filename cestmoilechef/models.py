from django.db import models
from django.core.urlresolvers import reverse

class Categorie(models.Model):
    nom = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(
        max_length=30,
        unique=True,
        help_text="ben... c'est une categorie, quoi !"
    )

    class Meta:
        ordering = ['nom']

    def get_absolute_url(self):
        return reverse('cestmoilechef_categorie_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.nom

class Photo(models.Model):
    nomComplet = models.CharField(max_length=80)
    nomAbrege = models.CharField(max_length=30)
    categorie = models.ForeignKey(Categorie)

    class Meta:
        ordering = ['nomAbrege']

    def get_absolute_url(self):
        return reverse('montre_photo_precise', kwargs={'nomPhoto': self.nomAbrege})

    def __str__(self):
        return self.nomAbrege
