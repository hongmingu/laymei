from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import EmailMessage
import re
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import now, timedelta
import json
from renoauth import texts
from renoauth import banned
from renoauth import options
from renoauth import status
import urllib
from urllib.parse import urlparse
import ssl
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.db.models import Q
# Create your models here.


def reaction(request):
    if request.method == "POST":
        if request.is_ajax():
            get_reaction_status = request.POST['reaction_status']
            message_pk = request.POST['message_pk']
            user_extension = request.user.userextension
            message_react = None
            clue = None

            try:
                message_react = MessageReact.objects.get(Q(message_id=message_pk), Q(user_extension=user_extension))
            except MessageReact.DoesNotExist:
                pass

            if message_react is not None:

                if get_reaction_status == message_react.status:
                    message_react.status = 0
                    message_react.save()
                    clue['success'] = True
                    clue['message'] = text.REMOVE_REACTION_SUCCESSFULLY
                    return JsonResponse({'clue': clue})
                else:
                    message_react.status = get_reaction_status
                    message_react.save()
                    clue['success'] = True
                    clue['message'] = text.CHANGED_REACTION_SUCCESSFULLY
                    return JsonResponse({'clue': clue})

            else:
                MessageReact.objects.create(user_extension=user_extension, message_id=message_pk,
                                            status=get_reaction_status)
                clue['success'] = True
                clue['message'] = text.CREATED_REACTION_SUCCESSFULLY
                return JsonResponse({'clue': clue})


def share(request):
    