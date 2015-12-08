__author__ = 'kodiers'

import random

from datetime import timedelta

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.db.models import Q

from django.core.mail import EmailMultiAlternatives

from web.constants import *
from web.models import Events

from quests.settings import FAIL_EMAIL_SILENTLY

def create_password_str():
    """
    This function generate 8-length random password from numbers and letters
    """
    symbols = '1 2 3 4 5 6 7 8 9 0 Q W E R T Y U I O P A S D F G H J K L Z X C V B N M q w e r t y u i o p a s d f g h j k l z x c v b n m'
    sym_list = symbols.split()
    password_list = random.sample(sym_list, 8)
    password = ''.join(password_list)
    return password


def json_wrapper(func):
    """
    Decorator for json endpoints (like delete task/evemt)
    :param func: function to decorate
    :return: function object
    """
    def decorated_func(request, *args, **kwargs):
        error = ""
        if request.method == 'POST':
            if 'pk' in request.POST and request.POST['pk']:
                return func(request, *args, **kwargs)
            else:
                error = REQUEST_PARAMETRS_ERROR
        else:
            error = REQUEST_TYPE_ERROR
        return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))
    return decorated_func


def search_events(string, start_date, end_date, country, city, from_cost, to_cost, duration, organizer):
    """
    Search string in title or description of events or search events by parameters:
    from start_date to end_date, events in country, in city, where cost is > from_cost and cost < to_cost,
    where event.duration = duration, end event organizer is organizer
    :param string: String to search
    :param start_date: datetime object (from date)
    :param end_date: datetime object (to date)
    :param country: string to search events in eventplaces.country
    :param city: string to search events in eventplaces.city
    :param from_cost: string -  minimal price of event
    :param to_cost: string - max price of event
    :param duration:string -  duration of event
    :param organizer: string - organizer username of event
    :return: QuerySet object (list of Events)
    """
    if string is not None:
        objects = Events.objects.filter(Q(title__icontains=string) | Q(description__icontains=string))
    else:
        objects = Events.objects.all()
    if start_date is not None:
        objects = objects.filter(start_date__gte=start_date)
    if end_date is not None:
        objects = objects.filter(end_date__lte=end_date)
    if country is not None:
        objects = objects.filter(place__country__icontains=country)
    if city is not None:
        objects = objects.filter(place__city__icontains=city)
    if to_cost is not None:
        objects = objects.filter(price__lte=convert_str_to_float(to_cost))
    if from_cost is not None:
        objects = objects.filter(price__gte=convert_str_to_float(from_cost))
    if duration is not None:
        duration_value = timedelta(hours=convert_str_to_int(duration))
        objects = objects.filter(duration__lte=duration_value)
    if organizer is not None:
        objects = objects.filter(organizer__username__icontains=organizer)
    return objects


def send_user_notification(subject, notification, from_email, to_email):
    """
    Send notification to user
    :param subject: Subject of email
    :param notification: Text of notification
    :param from_email: Sender email
    :param to_email: User email
    :return:
    """
    template_html = 'notifications/notification.html'
    html_content = render_to_string(template_html, {'subject': subject, 'notification': notification})
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send(fail_silently=FAIL_EMAIL_SILENTLY)


def construct_map_link(url, api_key, country=None, city=None, street=None):
    """
    Construct link for google static maps api
    :param url: google static maps api should contains {zoom}, {api_key}, {country}, {city}, {street} parameters,
    for use in str.format method
    :param api_key: API_KEY to access Google Static Maps API
    :param country: country
    :param city: city
    :param street: street
    :return: url to access Google Maps API with defined parameters
    """
    zoom = 1
    if country is not None:
        zoom = 2
    else:
        country = ""
    if city is not None:
        zoom = 8
    else:
        city = ""
    if street is not None:
       zoom = 13
    else:
        street = ""
    url = url.format(api_key=api_key, zoom=zoom, country=country, city=city, street=street)
    return url


def convert_str_to_int(string):
    """
    Try convert string to int. If exception then return 0.
    :param string: string to convert
    :return: int
    """
    try:
        num = int(string)
    except ValueError:
        num = 0
    return num


def check_get_param(param, request):
    """
    Check if param in GET request. If True retuen param value els return None
    :param param: string - param name
    :param request: HttpRequest object
    :return: string - param value
    """
    if param in request.GET and request.GET[param] != '':
        paramValue = request.GET[param]
    else:
        paramValue = None
    return paramValue


def convert_str_to_float(string):
    """
    Try convert string to float. If exception then return 0.0.
    :param string: string to convert
    :return: float
    """
    try:
        num = float(string)
    except ValueError:
        num = 0.0
    return num