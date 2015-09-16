from django.db import models
from django.db.models import Max
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

    def get_user_events(self):
        """
        """
        events = Events.objects.filter(organizer=self.user).order_by('start_date')
        return events

    class Meta:
        verbose_name_plural = "Quests users"
        verbose_name = "Quest user"


class Contacts(models.Model):
    """
    Model for user and organisator contacts
    """
    user = models.OneToOneField(User)
    country = models.CharField(max_length=255, null=True, blank=True, verbose_name="Country")
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name="City")
    street = models.TextField(verbose_name="Street", null=True, blank=True)
    phone = models.CharField(verbose_name="Phone number", null=True, blank=True, max_length=128)
    skype = models.CharField(max_length=255, null=True, blank=True, verbose_name="Skype")
    site = models.CharField(verbose_name="Web site", null=True, blank=True, max_length=128)

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
    show_personal_info = models.BooleanField(default=False, verbose_name="Show personal info")

    def __str__(self):
        return self.user.username

    def get_future_events(self):
        """
        Return all events, there user registered.
        """
        today = datetime.date.today()
        events = []
        all_events = Events.objects.filter(start_date__gte=today).order_by('start_date')
        user_teams = Teams.objects.filter(players=self.user)
        for event in all_events:
            if self.user in event.registered_players.all():
                events.append(event)
            for team in user_teams:
                if team in event.registered_teams.all():
                    events.append(event)
        return events

    def get_last_events(self):
        """
        Return all events, there user was registered and that completed
        """
        today = datetime.date.today()
        events = []
        all_events = Events.objects.filter(start_date__lt=today).filter(completed=True).order_by('start_date')
        user_teams = Teams.objects.filter(players=self.user)
        for event in all_events:
            if self.user in event.registered_players.all():
                events.append(event)
            for team in user_teams:
                if team in event.registered_teams.all():
                    events.append(event)
        return events

    def get_current_event(self):
        """
        Return all events, whcih started today for current player.
        """
        today = datetime.date.today()
        events = []
        all_events = Events.objects.filter(completed=False).filter(started=True).order_by('start_date')
        user_teams = Teams.objects.filter(players=self.user)
        for event in all_events:
            if self.user in event.registered_players.all():
                events.append(event)
            for team in user_teams:
                if team in event.registered_teams.all():
                    events.append(event)
        return events

    def get_user_teams(self):
        """
        Return all teams for current user.
        """
        return Teams.objects.filter(players=self.user)

    def get_user_photos(self):
        """
        Return all photos for current user.
        """
        return Photos.objects.filter(user=self.user).order_by('date')

    def add_points(self, points):
        """
        Increment user points
        """
        self.points += points
        self.save()

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
    show_on_main_page = models.BooleanField(default=False, verbose_name="Best organizer (show on main page)") # If true => show on main page

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
        events = Events.objects.filter(organizer=self.user).filter(start_date__gte=today).filter(started=False).filter(completed=False).order_by('start_date')
        return events

    def get_current_events(self):
        """
        Get current events for this organizer. Calling in template.
        """
        today = datetime.date.today()
        events = Events.objects.filter(organizer=self.user).filter(start_date=today).filter(completed=False).filter(started=True).order_by('pk')
        return events

    def get_completed_events(self):
        """
        Get completed events for this organizer. Calling in template
        """
        today = datetime.date.today()
        events = Events.objects.filter(organizer=self.user).filter(completed=True).order_by('start_date')
        return events

    def get_organizers_photo(self):
        """
        Get photo for current organizer.
        """
        return Photos.objects.filter(user=self.user).order_by('date')

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

    def add_points(self, points):
        """
        Increase team points
        """
        self.points += points
        self.save()

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"


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
    registered_players = models.ManyToManyField(User, verbose_name="Registered users", related_name="regitered_players",
                                                blank=True)
    registered_teams = models.ManyToManyField(Teams, verbose_name="Registered teams", blank=True)
    organizer = models.ForeignKey(User, verbose_name="Organizer", related_name="organizer")
    completed = models.BooleanField(default=False, verbose_name="Finished")
    duration = DurationField(verbose_name="Duration", null=True, blank=True)
    image = models.ImageField(upload_to='images', blank=True, null=True, verbose_name="Image")
    started = models.BooleanField(verbose_name="Started", default=False)
    # event_photos = models.ManyToManyField(EventsPhotos, verbose_name="Event photos")

    def image_tag(self):
        return u'<img src="%s" height=75 width=75 />' % (self.image.url)

    image_tag.short_description = "Current image"
    image_tag.allow_tags = True

    def __str__(self):
        return self.title

    def get_event_photos(self):
        """
        Return list of event photos
        """
        photos = Photos.objects.filter(event=self).order_by('date')
        return photos

    def get_event_tasks(self):
        """
        Return list of tasks in event
        """
        tasks = Tasks.objects.filter(event=self).order_by('pk')
        return tasks

    def get_event_winner(self):
        """
        Return username (if user is winner) or team.title if event for team only. Calling in template.
        """
        # statistics = EventStatistics.objects.filter(event=self).aggregate(Max('score'))
        # eventstat = EventStatistics.objects.filter(event=self).get(score=statistics['score__max'])
        # if self.is_team:
        #     team = eventstat.team.title
        #     return team
        # else:
        #     username = eventstat.player.username
        #     return username
        eventwinner = EventsWinners.objects.get(event=self)
        if self.is_team:
            return eventwinner.team.title
        else:
            return eventwinner.player.username

    def get_event_score(self):
        """
        Return max score for event. Calling in template.
        """
        statistics = EventStatistics.objects.filter(event=self).aggregate(Max('score'))
        return statistics['score__max']

    def get_registered_count(self):
        """
        Return number of registered players or teams
        """
        if self.is_team:
            return self.registered_teams.count()
        else:
            return self.registered_players.count()

    def get_event_score_by_winner(self):
        """
        Return max score for event winner.
        """
        if self.is_team:
            team = Teams.objects.get(title=self.get_event_winner())
            statistics = EventStatistics.objects.filter(event=self).filter(team=team).aggregate(Max('score'))
        else:
            user = User.objects.get(username=self.get_event_winner())
            statistics = EventStatistics.objects.filter(event=self).filter(player=user).aggregate(Max('score'))
        return statistics['score__max']


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
    answer = models.TextField(null=True, verbose_name="Answer", blank=True)
    event = models.ForeignKey(Events, verbose_name="Event")
    time = models.CharField(verbose_name="Time for task", null=True, blank=True, max_length=64)

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


class Photos(models.Model):
    """
    Model for photos.
    """
    title = models.TextField(verbose_name="Title", null=True, blank=True)
    description = models.TextField(verbose_name="Descrition", null=True, blank=True)
    date = models.DateField(verbose_name="Date", null=True, blank=True)
    event = models.ForeignKey(Events, null=True, blank=True, verbose_name="Event")
    user = models.ForeignKey(User, null=True, blank=True, verbose_name="User")
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
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

class EventStatistics(models.Model):
    """
    Model for store event's statistic
    """
    event = models.ForeignKey(Events, verbose_name="Event")
    team = models.ForeignKey(Teams, verbose_name="Team", null=True, blank=True)
    player = models.ForeignKey(User, verbose_name="Player", null=True, blank=True)
    score = models.IntegerField(verbose_name="Score", null=True, blank=True)
    time = DurationField(verbose_name="Executed time", null=True, blank=True)
    start_time = models.DateTimeField(verbose_name="Start time", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="End time", null=True, blank=True)
    completed = models.BooleanField(verbose_name="Completed for user/team", default=False)

    def __str__(self):
        if self.team != None:
            return self.team.title + ":" + self.event.title
        else:
            return self.player.username + ":" + self.event.title

    # def get_winner(self):
    #     """
    #     Get winner in event.
    #     """
    #     if self.event.is_team:


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
    time = models.IntegerField(verbose_name="Executed time", null=True, blank=True)
    start_time = models.DateTimeField(verbose_name="Start time", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="End time", null=True, blank=True)
    used_hints = models.IntegerField(default=0, verbose_name="Count of used hints")
    completed = models.BooleanField(default=False, verbose_name="Is task completed for user or team")
    started = models.BooleanField(default=False, verbose_name="Task started")
    answered = models.BooleanField(default=False, verbose_name="Task is correctly answered")
    # TODO: add fields for executed time in days, seconds, minutes, hours and add handler for this

    def __str__(self):
        if self.team != None:
            return self.team.title + ":" + self.task.title
        else:
            return self.player.username + ":" + self.task.title

    class Meta:
        verbose_name = "Task statistic"
        verbose_name_plural = "Tasks statistics"
        ordering = ('time',)


class TodayEvents(models.Model):
    """

    """
    event = models.OneToOneField(Events)
    start_time = models.DateTimeField()


class EventsWinners(models.Model):
    """

    """
    eventstat = models.OneToOneField(EventStatistics)
    player = models.ForeignKey(User, null=True, blank=True)
    team = models.ForeignKey(Teams, null=True, blank=True)
    event = models.OneToOneField(Events)





