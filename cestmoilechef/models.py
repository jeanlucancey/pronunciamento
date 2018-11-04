from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(
        max_length=30,
        unique=True,
        help_text="ben... c'est une categorie, quoi !"
    )

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Photo(models.Model):
    nomComplet = models.CharField(max_length=80)
    nomAbrege = models.CharField(max_length=30)
    categorie = models.ForeignKey(Categorie)

    class Meta:
        ordering = ['nomComplet']

    def __str__(self):
        return self.nomAbrege
