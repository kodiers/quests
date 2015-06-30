import datetime

from django.shortcuts import render, render_to_response, redirect, get_list_or_404, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.utils.translation import ugettext as _

from django.core.mail import send_mail

from web.models import QuestsUsers, Players, Organizers, Contacts, Events
from web.forms import UserRegistrationForm, RestorePasswordForm

from quests.settings import EMAIL_HOST_USER

from web.functions import create_password_str


# Create your views here.

def index(request):
    """
    Return index page. With events, players and organizers.
    :param request: HttpRequest
    :return: HttpResponse
    """
    today = datetime.date.today()
    nearest_events = Events.objects.filter(start_date__gte=today).order_by('start_date')[:3]
    best_players = Players.objects.filter(points__gt=0).order_by('-points')[:3]
    #TODO: get best organizers
    return render_to_response('index.html', {'nearest_events': nearest_events,
                                             'best_players': best_players},
                              context_instance=RequestContext(request))


def registration(request):
    """
    Register new user
    :param request: HttpRequest
    :return: HttpResponse
    """
    if request.user.is_authenticated():
        message = _("You are already registered!")
        return render_to_response('register_success.html', {'message': message},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create new user
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    new_user = User.objects.create_user(form.cleaned_data['login'],
                                                        form.cleaned_data['email'],
                                                        form.cleaned_data['password1'])
                    new_user.save()
                    email_subject = "Registration complete!"
                    email_message = """Hello! You was registered on site OUR_SITE. \n
                    Your login {login} \n Your password {password} \n Your email {email} \n
                    Thank you!""".format(login=form.cleaned_data['login'],
                                         password=form.cleaned_data['password1'],
                                         email=form.cleaned_data['email'])
                    recipients = [new_user.email]
                    try:
                        send_mail(email_subject, email_message, EMAIL_HOST_USER, recipients)
                    except:
                        error = _("Error sending confirmation email")
                except:
                    error = _("Error creating new user")
                if 'is_organizer' in request.POST:
                    new_organizer = QuestsUsers()
                    new_organizer.user = new_user
                    new_organizer.is_organizer = True
                    new_organizer.save()
                    orgzr = Organizers()
                    orgzr.user = new_user
                    orgzr.save()
                else:
                    new_player = QuestsUsers()
                    new_player.user = new_user
                    new_player.save()
                    player = Players()
                    player.user = new_user
                    player.save()
                auth_user = authenticate(username=new_user.username,
                                     password=form.cleaned_data['password1'])
                login(request, auth_user)
                message = _("You was succesfully registered!")
                return render_to_response('register_success.html', {'message': message},
                                      context_instance=RequestContext(request))
            else:
                error = _("Password and confirm password doesn't match")
        else:
            error = _("Error in forms fields. Try again!")
    else:
        error = ""
    form = UserRegistrationForm()
    return render_to_response('register.html', {'form': form, 'error': error},
                                  context_instance=RequestContext(request))


def restore_password(request):
    """
    Restore password view
    :param request:
    :return:
    """
    success = False
    if request.method == 'POST':
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            restore_email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=restore_email)
                password = create_password_str()
                user.set_password(password)
                user.save()
                email_subject = "Your password restored"
                email_message = """Hello! \n Your new password to our site is {password} \n
                                Thank you!""".format(password=password)
                recipients = [user.email]
                try:
                    send_mail(email_subject, email_message, EMAIL_HOST_USER, recipients)
                except:
                    error = _("Error send email!")
                error = _("Your password sent to your email")
                success = True
            except ObjectDoesNotExist:
                error = _("User with this email not found")
        else:
            error = _("Error in forms fields. Try again!")
    else:
        error = ""
    form = RestorePasswordForm()
    return render_to_response('restore_password.html', {'form': form, 'error': error,
                                                        'success': success},
                              context_instance=RequestContext(request))


@login_required()
def show_player_profile(request):
    """

    :param request:
    :return:
    """
    pass
