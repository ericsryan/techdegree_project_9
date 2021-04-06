import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from . import models


SEASON_CHOICES = [
    ('Spring', 'Spring'),
    ('Summer', 'Summer'),
    ('Fall', 'Fall'),
    ('Winter', 'Winter'),
]

YEAR_CHOICES = [tuple([x,x]) for x in range(
    int(datetime.datetime.now().strftime('%Y')),
    (int(datetime.datetime.now().strftime('%Y'))) + 5)
]


class UserRegisterForm(UserCreationForm):
    """Form to allow users to register"""
    email = forms.EmailField()
    verify_email = forms.EmailField(label="Please verify your email address")
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'verify_email',
            'password1',
            'password2',
        ]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('verify_email')

        if email != verify:
            raise ValidationError(
                "You need to enter the same email address in both fields"
            )


class MenuForm(forms.ModelForm):
    season = forms.CharField(
        label="Choose season:",
        widget=forms.Select(choices=SEASON_CHOICES)
    )
    year = forms.CharField(
        label="Choose year:",
        widget=forms.Select(choices=YEAR_CHOICES)
    )
    items = forms.ModelMultipleChoiceField(
        queryset=models.Item.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = models.Menu
        fields = (
            'season',
            'year',
            'items',
            'expiration_date',
        )

    def clean_expiration_date(self):
        """Validate that the expiration date is later than today"""
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date < datetime.date.today():
            raise ValidationError(
                "The expiration date should be some time later than today."
            )
        return expiration_date
