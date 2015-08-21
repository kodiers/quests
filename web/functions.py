__author__ = 'kodiers'

import random


from django.shortcuts import render_to_response
from django.template import RequestContext

from web.constants import *

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