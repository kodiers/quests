__author__ = 'kodiers'
from django import template
from django.contrib.auth.models import User
from web.models import Organizers, Events, QuestsUsers, Players, EventStatistics, Tasks, TaskStatistics

register = template.Library()

@register.filter()
def get_player_score(username):
    """
    Return score for user.
    :param username: username
    :return: score
    """
    user = User.objects.get(username=username)
    player = Players.objects.get(user=user)
    return player.points


@register.filter()
def check_user_in_registered_team(username, event_pk):
    """
    Check^ uf user in team, that are already registered to event.
    :param username: username
    :param event_pk: pk of event
    :return: Boolean
    """
    event = Events.objects.get(pk=event_pk)
    user = User.objects.get(username=username)
    registered = False
    for team in event.registered_teams.all():
        if user in team.players.all():
            registered = True
    return registered


@register.filter()
def get_score_for_event_by_user(username, event):
    """
    Return EventStatistics object for event for user:
    :param username: username of user
    :param event: event object
    :return: List of event statistics objects
    """
    user = User.objects.get(username=username)
    player = Players.objects.get(user=user)
    stat = EventStatistics.objects.filter(event=event).get(player=user)
    return stat.score


@register.filter()
def get_organizer_by_username(username):
    """
    Get organizer by username and retur organizer pk.
    :param username: username of user
    :return: organizer.pk
    """
    user = User.objects.get(username=username)
    organizer = Organizers.objects.get(user=user)
    return organizer.pk


@register.filter()
def add_class_to_formfield(field, css):
    """
    """
    return field.as_widget(attrs={"class": css})


@register.filter()
def get_player_by_username(username):
    """
    Get player by username and return player pk.
    :param username: username of user
    :return: player.pk
    """
    user = User.objects.get(username=username)
    player = Players.objects.get(user=user)
    return player.pk


@register.filter()
def get_user_team_by_event(username, event_id):
    """
    """
    user = User.objects.get(username=username)
    event = Events.objects.get(pk=event_id)
    if event.is_team:
        for team in event.registered_teams.all():
            if user in team.players.all():
                return team.title


@register.assignment_tag()
def get_taskstat_for_task(username, task_id):
    """
    """
    # username = context['user']
    global task_stat
    task = Tasks.objects.get(pk=task_id)
    user = User.objects.get(username=username)
    user_team = None
    if task.event.is_team:
        for team in task.event.registered_teams.all():
            if user in team.players.all():
                user_team = team
        if user_team:
            try:
                task_stat = TaskStatistics.objects.filter(task=task).get(team=user_team)
            except TaskStatistics.DoesNotExist:
                task_stat = None
    else:
        try:
           task_stat = TaskStatistics.objects.filter(task=task).get(player=user)
        except TaskStatistics.DoesNotExist:
            task_stat = None
    return task_stat



# @register.filter()
# def if_user_is_organizer(username):
#     """
#     Check, then user if organizer. If yes => return true.
#     :param username: username of user
#     :return: Boolean
#     """
#     user = User.objects.get(username=username)
#     if Organizers.objects.filter(user=user).exists():
#         return True
#     else:
#         return False