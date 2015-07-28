__author__ = 'kodiers'
from django import template
from django.contrib.auth.models import User
from web.models import Organizers, Events, QuestsUsers, Players

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

