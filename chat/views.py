import json

from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from chat.models import Chat, Messages
from chat.constants import CHAT_ID_ERROR
from chat.functions import set_new_messages_to_old

from web.constants import REQUEST_TYPE_ERROR, REQUEST_PARAMETRS_ERROR

from quests.settings import API_KEY

# Create your views here.


@login_required()
def show_contact_list(request):
    """
    Show contacts list.
    :param request: HttpRequest
    :return: HttpResponse (all chats for current user)
    """
    chats = Chat.objects.filter(users=request.user)
    if chats:
        for chat in chats:
            # add partner field for chat for chats
            chat.partner = chat.users.exclude(id=request.user.id)[0]
    return render_to_response('contacts_list.html', {'chats': chats, 'object': request.user},
                              context_instance=RequestContext(request))


@login_required()
def check_username(request):
    """
    Check username before send message. Accept request from AJAX function.
    :param request: HttpRequest from check_username script AJAX endpoint
    :return: If user with this username found return code 1, else return code 2 as AJAX.
    If error in request or parameters return error page
    """
    if request.method == 'POST':
        if 'receiver' in request.POST:
            receiver = request.POST['receiver']
            try:
                user_exist = User.objects.get(username=receiver)
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                answer = {'code': 2} # if user not found or multiple users found - return code 2
                return HttpResponse(json.dumps(answer), content_type="application/json")
            answer = {'code': 1} # if user found return code 1
            return HttpResponse(json.dumps(answer), content_type="application/json")
        else:
            return render_to_response('error.html', {'error': REQUEST_PARAMETRS_ERROR},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('error.html', {'error': REQUEST_TYPE_ERROR},
                                  context_instance=RequestContext(request))


@login_required()
def send_message(request):
    """
    Save message in database. And redirect to chat room. If chat not exists - create new chat room.
    :param request: HttRequest as POST
    :return: If not errors and request POST return redirect to chat room page. Else return error page.
    """
    if request.method == 'POST':
        receiver = User.objects.get(username=request.POST['receiver'])
        sender = User.objects.get(username=request.POST['sender'])
        chats = Chat.objects.filter(users=receiver).filter(users=request.user)
        chat = None
        new_message = Messages()
        if chats.exists():
            # If chat exist get first chat room for current user and receiver
            chat = chats[0]
            old_messages = Messages.objects.filter(chat=chat).filter(new=True)
            set_new_messages_to_old(old_messages)
        else:
            chat = Chat.objects.create()
            chat.users.add(sender, receiver)
        new_message.chat = chat
        new_message.sender = sender
        new_message.text = request.POST['text']
        new_message.new = True
        new_message.save()
        chat.have_new_message = True
        chat.save()
        return redirect('/messages/chat/' + str(chat.id) +'/')
    else:
        return render_to_response('error.html', {'error': REQUEST_TYPE_ERROR}, context_instance=RequestContext(request))


@login_required()
def show_chat(request, id):
    """
    Show main chat window.
    :param request: HttpRequest
    :param id: chat id
    :return: HttpResponse (messages, receiver and chat objects)
    """
    try:
       chat = Chat.objects.get(id=id)
       chat.have_new_message = False
       chat.save()
    except (Chat.DoesNotExist, Chat.MultipleObjectsReturned):
        error = CHAT_ID_ERROR
        return render_to_response('error.html', {'error': error}, context_instance=RequestContext(request))
    for user in chat.users.all():
        if user != request.user:
            receiver = user
    messages = Messages.objects.filter(chat=chat).order_by('datetime')
    new_messages = messages.filter(new=True)
    set_new_messages_to_old(new_messages)
    return render_to_response('chat.html', {'messages': messages, 'receiver': receiver, 'chat': chat,
                                            'object': request.user},
                              context_instance=RequestContext(request))


@csrf_exempt
def send_message_api(request):
    """
    API endpoint for tornado application (chatapp.py). Save message in database and return message object as JSON.
    :param request: HttpRequest from tornado app. Should have chat (chat.id), text (message text),
    sender (sender username) parameters
    :return: Return Message object as JSON.
    """
    if request.method == "POST":
        if request.POST['API_KEY'] == API_KEY:
            chat = Chat.objects.get(id=request.POST['chat'])
            text = request.POST['text']
            sender = User.objects.get(username=request.POST['sender'])
            if sender not in chat.users.all():
                return HttpResponse(json.dumps({'chat': chat.pk, 'Error': 'incorrect chat user'}))
            messages = Messages.objects.filter(chat=chat).filter(new=True)
            set_new_messages_to_old(messages)
            new_message = Messages()
            new_message.sender = sender
            new_message.chat = chat
            new_message.text = text
            new_message.new = True
            new_message.save()
            chat.have_new_message = True
            chat.save()
            return HttpResponse(json.dumps({
                'sender': sender.username,
                'text': text,
                'chat': chat.id,
                'datetime': new_message.datetime.strftime('%d-%m-%Y %H:%M')
            }), content_type="application/json")




