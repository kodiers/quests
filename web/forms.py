__author__ = 'kodiers'

from django import forms
from django.utils.translation import ugettext_lazy as _

from web.models import Events


class UserRegistrationForm(forms.Form):
    """
    Form for registration new user
    """
    login = forms.CharField(label=_("Nickname"), max_length=128)
    email = forms.EmailField(label=_("Email"), max_length=128)
    password1 = forms.CharField(label=_("Password"), max_length=128, widget=forms.PasswordInput,
                                min_length=8)
    password2 = forms.CharField(label=_("Confirm password"), max_length=128,
                                widget=forms.PasswordInput, min_length=8)
    is_organizer = forms.BooleanField(label=_("Are you organizer?"), required=False)


class RestorePasswordForm(forms.Form):
    """
    Restore password form
    """
    email = forms.EmailField(label="Email", max_length=128)


class CreateTeamForm(forms.Form):
    """
    Create team form
    """
    title = forms.CharField(label=_("Title"), max_length=128)


class PlayerProfileForm(forms.Form):
    """
    Change player profile form
    """
    SEX = (
        ('0', _('MALE')),
        ('1', _('FEMALE')),
        ('2', _('NOT DEFINED'))
    )
    avatar = forms.ImageField(label=_("Avatar"), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label=_("About me"), required=False)
    date_of_birth = forms.DateField(label=_("Date of birth"), required=False)
    sex = forms.ChoiceField(choices=SEX, label=_('Sex'), required=False)
    country = forms.CharField(max_length=255, required=False, label=_("Country"))
    city = forms.CharField(max_length=255, required=False, label=_("City"))
    street = forms.CharField(required=False, label=_("Street"), widget=forms.Textarea(attrs={'rows': 1}))
    phone = forms.CharField(required=False, label=_('Phone number'), max_length=15)
    skype = forms.CharField(max_length=255, label="Skype", required=False)
    site = forms.CharField(label="Web site", required=False)
    email = forms.EmailField(label="Email")
    show_personal_info = forms.BooleanField(label=_("Show my personal info"), required=False)


class CreateEventForm(forms.ModelForm):
    """
    Model Form for create event.
    Add fields to create and edit EventPlaces object and generate map.
    """
    country = forms.CharField(max_length=255, required=False, label=_("Country"))
    city = forms.CharField(max_length=255, required=False, label=_("City"))
    street = forms.CharField(required=False, label=_("Street"), max_length=255)
    class Meta:
        model = Events
        fields = ['title', 'description', 'is_team', 'start_date', 'end_date', 'duration', 'image',
                  'max_players', 'min_players', 'organizer']
        widgets = {'organizer':forms.HiddenInput()}


class OrganizerProfileForm(forms.Form):
    """
    Change organizer profile form
    """
    avatar = forms.ImageField(label=_("Avatar"), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label=_("About me"), required=False)
    date_of_birth = forms.DateField(label=_("Date of birth"), required=False)
    country = forms.CharField(max_length=255, required=False, label=_("Country"))
    city = forms.CharField(max_length=255, required=False, label=_("City"))
    street = forms.CharField(required=False, label=_("Street"), widget=forms.Textarea(attrs={'rows': 1}))
    phone = forms.CharField(required=False, label=_('Phone number'), max_length=15)
    skype = forms.CharField(max_length=255, label="Skype", required=False)
    site = forms.CharField(label="Web site", required=False)
    email = forms.EmailField(label="Email")
