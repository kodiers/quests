import datetime
import json

from django.http import HttpResponse

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.utils.translation import ugettext as _
from django.utils.timezone import utc

from web.constants import SIMPLE_JSON_ANSWER

from chat.models import Messages, ContactList

# Create your views here.


@login_required()
def show_contact_list(request):
    """

    :param request:
    :return:
    """
    if ContactList.objects.filter(owner=request.user).exists():
        contactlist = ContactList.objects.get(owner=request.user)
    else:
        contactlist = ContactList()
        contactlist.owner = request.user
        contactlist.save()
    return render_to_response('contacts_list.html', {'object': contactlist}, RequestContext(request))


@login_required()
def check_username(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            return HttpResponse(json.dumps(SIMPLE_JSON_ANSWER), content_type="application/json")
        SIMPLE_JSON_ANSWER['code'] = 2
    return HttpResponse(json.dumps(SIMPLE_JSON_ANSWER), content_type="application/json")



@login_required()
def new_message(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        pass
    else:
        return render_to_response('new_message.html', RequestContext(request))

