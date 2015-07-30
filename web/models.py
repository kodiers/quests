from django.db import models
from django.contrib.auth.models import User

import datetime

from durationfield.db.models.fields.duration import DurationField

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
    tariff = models.ForeignKey(Tariffs, verbose_name="Tariff", null=True, blank=True)
    show_on_main_page = models.BooleanField(default=False, verbose_name="Best organizer (show on main page)") # If tru => show on main page

    def __str__(self):
        return self.user.username

    def get_three_future_events(self):
        """
        Get three future events for organizer. Calling in template.
        """
        today = datetime.date.today()
        events = Events.objects.filter(organizer=self.user).filter(start_date__gte=today).order_by('start_date')[:3]
        return events

    def get_future_events(self):
        """
        Get all future events for organizer. Calling in template.
        """
        today = datetime.date.today()
        events = Events.objects.filter(organizer=self.user).filter(start_date__gte=today).order_by('start_date')
        return events

    class Meta:
        verbose_name = "Organizer"
        verbose_name_plural = "Organizers"


class Teams(models.Model):
    """
    Model for players teams
    """
    title = models.CharField(max_length=255, verbose_name="Title")
    creator = models.OneToOneField(User, null=True, blank=True, verbose_name='Creator')
    players = models.ManyToManyField(User, related_name='team_players', verbose_name='Players')
    points = models.IntegerField(verbose_name="Total points", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"


class Messages(models.Model):
    """
    Model for user messages
    """
    text = models.TextField(verbose_name="Text")
    from_user = models.ForeignKey(User, verbose_name="From", related_name='from_user')
    to_user = models.ForeignKey(User, verbose_name="To", related_name='to_user')
    date = models.DateTimeField(verbose_name="Date")

    def __str__(self):
        return self.from_user.username + " to " + self.to_user.username

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ('date',)


class EventsPlaces(models.Model):
    """
    Store events and tasks places
    """
    country = models.CharField(max_length=255, null=True, blank=True, verbose_name="Country")
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name="City")
    street = models.TextField(verbose_name="Street", null=True, blank=True)
    lat = models.FloatField(verbose_name="Latitude", null=True, blank=True)
    lon = models.FloatField(verbose_name="Longtitude", null=True, blank=True)
    map_link = models.TextField(verbose_name="Link to map", null=True, blank=True)

    class Meta:
        verbose_name = "Event and task place"
        verbose_name_plural = "Event and task places"


class EventsPhotos(models.Model):
    """
    Model for events photos.
    """
    title = models.TextField(verbose_name="Title", null=True, blank=True)
    description = models.TextField(verbose_name="Descrition", null=True, blank=True)
    date = models.DateField(verbose_name="Date", null=True, blank=True)
    image = models.ImageField(upload_to='images')

    def image_tag(self):
        return u'<img src="%s" height=75 width=75 />' % (self.image.url)

    image_tag.short_description = "Current image"
    image_tag.allow_tags = True

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "Image"

    class Meta:
        verbose_name = "Event photo"
        verbose_name_plural = "Event photos"


class Events(models.Model):
    """
    Model for events.
    If is_team == True, then the this events for teams only.
    If completed == True, then this event is finished
    """
    title = models.TextField(verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    map_link = models.TextField(verbose_name="Link to map", null=True, blank=True)
    place = models.ForeignKey(EventsPlaces, verbose_name="Place", null=True, blank=True)
    is_team = models.BooleanField(default=False, verbose_name="Team only")
    price = models.FloatField(verbose_name="Price", default=0.0)
    max_players = models.IntegerField(verbose_name="Limit players", null=True, blank=True)
    start_date = models.DateTimeField(verbose_name="Start date")
    end_date = models.DateTimeField(verbose_name="End date")
    registered_players = models.ManyToManyField(User, verbose_name="Registered users",
                                                related_name="regitered_players", null=True,
                                                blank=True)
    registered_teams = models.ManyToManyField(Teams, verbose_name="Registered teams", null=True,
                                              blank=True)
    organizer = models.ForeignKey(User, verbose_name="Organizer", related_name="organizer")
    completed = models.BooleanField(default=False, verbose_name="Finished")
    duration = DurationField(verbose_name="Duration", null=True, blank=True)
    image = models.ImageField(upload_to='images', blank=True, null=True, verbose_name="Image")
    event_photos = models.ManyToManyField(EventsPhotos, verbose_name="Event photos", null=True, blank=True)

    def image_tag(self):
        return u'<img src="%s" height=75 width=75 />' % (self.image.url)

    image_tag.short_description = "Current image"
    image_tag.allow_tags = True

    def __str__(self):
        return self.title

    # def get_event_photos(self):
    #     """
    #     Return list of event photos
    #     """
    #     photos =

    def get_event_tasks(self):
        """
        Return list of tasks in event
        """
        tasks = Tasks.objects.filter(event=self).order_by('pk')
        return tasks

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ('start_date',)


class Tasks(models.Model):
    """
    Model for event's tasks
    """
    title = models.TextField(verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    map_link = models.TextField(verbose_name="Link to map", null=True, blank=True)
    place = models.ForeignKey(EventsPlaces, verbose_name="Place", null=True, blank=True)
    score = models.IntegerField(verbose_name="Score", default=0)
    answer = models.TextField(null=True, verbose_name="Answer")
    event = models.ForeignKey(Events, verbose_name="Event")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Hints(models.Model):
    """
    Model for task's hint
    """
    text = models.TextField(verbose_name="Text")
    price = models.FloatField(verbose_name="Price", default=0.0)
    task = models.OneToOneField(Tasks)

    def __str__(self):
        return self.task.title

    class Meta:
        verbose_name_plural = "Hints"
        verbose_name = "Hint"


class EventStatistics(models.Model):
    """
    Model for store event's statistic
    """
    event = models.ForeignKey(Events, verbose_name="Event")
    team = models.ForeignKey(Teams, verbose_name="Team", null=True, blank=True)
    player = models.ForeignKey(User, verbose_name="Player", null=True, blank=True)
    score = models.IntegerField(verbose_name="Score", null=True, blank=True)
    time = DurationField(verbose_name="Executed time", null=True, blank=True)

    def __str__(self):
        if self.team != None:
            return self.team.title + ":" + self.event.title
        else:
            return self.player.username + ":" + self.event.title

    class Meta:
        verbose_name = "Event statistic"
        verbose_name_plural = "Events statistics"
        ordering = ('time',)


class TaskStatistics(models.Model):
    """
    Model for store task's statistic.
    """
    task = models.ForeignKey(Tasks, verbose_name="Task")
    team = models.ForeignKey(Teams, verbose_name="Team", null=True, blank=True)
    player = models.ForeignKey(User, verbose_name="Player", null=True, blank=True)
    score = models.IntegerField(verbose_name="Score", null=True, blank=True)
    time = DurationField(verbose_name="Executed time", null=True, blank=True)
    used_hints = models.IntegerField(default=0, verbose_name="Count of used hints")

    def __str__(self):
        if self.team != None:
            return self.team.title + ":" + self.task.title
        else:
            return self.player.username + ":" + self.task.title

    class Meta:
        verbose_name = "Task statistic"
        verbose_name_plural = "Tasks statistics"
        ordering = ('time',)








