from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Chat(models.Model):
    """
    Chat model. Contains all users in chat.
    """
    users = models.ManyToManyField(User, verbose_name=_("Users"))
    have_new_message = models.BooleanField(default=False, verbose_name=_("New message"))

    def get_message_count(self):
        """

        :return:
        """
        msg_count = Messages.objects.filter(chat=self).count()
        return msg_count

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"


class Messages(models.Model):
    """
    Message model.
    """
    sender = models.ForeignKey(User, verbose_name=_("Sender"))
    chat = models.ForeignKey(Chat, verbose_name="Chat")
    text = models.TextField(verbose_name=_("Message"))
    new = models.BooleanField(default=False, verbose_name=_("New"))
    datetime = models.DateTimeField(auto_now=True, verbose_name=_("Date and time"))

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
