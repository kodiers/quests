from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Chat(models.Model):
    """
    Chat model. Contains all users in chat.
    """
    users = models.ManyToManyField(User, verbose_name="Users")
    have_new_message = models.BooleanField(default=False, verbose_name="New message")

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"


class Messages(models.Model):
    """
    Message model.
    """
    sender = models.ForeignKey(User, verbose_name="Sender")
    chat = models.ForeignKey(Chat, verbose_name="Chat")
    text = models.TextField(verbose_name="Message")
    new = models.BooleanField(default=False, verbose_name="New")
    datetime = models.DateTimeField(auto_now=True, verbose_name="Date and time")

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
