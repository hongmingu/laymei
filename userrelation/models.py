from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from renoauth.models import *


@python_2_unicode_compatible
class FriendOffer(models.Model):
    _from = models.ForeignKey(UserExtension, related_name='friend_from')
    _to = models.ForeignKey(UserExtension, related_name='friend_to')
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return "from %s to %s" % (self._from.usersubusername.username, self._to.usersubusername.username)

    class Meta:
        unique_together = ('_to', '_from',)


@python_2_unicode_compatible
class FriendsList(models.Model):
    user_extension = models.OneToOneField(UserExtension)


@python_2_unicode_compatible
class FollowingList(models.Model):
    user_extension = models.OneToOneField(UserExtension)


@python_2_unicode_compatible
class FollowerList(models.Model):
    user_extension = models.OneToOneField(UserExtension)


@python_2_unicode_compatible
class Block(models.Model):
    _from = models.ForeignKey(UserExtension, related_name='block_from')
    _from = models.ForeignKey(UserExtension, related_name='block_from')
    _to = models.ForeignKey(UserExtension, related_name='block_to')

    def __str__(self):
        return "from %s to %s" % (self._from.usersubusername.username, self._to.usersubusername.username)

    class Meta:
        unique_together = ('_to', '_from',)
