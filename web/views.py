import datetime

from django.http import Http404

from django.shortcuts import render, render_to_response, redirect, get_list_or_404, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import ListView, DetailView

from django.utils.translation import ugettext as _

from django.core.mail import send_mail

from web.models import QuestsUsers, Players, Organizers, Contacts, Events, Teams
from web.forms import UserRegistrationForm, RestorePasswordForm, CreateTeamForm

from quests.settings import EMAIL_HOST_USER

from web.functions import create_password_str

FORM_FIELDS_ERROR = _("Error in forms fields. Try again!")
REQUEST_PARAMETRS_ERROR = _('Incorrect request parameters!')
REQUEST_TYPE_ERROR = _('Incorrect request!')

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
    best_organizers = Organizers.objects.filter(show_on_main_page=True)[:3]
    return render_to_response('index.html', {'nearest_events': nearest_events,
                                             'best_players': best_players,
                                             'best_organizers': best_organizers},
                              context_instance=RequestContext(request))


def registration(request):
    """
    Register new user. Create user, organizer or players objects in database. Send confirmation email.
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
                auth_user = authenticate(username=new_user.username,
                                     password=form.cleaned_data['password1'])
                login(request, auth_user)
                message = _("You was succesfully registered!")
                return render_to_response('register_success.html', {'message': message}, context_instance=RequestContext(request))
            else:
                error = _("Password and confirm password doesn't match")
        else:
            error = FORM_FIELDS_ERROR
    else:
        error = ""
    form = UserRegistrationForm()
    return render_to_response('register.html', {'form': form, 'error': error}, context_instance=RequestContext(request))


def restore_password(request):
    """
    Restore password view. Send restored password to email.
    :param request: HttpRequest
    :return: HttpResponse
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
            error = FORM_FIELDS_ERROR
    else:
        error = ""
    form = RestorePasswordForm()
    return render_to_response('restore_password.html', {'form': form, 'error': error,
                                                        'success': success},
                              context_instance=RequestContext(request))


def login_view(request):
    """
    Login view. If login successful redirect to index page or to 'next' parameter in GET request.
    :param request: HttpRequest
    :return: HttpResponse
    """
    # TODO: complete debugging
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(request.POST.get('next', '/'))
                else:
                    error = _("User is not active!")
            else:
                error = _("Incorrect username or password!")
        else:
            error = FORM_FIELDS_ERROR
    error = ""
    next_url = '/'
    if 'next' in request.GET:
        if request.GET['next'] != '':
            next_url = request.GET['next']
    form = AuthenticationForm()
    return render_to_response('login.html', {'form': form, 'error': error, 'next_url': next_url},
                              context_instance=RequestContext(request))


def logout_view(request):
    """
    Logout view (handler). After logout redirect to index page.
    :param request: HttpRequest
    :return: HttpResponse
    """
    logout(request)
    return redirect('/')


class EventView(DetailView):
    """
    Show events detail
    """
    model = Events
    template_name = 'event.html'


@login_required()
def confirm_join_event(request, pk):
    """
    Show register join event confirmation page. On page user can choise team or register as player
    (depends on event type (team or not)). User should be logged in.
    :param request: HttpRequest object
    :param pk: pk of event
    :return: HttpResponse object
    """
    event = get_object_or_404(Events, pk=pk)
    user_registered = False
    for team in event.registered_teams.all():
        if request.user in team.players.all():
            user_registered = True
    if request.user in event.registered_players.all():
        user_registered = True
    return render_to_response('confirm_join_event.html', {'object': event, 'user_registered': user_registered},
                              context_instance=RequestContext(request))


@login_required()
def join_event(request, flag):
    """

    :param request:
    :param flag:
    :return:
    """
    event = None
    error = ''
    if request.method == 'POST':
        if 'event_pk' in request.POST:
            event = get_object_or_404(Events, pk=request.POST['event_pk'])
            if flag == 'player':
                event.registered_players.add(request.user)
                error = _('You was successfully registered to event!')
            elif flag == 'team':
                try:
                    team = Teams.objects.get(creator=request.user)
                    if team in event.registered_teams.all():
                        error = _('Your team are already registered in this event!')
                    else:
                        event.registered_teams.add(team)
                        error = _('You team was registered to event %s' % event.title)
                except ObjectDoesNotExist:
                    pass
            else:
                error = REQUEST_PARAMETRS_ERROR
        else:
            error = REQUEST_PARAMETRS_ERROR
    else:
        error = REQUEST_TYPE_ERROR
    return render_to_response('join_event.html', {'object': event, 'error': error},
                              context_instance=RequestContext(request))


@login_required()
def create_team(request, event_pk=None):
    """
    Create team. If successfull redirect to index page by JavaScript code.
    Optionaly can register team to event (if event_pk !=none).
    :param request: HttpRequest
    :param event_pk: pk of event
    :return: HttpResponse
    """
    if event_pk is not None:
        event = get_object_or_404(Events, pk=event_pk)
    else:
        event = ''
    success = False
    error = None
    teams = Teams.objects.all()
    for tm in teams:
        if request.user == tm.creator:
            error = _('You are creator of team %s' % tm.title)
            success = True
            break
    if request.method == 'POST':
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            try:
                team = Teams()
                team.title = form.cleaned_data['title']
                team.creator = request.user
                team.save()
                team.players.add(request.user)
                success = True
            except:
                error = _('Error create team!')
            if 'event_pk' in request.POST:
                event = get_object_or_404(Events, pk=request.POST['event_pk'])
                if team is not None:
                    event.registered_teams.add(team)
                    success = True
        else:
            error = FORM_FIELDS_ERROR
    form = CreateTeamForm()
    return render_to_response('create_team.html', {'form': form, 'event': event, 'error': error, 'success': success},
                              context_instance=RequestContext(request))


@login_required()
def join_team(request):
    """
    Add user to team.players field. Wait for post request to do this.
    :param request: HttpRequest
    :return: HttpResponse
    """
    error = ''
    if request.method == 'POST':
        if 'team_pk' in request.POST:
            team = get_object_or_404(Teams, pk=request.POST['team_pk'])
            team.players.add(request.user)
            error = _('You successfully joined team %s' % team.title)
        else:
            error = REQUEST_PARAMETRS_ERROR
    else:
        error = REQUEST_TYPE_ERROR
    return render_to_response('join_event.html', {'error': error}, context_instance=RequestContext(request))


class PlayerView(DetailView):
    """
    Show player detail info for other users.
    """
    model = Players
    template_name = 'player.html'


class OrganizerView(DetailView):
    """
    Show organizer details for other users.
    """
    model = Organizers
    template_name = 'organizer.html'


@login_required()
def show_my_profile(request, pk):
    """

    :param request:
    :param pk:
    :return:
    """
    # TODO: complete profile view
    if Organizers.objects.get(user=request.user).exists():
        return redirect('/profile')
    elif Players.objects.get(user=request.user).exists():
        pass
    else:
        return Http404("User doesn't exist")
    if request.user.pk != pk:
        return redirect('/player/%s' % pk )
    if request.method == 'POST':
        pass


