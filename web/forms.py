__author__ = 'kodiers'

from django import forms

from web.models import Events


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


class CreateTeamForm(forms.Form):
    """
    Create team form
    """
    title = forms.CharField(label="Title", max_length=128)


class PlayerProfileForm(forms.Form):
    """
    Change player profile form
    """
    SEX = (
        ('0', 'MALE'),
        ('1', 'FEMALE'),
        ('2', 'NOT DEFINED')
    )
    avatar = forms.ImageField(label="Avatar", required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label="About me", required=False)
    date_of_birth = forms.DateField(label="Date of birth", required=False)
    sex = forms.ChoiceField(choices=SEX, label='Sex', required=False)
    country = forms.CharField(max_length=255, required=False, label="Country")
    city = forms.CharField(max_length=255, required=False, label="City")
    street = forms.CharField(required=False, label="Street", widget=forms.Textarea(attrs={'rows': 1}))
    phone = forms.CharField(required=False, label='Phone number', max_length=15)
    skype = forms.CharField(max_length=255, label="Skype", required=False)
    site = forms.CharField(label="Web site", required=False)
    email = forms.EmailField(label="Email")
    show_personal_info = forms.BooleanField(label="Show my personal info", required=False)


class CreateEventForm(forms.ModelForm):
    """
    Model Form for create event.
    """
    class Meta:
        model = Events
        fields = ['title', 'description', 'map_link', 'is_team', 'start_date', 'end_date', 'duration', 'image',
                  'organizer']
        widgets = {'organizer':forms.HiddenInput()}


class OrganizerProfileForm(forms.Form):
    """
    Change organizer profile form
    """
    avatar = forms.ImageField(label="Avatar", required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label="About me", required=False)
    date_of_birth = forms.DateField(label="Date of birth", required=False)
    country = forms.CharField(max_length=255, required=False, label="Country")
    city = forms.CharField(max_length=255, required=False, label="City")
    street = forms.CharField(required=False, label="Street", widget=forms.Textarea(attrs={'rows': 1}))
    phone = forms.CharField(required=False, label='Phone number', max_length=15)
    skype = forms.CharField(max_length=255, label="Skype", required=False)
    site = forms.CharField(label="Web site", required=False)
    email = forms.EmailField(label="Email")
