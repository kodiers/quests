__author__ = 'kodiers'

import random

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.db.models import Q

from web.constants import *
from web.models import Events

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


def search_events(string, start_date, end_date):
    """
    Search string in title or description of events or search events from event.start_date=start_date
    to event.end_date = end_date
    :param string: String to search
    :param start_date: datetime object (from date)
    :param end_date: datetime object (to date)
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
    return objects