import json

from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail

from pages.models import FAQ, Pages, Contacts
from pages.constants import MESSAGE_SUBJECT

from quests.settings import EMAIL_HOST_USER

# Create your views here.

class FAQListView(ListView):
    """
    Show list of all questions. Ordering by model definition
    """
    model = FAQ
    template_name = "pages/faq.html"


class PagesDetailView(DetailView):
    """
    Show content of page.
    """
    model = Pages
    template_name = "pages/page.html"
    slug_field = 'url'
    slug_url_kwarg = 'url'


class ContactsDetailView(DetailView):
    """

    """
    model = Contacts
    template_name = "pages/contacts.html"
    slug_field = 'url'
    slug_url_kwarg = 'url'


def send_email_message(request):
    """
    Send message from feedback form through AJAX request.
    :param request: HttpRequest (from JS file send_email)
    :return: HttpResponse - if success return json {data: 1} else return json {data: 2}
    """
    if request.method == 'POST':
        if 'SenderName' in request.POST and 'SenderEmail' in request.POST \
                and 'SenderMessage' in request.POST and 'token' in request.POST:
            senderName = request.POST['SenderName']
            senderEmail = request.POST['SenderEmail']
            message = request.POST['SenderMessage']
            contacts = Contacts.objects.get(url=request.POST['token'])
            email_message = """Message from site. \n
             Message from {senderName} \n Sender email: {senderEmail} \n Message: {message}""".format(
                senderName=senderName, senderEmail=senderEmail, message=message)
            recipients = [contacts.email]
            try:
                send_mail(MESSAGE_SUBJECT, email_message, EMAIL_HOST_USER, recipients)
                return HttpResponse(json.dumps({'data': 1}), content_type='application/json')
            except:
                return HttpResponse(json.dumps({'data': 2}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'data': 2}), content_type='application/json')





