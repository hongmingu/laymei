from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from renoauth.models import *


@python_2_unicode_compatible
class Message(models.Model):
    dump_text = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    _from = models.ForeignKey(UserExtension)
    public = models.BooleanField(default=False)
    recipients_list = models.BooleanField(default=False)
    open = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.public is True:
            if self.has_list is False:
                to = 'all'
            else:
                to = 'impossible'
        else:
            if self.has_list is False:
                to = 'friends'
            else:
                to = 'recipients'
        return "from: %s //to: %s //text : %s" % (self._from.usersubusername.username,
                                                  to, self.dump_text)


@python_2_unicode_compatible
class MessageRecipientsList(models.Model):
    dump_text = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "dump_text: %s" % self.dump_text


