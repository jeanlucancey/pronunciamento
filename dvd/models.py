from django.db import models
from django.core.urlresolvers import reverse

class Dvd(models.Model):
    titre = models.CharField(max_length=80)
    slug = models.SlugField(
        max_length=31,
        unique=True,
        help_text='Un slug pour les DVD.')
    actClair = models.CharField(max_length=120)
    reaClair = models.CharField(max_length=80)
    genre = models.CharField(max_length=40)
    place = models.CharField(max_length=40)
    obs = models.CharField(max_length=160)

    class Meta:
        ordering = ['titre']

    def get_absolute_url(self):
        return reverse('dvd_detail', kwargs={'slugUrl': self.slug})

    def get_update_url(self):
        return reverse('dvd_update', kwargs={'slugUrl': self.slug})

    def get_delete_url(self):
        return reverse('dvd_delete', kwargs={'slugUrl': self.slug})

    def __str__(self):
        return self.titre
