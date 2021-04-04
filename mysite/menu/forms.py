from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _

from . import models


class UserRegisterForm(UserCreationForm):
    """Form to allow users to register"""
    email = forms.EmailField()
    verify_email = forms.EmailField(label="Please verify your email address")
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text="""
        <ul>
            <li>Your password can't be too similar to your other personal information</li>
            <li>Your password can't be a commonly used password</li>
            <li>Your password can't be entirly numeric</li>
            <li>Your password must contain at least 14 characters</li>
            <li>Your password must contain uppercase and lowercase letters</li>
            <li>Your password must contain at least one numeric digit</li>
            <li>Your password must contain at least one special character</li>
        </ul>
        """
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


class MenuForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=models.Item.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = models.Menu
        fields = (
            'season',
            'items',
            'expiration_date'
        )
