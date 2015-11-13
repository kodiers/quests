import datetime
import json

from django.http import HttpResponse

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from django.views.generic import ListView, DetailView

from django.utils.translation import ugettext as _
from django.utils.timezone import utc

from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from web.models import QuestsUsers, Players, Organizers, Contacts, Events, Teams, Tasks, Hints, EventsPlaces, Photos, \
    TaskStatistics, EventStatistics
from web.forms import UserRegistrationForm, RestorePasswordForm, CreateTeamForm, PlayerProfileForm, CreateEventForm, \
    OrganizerProfileForm

from quests.settings import EMAIL_HOST_USER, FAIL_EMAIL_SILENTLY, GOOGLE_MAPS_BROWSER_API_KEY, GOOGLE_API_STRING_URL

from web.functions import create_password_str, json_wrapper, search_events, send_user_notification, construct_map_link

from web.constants import *


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
                    email_message = """Hello! You was registered on site GetQuests.com. \n
                    Your login {login} \n Your password {password} \n Your email {email} \n
                    Thank you!""".format(login=form.cleaned_data['login'],
                                         password=form.cleaned_data['password1'],
                                         email=form.cleaned_data['email'])
                    recipients = [new_user.email]
                    send_mail(email_subject, email_message, EMAIL_HOST_USER, recipients, fail_silently=FAIL_EMAIL_SILENTLY)
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
            # error = form.errors
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
    if request.user.is_authenticated():
        message = _("You are already registered!")
        return render_to_response('register_success.html', {'message': message},
                                  context_instance=RequestContext(request))
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
                send_mail(email_subject, email_message, EMAIL_HOST_USER, recipients, fail_silently=FAIL_EMAIL_SILENTLY)
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
    error = ""
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
                    error = USER_NOT_ACTIVE
            else:
                error = INCORRECT_USERNAME_PASSWORD
        else:
            error = INCORRECT_USERNAME_PASSWORD
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
    View for regiter user or team in event.
    :param request: HttpRequest
    :param flag: 'player' or 'team' if event is team
    :return: HttpResponse object
    """
    event = None
    error = ''
    if request.method == 'POST':
        if 'event_pk' in request.POST:
            event = get_object_or_404(Events, pk=request.POST['event_pk'])
            if flag == 'player':
                event.registered_players.add(request.user)
                error = SUCCESSFULLY_REGITERED
                player_notification = _('You was succesfully registered to event %s' % event.title)
                # Send notification to player
                send_user_notification(SUCCESSFULLY_REGITERED, player_notification, EMAIL_HOST_USER, request.user.email)
                # Send notification to organizer
                org_subject = _("Player was registered to your event %s" % event.title)
                org_notification = _("Player {player} was registered to your event {event}".format(
                    player=request.user.username, event=event.title))
                send_user_notification(org_subject, org_notification, EMAIL_HOST_USER, event.organizer.email)
            elif flag == 'team':
                try:
                    team = Teams.objects.get(creator=request.user)
                    if team in event.registered_teams.all():
                        error = TEAM_ALREADY_REGISTERED
                    else:
                        event.registered_teams.add(team)
                        error = _(TEAM_WAS_REGISTERED % event.title)
                        creator_notification = _("Your team {team} was registered to event {event}".format(
                            team=team.title, event=event.title))
                        # Send notification to team creator
                        send_user_notification(error, creator_notification, EMAIL_HOST_USER, team.creator.email)
                        # Send notification to organizer
                        org_subject = _("Team was registered to your event.")
                        org_notification = _("Team {team} was registered to your event {event}".format(
                            team=team.title, event=event.title
                        ))
                        send_user_notification(org_subject, org_notification, EMAIL_HOST_USER, event.organizer.email)
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
def show_my_profile(request):
    """
    Show and edit user (player) profile.
    :param request: HttpRequest
    :return: HttpResponse
    """
    message = ''
    error = ''
    user = User.objects.get(pk=request.user.pk)
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
            user.players.show_personal_info = form.cleaned_data['show_personal_info']
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
                       'email': user.email, 'show_personal_info': user.players.show_personal_info}
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
    :param pk: id of event for edit
    :return: HttpResponse
    """
    error = ''
    if pk is not None:
        event = get_object_or_404(Events, pk=pk)
        # Try get existing event place object
        if event.place:
            place = EventsPlaces.objects.get(pk=event.place.pk)
        else:
            place = EventsPlaces()
        # Check that user want edit created by self
        if event.organizer != request.user:
            error = _("You are not creator of this event")
            return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))
    else:
        event = None
        place = EventsPlaces()
    if request.method == 'POST':
        form = CreateEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            if 'country' in request.POST and request.POST['country']:
                place.country = request.POST['country']
            if 'city' in request.POST and request.POST['city']:
                place.city = request.POST['city']
            if 'street' in request.POST and request.POST['street']:
                place.street = request.POST['street']
            place.save()
            event.place = place
            event.map_link = construct_map_link(GOOGLE_API_STRING_URL, GOOGLE_MAPS_BROWSER_API_KEY, place.country, place.city, place.street)
            event.save()
            return redirect('/create_event/' + str(event.pk) + '/')
        else:
            error = FORM_FIELDS_ERROR
    else:
        form = CreateEventForm(initial={'organizer':request.user, 'duration':'1d 00:00:00',
                                        'country': place.country, 'city': place.city,
                                        'street': place.street}, instance=event)
    return render_to_response('create_event.html', {'form': form, 'event': event, 'error': error},
                              context_instance=RequestContext(request))


@login_required()
def add_task(request):
    """
    Add task to event through AJAX request.
    :param request: HttpRequest (from AJAX function add_task())
    :return: HttpResponse - if success return json else retuen error page
    """
    error = ''
    if request.method == 'POST':
        if 'event' in request.POST and request.POST['event']:
            event = Events.objects.get(pk=request.POST['event'])
            new_task = Tasks()
            new_task.event = event
            new_place = EventsPlaces()
            # Filling task properties
            if 'title' in request.POST and request.POST['title']:
                new_task.title = request.POST['title']
            if 'description' in request.POST and request.POST['description']:
                new_task.description = request.POST['description']
            if 'score' in request.POST and request.POST['score']:
                new_task.score = request.POST['score']
            if 'answer' in request.POST and request.POST['answer']:
                new_task.answer = request.POST['answer']
            if 'time' in request.POST and request.POST['time']:
                new_task.time = request.POST['time']
            # Filing EventPlace properties
            if 'country' in request.POST and request.POST['country']:
                new_place.country = request.POST['country']
            if 'city' in request.POST and request.POST['city']:
                new_place.city = request.POST['city']
            if 'street' in request.POST and request.POST['street']:
                new_place.street = request.POST['street']
            #     Longtitude and latitude for task not used in this version
            # if 'lon' in request.POST:
            #     if request.POST['lon'] == '' or request.POST['lon'] == 'None':
            #         new_place.lon = 0.0
            #     else:
            #         new_place.lon = float(request.POST['lon'])
            # if 'lat' in request.POST:
            #     if request.POST['lat'] == '' or request.POST['lat'] == 'None':
            #         new_place.lat = 0.0
            #     else:
            #         new_place.lat = float(request.POST['lat'])
            new_place.save()
            new_task.place = new_place
            new_task.save()
            # Create hint for the task
            hint = ''
            if 'hint' in request.POST and request.POST['hint']:
                hint = Hints()
                hint.task = new_task
                hint.text = request.POST['hint']
                hint.save()
            json_answer = { 'title': new_task.title, 'description': new_task.description, 'maplink': new_task.map_link,
                            'score': new_task.score, 'answer': new_task.answer, 'time': new_task.time,
                            'event': new_task.event.pk, 'task_pk': new_task.pk }
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


@login_required()
@json_wrapper
def delete_task(request):
    """
    Delete task view. Accept post request from AJAX function.
    :param request: HttpRequest (from AJAX function delete_task())
    :return: HttpResponse - if success return json else return error page
    """
    task = Tasks.objects.get(pk=request.POST['pk'])
    task.delete()
    return HttpResponse(json.dumps(SIMPLE_JSON_ANSWER), content_type="application/json")


@login_required()
def edit_task(request):
    """
    Edit task view. Accept post request from AJAX function.
    :param request: HttpRequest (from AJAX function edit_task())
    :return: HttpResponse - if success return json else return error page
    """
    # TODO: create view to AJAX edit_task function
    error = ''
    if request.method == 'POST':
        if 'pk' in request.POST and request.POST['pk']:
            task = get_object_or_404(Tasks, pk=request.POST['pk'])
        else:
            error = REQUEST_PARAMETRS_ERROR
            return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))
        if 'title' in request.POST and request.POST['title']:
            task.title = request.POST['title']
        if 'description' in request.POST and request.POST['description']:
            task.description = request.POST['description']
        if 'score' in request.POST and request.POST['score']:
            task.score = request.POST['score']
        if 'answer' in request.POST and request.POST['answer']:
            task.answer = request.POST['answer']
        if 'time' in request.POST and request.POST['time']:
            task.time = request.POST['time']
        task.save()
        # Filing EventPlace properties
        if 'placepk' in request.POST and request.POST['placepk']:
            place = EventsPlaces.objects.get(pk=request.POST['placepk'])
            if 'country' in request.POST and request.POST['country']:
                place.country = request.POST['country']
            if 'city' in request.POST and request.POST['city']:
                place.city = request.POST['city']
            if 'street' in request.POST and request.POST['street']:
                place.street = request.POST['street']
            # Longtitude and latitude not used in this version
            # if 'lon' in request.POST:
            #     if request.POST['lon'] == 'None' or request.POST['lon'] == '':
            #         place.lon = 0.0
            #     else:
            #         place.lon = float(request.POST['lon'])
            # if 'lat' in request.POST:
            #     if request.POST['lat'] == 'None' or request.POST['lat'] == '':
            #         place.lat = 0.0
            #     else:
            #         place.lat = float(request.POST['lat'])
            place.save()
        hint = None
        json_answer = { 'title': task.title, 'description': task.description, 'maplink': task.map_link,
                            'score': task.score, 'answer': task.answer, 'time': task.time,
                            'event': task.event.pk, 'task_pk': task.pk }
        if 'hintpk' in request.POST and request.POST['hintpk']:
            hint = Hints.objects.get(pk=request.POST['hintpk'])
            if request.POST['hint']:
                hint.text = request.POST['hint']
                hint.save()
                json_answer['hint'] = hint.text
        elif 'hint' in request.POST and request.POST['hint']:
            hint = Hints()
            hint.text = request.POST['hint']
            hint.task = task
            hint.save()
            json_answer['hint'] = hint.text
        else:
            json_answer['hint'] = 'None'
        return HttpResponse(json.dumps(json_answer), content_type="application/json")
    else:
        error = REQUEST_TYPE_ERROR
        return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))


@login_required()
@json_wrapper
def delete_event(request):
    """
    Delete event view. Accept post request from AJAX function.
    :param request: HttpRequest (from AJAX function delete_event())
    :return: HttpResponse - if success return json else return error page
    """
    event = Events.objects.get(pk=request.POST['pk'])
    if request.user == event.organizer:
        event.delete()
    return HttpResponse(json.dumps(SIMPLE_JSON_ANSWER), content_type="application/json")


@login_required()
@json_wrapper
def delete_team(request):
    """
    Delete team view. Accept post request from AJAX function.
    :param request: HttpRequest (from AJAX function delete_team())
    :return: HttpResponse - if success return json else return error page
    """
    team = Teams.objects.get(pk=request.POST['pk'])
    if request.user == team.creator:
        team.delete()
    return HttpResponse(json.dumps(SIMPLE_JSON_ANSWER), content_type="application/json")


@login_required()
@json_wrapper
def leave_team(request):
    """
    Leave team view. Accept post request from AJAX function.
    :param request: HttpRequest (from AJAX function leave_team())
    :return: HttpResponse - if success return json else return error page
    """
    team = Teams.objects.get(pk=request.POST['pk'])
    team.players.remove(request.user)
    return HttpResponse(json.dumps(SIMPLE_JSON_ANSWER), content_type="application/json")


@login_required()
@json_wrapper
def unregister_event(request):
    """
    Unregister event view. Accept post request from AJAX function.
    :param request: HttpRequest (from AJAX function unregister_event())
    :return: HttpResponse - if success return json else return error page
    """
    event = Events.objects.get(pk=request.POST['pk'])
    event.registered_players.remove(request.user)
    return HttpResponse(json.dumps(SIMPLE_JSON_ANSWER), content_type="application/json")


@login_required()
def upload_photos(request):
    """
    Upload photo AJAX endpoint. Accept post request from AJAX function.
    :param request: HttpRequest (from AJAX function upload())
    :return: HttpResponse - if success return json else return error page
    """
    # TODO: create ajax request(script) for upload photos and completed the view
    error = ''
    if request.method == 'POST':
        if 'photo' in request.FILES:
            photo = Photos()
            image = request.FILES['photo']
            photo.user = request.user
            photo.image = image
            if 'title' in request.POST and request.POST['title']:
                photo.title = request.POST['title']
            if 'description' in request.POST and request.POST['description']:
                photo.description = request.POST['description']
            if 'date' in request.POST and request.POST['date']:
                photo.date = request.POST['date']
            if 'event' in request.POST and request.POST['event']:
                event = Events.objects.get(pk=request.POST['event'])
                photo.event = event
            photo.save()
            return HttpResponse(json.dumps(SIMPLE_JSON_ANSWER), content_type="application/json")
        else:
            error = REQUEST_PARAMETRS_ERROR
    else:
        error = REQUEST_TYPE_ERROR
    return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))


@login_required()
@json_wrapper
def delete_photo(request):
    """
    Delete photo view. Accept post request from AJAX function .
    :param request: HttpRequest (from AJAX function delete_photo())
    :return: HttpResponse - if success return json else return error page
    """
    photo = Photos.objects.get(pk=request.POST['pk'])
    if photo.user == request.user:
        photo.delete()
        return HttpResponse(json.dumps(SIMPLE_JSON_ANSWER), content_type="application/json")
    else:
        error = _("You are not owner of photo")
        return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))


@login_required()
def play_event(request, pk):
    """
    Show play events page. If user just started => then create eventstatistics object for this event and user.
    :param request: HttpRequest object
    :param pk: pk of event
    :return: HttpResponse (render play_event.html template)
    """
    error = ''
    event = Events.objects.get(pk=pk)
    user_teams = request.user.players.get_user_teams()
    user_registered = False
    user_team = None
    if not event.started:
        error = _("Event is not started!")
        return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))
    if event.is_team:
        # Check if user in registered team
        for team in user_teams:
            if team in event.registered_teams.all():
                user_team = team
                user_registered = True
    else:
        # Check if user registered by self
        if request.user in event.registered_players.all():
            user_registered = True
    if not user_registered:
        # If user isn't register - show error
        error = _("You are not registered to this event")
        return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))
    tasks = event.get_event_tasks()
    try:
        # Try get existing EventStatistics object. If not => create new one
        eventstat = EventStatistics.objects.filter(event=event).get(player=request.user)
    except EventStatistics.DoesNotExist:
        eventstat = EventStatistics()
        eventstat.event = event
        eventstat.team = user_team
        eventstat.player = request.user
        eventstat.start_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        eventstat.save()
    return render_to_response('play_event.html', {'event': event, 'tasks': tasks, 'user_team': user_team, 'eventstat': eventstat},
                              context_instance=RequestContext(request))

# TODO: complete comments from here
@login_required()
@json_wrapper
def start_task(request):
    """
    Start task. Accept post request from AJAX function.
    :param request: HttpRequest (from AJAX function start_task())
    :return: HttpResponse - if success return json else return error page
    """
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    error = ''
    task = Tasks.objects.get(pk=request.POST['pk'])
    task_completed = False
    registered_team = None
    if task.event.is_team:
        user_teams = request.user.players.get_user_teams()
        for team in user_teams:
            if team in task.event.registered_teams.all():
                registered_team = team
                taskstat = TaskStatistics.objects.filter(task=task).filter(team=registered_team).filter(completed=True)
                if taskstat:
                    error = _("Your team member answered for this task")
                    task_completed = True
    else:
        taskstat = TaskStatistics.objects.filter(task=task).filter(player=request.user).filter(completed=True)
        if taskstat:
            error = _("You are answered for this task")
            task_completed = True
    if not task_completed:
        taskstat = TaskStatistics.objects.filter(task=task).filter(player=request.user).filter(started=True)
        if not taskstat:
            taskstat = TaskStatistics()
            taskstat.task = task
            taskstat.start_time = now
            taskstat.player = request.user
            taskstat.started = True
            if task.event.is_team:
                taskstat = registered_team
            taskstat.save()
        return HttpResponse(json.dumps(SIMPLE_JSON_ANSWER), content_type="application/json")
    else:
        return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))


@login_required()
@json_wrapper
def task_answer(request):
    """
    Complete task and check if answer is correct. Accept request from AJAX function.
    :param request: HttpRequest (from send_answer JS function)
    :return: HttpResponse - if success return json else return error page
    """
    error = ''
    user = request.user
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    task = Tasks.objects.get(pk=request.POST['pk'])
    taskstat = TaskStatistics.objects.filter(task=task).filter(player=request.user).get(started=True)
    correct_time = False
    if taskstat:
        if taskstat.completed:
            error = _("You are answered for this task")
        else:
            answer = request.POST['answer']
            task_fact_duraction = abs(now - taskstat.start_time)
            taskstat.time = task_fact_duraction.seconds // 60
            if task.answer == answer:
                correct_time =True
                if task.time is not None:
                    if task.time != 'None':
                        if taskstat.time <= int(task.time):
                           correct_time = True
                        else:
                           correct_time = False
            if correct_time:
                taskstat.answered = True
                taskstat.score = task.score
                user.players.add_points(task.score)
                if task.event.is_team:
                    team = taskstat.team
                    team.add_points(task.score)
            taskstat.end_time = now
            taskstat.completed = True
            taskstat.save()
            return HttpResponse(json.dumps(SIMPLE_JSON_ANSWER), content_type="application/json")
    else:
        error = _("This task isn't started")
    return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))


@login_required()
@json_wrapper
def complete_event(request):
    """
    Complete event. Accept request from AJAX function.
    :param request: HttpRequest (from complete_event JS function)
    :return: HttpResponse - if success return json else return error page
    """
    eventstat = EventStatistics.objects.get(pk=request.POST['pk'])
    user_team = None
    if request.user == eventstat.player:
        event = eventstat.event
        tasks = Tasks.objects.filter(event=event)
        tasks_score = 0
        for task in tasks:
            try:
                taskstat = TaskStatistics.objects.filter(player=request.user).filter(completed=True).filter(task=task).get(answered=True)
            except TaskStatistics.DoesNotExist:
                taskstat = None
            if taskstat:
                tasks_score += taskstat.score
        eventstat.completed = True
        eventstat.score = tasks_score
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        eventstat.end_time = now
        event_fact_duration = abs(now - eventstat.start_time)
        eventstat.time = event_fact_duration.seconds // 60
        eventstat.save()
        return HttpResponse(json.dumps(SIMPLE_JSON_ANSWER), content_type="application/json")
    else:
        error = _("You are not started this event")
        return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))


@login_required()
def show_my_organizer_profile(request):
    """
    Show and edit user (organizer) profile.
    :param request: HttpRequest
    :return: HttpResponse
    """
    message = ''
    error = ''
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        form = OrganizerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Change players and user properties
            user.email = form.cleaned_data['email']
            if 'avatar' in request.FILES:
                user.questsusers.image = form.cleaned_data['avatar']
            user.organizers.description = form.cleaned_data['description']
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
            user.organizers.save()
            user.contacts.save()
            user.save()
            message = _("Your profile updated successfully!")
        else:
            error = FORM_FIELDS_ERROR
    # Initialize form fields dictionary
    intial_formdata = {'avatar': user.questsusers.image, 'description': user.organizers.description,
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
    form = OrganizerProfileForm(request.POST or None, initial=intial_formdata)
    return render_to_response('organizer_profile.html',
                              {'object': user, 'message': message, 'error': error , 'form': form},
                              context_instance=RequestContext(request))


class EventsListView(ListView):
    """
    Show events from today start_date. Default events view.
    """
    template_name = 'events.html'
    queryset = Events.objects.filter(start_date__gte=datetime.datetime.now())
    paginate_by = 20


class AllEventsListView(ListView):
    """
    Show all events. Ordering like in model.
    """
    template_name = 'events.html'
    model = Events
    paginate_by = 20


def search_events_view(request):
    """
    Search events by start date, end date, title and description
    :param request: HttpRequest (with search, start_date and end_date parameters - or without it)
    :return: HttpResponse object
    """
    if 'search' not in request.GET or request.GET['search'] == '':
        search_string = None
    else:
        search_string = request.GET['search']
    start_date = None
    end_date = None
    if 'start_date' in request.GET:
        if request.GET['start_date'] != '':
            try:
                # Convert string ['start_date'] to datetime object
                start_date = datetime.datetime.strptime(request.GET['start_date'], "%Y-%m-%d %H:%M")
            except ValueError:
                start_date = None
    if 'end_date' in request.GET:
        if request.GET['end_date'] != '':
            try:
                # Convert string ['end_date'] to datetime object
                end_date = datetime.datetime.strptime(request.GET['end_date'], "%Y-%m-%d %H:%M")
            except ValueError:
                end_date = None
    # Search events
    objects = search_events(search_string, start_date, end_date)
    paginator = Paginator(objects, 20)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    return render_to_response('events.html', {'object_list': object_list}, context_instance=RequestContext(request))


class PlayersListView(ListView):
    """
    Show list of all players. Ordering by username
    """
    queryset = Players.objects.all().order_by('user__username')
    template_name = "players.html"
    paginate_by = 20


def search_players_view(request):
    """
    Search players by username and description
    :param request: HttpRequest (with search parameter - or without it)
    :return: HttpResponse object
    """
    if 'search' not in request.GET or request.GET['search'] != '':
        objects = Players.objects.filter(Q(user__username__icontains=request.GET['search'])|Q(description__icontains=request.GET['search']))
    else:
        objects = Players.objects.all()
    objects = objects.order_by('user__username')
    paginator = Paginator(objects, 20)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    return render_to_response('players.html', {'object_list': object_list}, context_instance=RequestContext(request))


class OrganizerListView(ListView):
    """
    Show list of all organizers. Ordering by username
    """
    queryset = Organizers.objects.all().order_by('user__username')
    template_name = 'organizers.html'
    paginate_by = 20


def search_organizers_view(request):
    """
    Search organizers by username and description
    :param request: HttpRequest (with search parameter - or without it)
    :return: HttpResponse object
    """
    if 'search' not in request.GET or request.GET['search'] != '':
        objects = Organizers.objects.filter(Q(user__username__icontains=request.GET['search'])|Q(description__icontains=request.GET['search']))
    else:
        objects = Organizers.objects.all()
    objects = objects.order_by('user__username')
    paginator = Paginator(objects, 20)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    return render_to_response('organizers.html', {'object_list': object_list}, context_instance=RequestContext(request))
