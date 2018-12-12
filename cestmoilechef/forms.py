from django import forms
from django.core.exceptions import ValidationError

from .models import Categorie, Photo

class CategorieForm(forms.ModelForm):
# Le fait d'heriter de ModelForm dispense d'écrire une méthode save(), cf. p. 240
    class Meta:
        model = Categorie
        fields = '__all__'

    def clean_nom(self):
    # S'assure que le nom est en bdc because ordre alpha informatique
        return self.cleaned_data['nom'].lower()

    def clean_slug(self):
        new_slug = (self.cleaned_data['slug'].lower())
        if new_slug == 'create':
            raise ValidationError('Slug may not be "create".')
        return new_slug

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'

    def clean_nom(self):
    # S'assure que le nom est en bdc because ordre alpha informatique
        return self.cleaned_data['nomAbrege'].lower()
    
