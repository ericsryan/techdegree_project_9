from django import forms

from . import models

class MenuForm(forms.ModelForm):

    class Meta:
        model = models.Menu
        fields = (
            'season',
            'items',
            'expiration_date'
        )
