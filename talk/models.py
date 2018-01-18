from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from renoauth.models import *
from message.models import *


@python_2_unicode_compatible
class TalkExtension(models.Model):
    dump_text = models.CharField(max_length=10)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(UserExtension)


@python_2_unicode_compatible
class TalkRoom(models.Model):
    talk_extension = models.ForeignKey(TalkExtension)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    _with = models.ForeignKey(UserExtension)


@python_2_unicode_compatible
class TalkClose(models.Model):
    talk_room = models.OneToOneField(TalkRoom)


@python_2_unicode_compatible
class Talk(models.Model):
    message = models.ForeignKey(Message, null=True, blank=True)
    dump_text = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    talk_room = models.ForeignKey(TalkRoom)
    _from = models.ForeignKey(UserExtension)

    def __str__(self):
        if self.public is True:
            if self.whole is True:
                to = 'all'
            else:
                to = 'impossible'
        else:
            if self.whole is True:
                to = 'friends'
            else:
                to = 'recipients'
        return "from: %s //to: %s //text : %s" % (self._from.usersubusername.username,
                                                  to, self.dump_text)
