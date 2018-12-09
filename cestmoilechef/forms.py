from django import forms
from django.core.exceptions import ValidationError
from .models import Categorie

class CategorieForm(forms.Form):
    nomDsForm = forms.CharField(max_length=30)
    slugDsForm = forms.SlugField(
                     max_length=30,
                     help_text='Une étiquette pour CategorieForm'
                 )

    def clean_nom(self):
    # S'assure que le nom est en bdc because ordre alpha informatique
        return self.cleaned_data['nomDsForm'].lower()

    def clean_slug(self):
        new_slug = (self.cleaned_data[slugDsForm].lower())
        if new_slug == 'create':
            raise ValidationError('Slug may not be "create".')
        return new_slug

    def save(self):
        new_categorie = Categorie.objects.create(
                            nom = self.cleaned_data['nomDsForm'],
                            slug = self.cleaned_data['slugDsForm']
                        )
        return new_categorie
