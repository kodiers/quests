from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class QuestsUsers(models.Model):
    """
    Extending base user model.
    If is_organizer == True - user is quests organizer
    """
    user = models.OneToOneField(User)
    is_organizer = models.BooleanField(default=False, verbose_name="Organizer")
    image = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name="Avatar")

    def image_tag(self):
        return u'<img src="%s" height=75 width=75 />' % (self.image.url)

    image_tag.short_description = "Current avatar"
    image_tag.allow_tags = True

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Quests users"
        verbose_name = "Quest user"


class Contacts(models.Model):
    """
    Model for user and organisator contacts
    """
    user = models.ForeignKey(User)
    country = models.CharField(max_length=255, null=True, blank=True, verbose_name="Country")
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name="City")
    street = models.TextField(verbose_name="Street", null=True, blank=True)
    phone = models.TextField(verbose_name="Phone number", null=True, blank=True)
    skype = models.CharField(max_length=255, null=True, blank=True, verbose_name="Skype")
    site = models.TextField(verbose_name="Web site", null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Contacts"
        verbose_name = "Contact"


class Players(models.Model):
    """
    Model for define players properties.
    """
    SEX = (
        (0, 'MALE'),
        (1, 'FEMALE'),
        (2, 'NOT DEFINED')
    )

    user = models.OneToOneField(User)
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    sex = models.IntegerField(choices=SEX, default=2, verbose_name="Sex")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of birth")
    points = models.IntegerField(default=0, verbose_name="Points")
    rating = models.IntegerField(default=0, verbose_name="Place (rating)")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"


class Tariffs(models.Model):
    """
    Models for tarifs
    """
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    price = models.FloatField(default=0.0, verbose_name="Price")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tariff"
        verbose_name_plural = "Tariffs"
        ordering = ('price', )



class TariffsFeature(models.Model):
    """
    Models for tarifs features
    """
    title = models.TextField(verbose_name="Title")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    tariffs = models.ManyToManyField(Tariffs, verbose_name="Tariff")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tariff feature"
        verbose_name_plural = "Tariff features"


class Organizers(models.Model):
    """
    Model for define organizer properties
    """
    user = models.OneToOneField(User)
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    tariff = models.ForeignKey(Tariffs, verbose_name="Tariff")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Organizer"
        verbose_name_plural = "Organizers"


class Commands(models.Model):
    """
    Model for players commands
    """
    # TODO: complete this model
    title = models.CharField(max_length=255, verbose_name="Title")
    players = models.ManyToManyField(Players)







