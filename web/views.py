import datetime
import json

from django.http import Http404, HttpResponse

from django.shortcuts import render, render_to_response, redirect, get_list_or_404, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import ListView, DetailView, UpdateView

from django.utils.translation import ugettext as _

from django.core.mail import send_mail

from web.models import QuestsUsers, Players, Organizers, Contacts, Events, Teams, Tasks, Hints, EventsPlaces
from web.forms import UserRegistrationForm, RestorePasswordForm, CreateTeamForm, PlayerProfileForm, CreateEventForm

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
    Show and edit user (player) profile.
    :param request: HttpRequest
    :param pk: pk (id) of user
    :return: HttpResponse
    """
    message = ''
    error = ''
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Change players and user properties
            user.email = form.cleaned_data['email']
            if 'avatar' in request.FILES:
                user.questsusers.image = form.cleaned_data['avatar']
            user.players.description = form.cleaned_data['description']
            user.players.date_of_birth = form.cleaned_data['date_of_birth']
            user.players.sex = form.cleaned_data['sex']
            if not Contacts.objects.filter(user=user).exists():
                # Create contacts for user if not exists
                user_contacts = Contacts()
                user_contacts.user = user
                user_contacts.save()
            user.contacts.country = form.cleaned_data['country']
            user.contacts.city = form.cleaned_data['city']
            user.contacts.street = form.cleaned_data['street']
            user.contacts.phone = form.cleaned_data['phone']
            user.contacts.skype = form.cleaned_data['skype']
            user.contacts.site = form.cleaned_data['site']
            user.questsusers.save()
            user.players.save()
            user.contacts.save()
            user.save()
            message = _("Your profile updated successfully!")
        else:
            error = FORM_FIELDS_ERROR
    # Initialize form fields dictionary
    intial_formdata = {'avatar': user.questsusers.image, 'description': user.players.description,
                       'date_of_birth': user.players.date_of_birth, 'sex': user.players.sex,
                       'country': '', 'city': '', 'street': '', 'phone':'', 'skype': '', 'site': '',
                       'email': user.email}
    if Contacts.objects.filter(user=user).exists():
        # Load contacts in form field for user if exists
        intial_formdata['country'] = user.contacts.country
        intial_formdata['city'] = user.contacts.city
        intial_formdata['street'] = user.contacts.street
        intial_formdata['phone'] = user.contacts.phone
        intial_formdata['skype'] = user.contacts.skype
        intial_formdata['site'] = user.contacts.site
    form = PlayerProfileForm(request.POST or None, initial=intial_formdata)
    return render_to_response('player_profile.html', {'form': form, 'object': user, 'message': message, 'error': error},
                              context_instance=RequestContext(request))


@login_required()
def create_event(request, pk=None):
    """
    Create new event.
    If pk != none edit event with pk.
    :param request: HttpRequest
    :return: HttpResponse
    """
    # TODO: Recreate to ajax
    error = ''
    if pk is not None:
        event = get_object_or_404(Events, pk=pk)
        # Check that user want edit created by self
        if event.organizer != request.user:
            error = _("You are not creator of this event")
            return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))
    else:
        event = None
    if request.method == 'POST':
        form = CreateEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            return redirect('/create_event/' + str(event.pk) + '/')
        else:
            error = FORM_FIELDS_ERROR
    else:
        form = CreateEventForm(initial={'organizer':request.user}, instance=event)
    return render_to_response('create_event.html', {'form': form, 'event': event, 'error': error},
                              context_instance=RequestContext(request))


@login_required()
def add_task(request):
    """
    Add task to event through AJAX request.
    :param request: HttpRequest (from AJAX function add_task())
    :return: HttpResponse - if success return json else retuen error page
    """
    # TODO: add edit view
    error = ''
    if request.method == 'POST':
        if request.POST['event']:
            event = Events.objects.get(pk=request.POST['event'])
            new_task = Tasks()
            new_task.event = event
            new_place = EventsPlaces()
            # Filling task properties
            if request.POST['title']:
                new_task.title = request.POST['title']
            if request.POST['description']:
                new_task.description = request.POST['description']
            if request.POST['map_link']:
                new_task.map_link = request.POST['map_link']
            if request.POST['score']:
                new_task.score = request.POST['score']
            if request.POST['answer']:
                new_task.answer = request.POST['answer']
            if request.POST['time']:
                new_task.time = request.POST['time']
            # Filing EventPlace properties
            if request.POST['country']:
                new_place.country = request.POST['country']
            if request.POST['city']:
                new_place.city = request.POST['city']
            if request.POST['street']:
                new_place.street = request.POST['street']
            if request.POST['lon']:
                new_place.lon = request.POST['lon']
            if request.POST['lat']:
                new_place.lat = request.POST['lat']
            new_place.save()
            new_task.place = new_place
            new_task.save()
            # Create hint for the task
            hint = ''
            if request.POST['hint']:
                hint = Hints()
                hint.task = new_task
                hint.text = request.POST['hint']
                hint.save()
            json_answer = { 'title': new_task.title, 'description': new_task.description, 'maplink': new_task.map_link,
                            'score': new_task.score, 'answer': new_task.answer, 'time': new_task.time,
                            'event': new_task.event.pk }
            if hint != '':
                json_answer['hint'] = hint.text
            else:
                json_answer['hint'] = 'None'
            return HttpResponse(json.dumps(json_answer), content_type="application/json")
        else:
            error = _('Event undefined!')
    else:
        error = REQUEST_TYPE_ERROR
        return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))

