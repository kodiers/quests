__author__ = 'kodiers'
from django import template
from django.contrib.auth.models import User
from web.models import Organizers, Events, QuestsUsers, Players, EventStatistics

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

