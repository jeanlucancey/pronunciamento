from django import forms
from django.core.exceptions import ValidationError

from .models import Dvd

class DvdForm(forms.ModelForm):
# Le fait d'heriter de ModelForm dispense d'écrire une méthode save(), cf. p. 240
    class Meta:
        model = Dvd
        fields = '__all__'

    def clean_slug(self):
        new_slug = (self.cleaned_data['slug'].lower())
        if new_slug == 'create':
            raise ValidationError('Le slug ne peut pas être "create".')
        return new_slug
