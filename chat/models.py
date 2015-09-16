from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Messages(models.Model):
    """
    Model for user messages
    """
    text = models.TextField(verbose_name="Text")
    from_user = models.ForeignKey(User, verbose_name="From", related_name='from_user')
    to_user = models.ForeignKey(User, verbose_name="To", related_name='to_user')
    date = models.DateTimeField(verbose_name="Date")
    new = models.BooleanField(verbose_name="New message", default=True)

    def __str__(self):
        return self.from_user.username + " to " + self.to_user.username

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ('date',)


class ContactList(models.Model):
    """
    Contact list model
    """
    owner = models.OneToOneField(User, verbose_name="Owner")
    contacts = models.ManyToManyField(User, verbose_name="Contacts", related_name="user_contacts")

    def __str__(self):
        return self.owner.username

    class Meta:
        verbose_name = "Contact list"
        verbose_name_plural = "Contact lists"
