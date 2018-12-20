from django import forms
from django.core.exceptions import ValidationError

from .models import ElementDialogue

class ElementDialogueForm(forms.ModelForm):
# Le fait d'heriter de ModelForm dispense d'écrire une méthode save(), cf. p. 240
    class Meta:
        model = ElementDialogue
        fields = '__all__'

    def clean_nom(self):
        new_nom = (self.cleaned_data['nom'].lower())
        if new_nom == 'create':
            raise ValidationError('Le nom ne peut pas être "create".')
        return new_nom
