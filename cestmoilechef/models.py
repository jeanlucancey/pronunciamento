from django.db import models
from django.core.urlresolvers import reverse

class Categorie(models.Model):
    nom = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(
        max_length=30,
        unique=True,
        help_text="tout en bdc siouplaît!"
    )

    class Meta:
        ordering = ['nom']

    def get_absolute_url(self):
        return reverse('categorie_detail', kwargs={'slugUrl': self.slug})

    def get_update_url(self):
        return reverse('categorie_update', kwargs={'slugUrl': self.slug})

    def get_delete_url(self):
        return reverse('detruit_une_categorie', kwargs={'slugUrl': self.slug})

    def __str__(self):
        return self.nom

class Photo(models.Model):
    nomComplet = models.CharField(max_length=80)
    nomAbrege = models.CharField(max_length=30)
    categorie = models.ForeignKey(Categorie)

    class Meta:
        ordering = ['nomAbrege']

    def get_absolute_url(self):
        return reverse('montre_photo_precise', kwargs={'nomPhotoUrl': self.nomAbrege})

    def get_update_url(self): # Inspiré, mais très vaguement, de la page 258
        return reverse('photo_update', kwargs={'nomPhotoUrl': self.nomAbrege})

    def get_delete_url(self):
        return reverse('detruit_une_photo', kwargs={'nomPhotoUrl': self.nomAbrege})

    def __str__(self):
        return self.nomAbrege
