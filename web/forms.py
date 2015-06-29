__author__ = 'kodiers'

from django import forms

class UserRegistrationForm(forms.Form):
    """
    Form for registration new user
    """
    login = forms.CharField(label="Nickname", max_length=128)
    email = forms.EmailField(label="Email", max_length=128)
    password1 = forms.CharField(label="Password", max_length=128, widget=forms.PasswordInput,
                                min_length=8)
    password2 = forms.CharField(label="Confirm password", max_length=128,
                                widget=forms.PasswordInput, min_length=8)
    is_organizer = forms.BooleanField(label="Are you organizer?", required=False)


class RestorePasswordForm(forms.Form):
    """
    Restore password form
    """
    email = forms.EmailField(label="Email", max_length=128)
