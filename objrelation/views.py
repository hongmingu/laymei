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
            clue = None
            get_reaction_status = None

            try:
                get_reaction_status = request.POST['reaction_status']
            except KeyError:
                clue['success'] = False
                clue['message'] = texts.REACTION_NO_POST_STATUS
                return JsonResponse({'clue': clue})

            try:
                message_pk = request.POST['message_pk']
            except KeyError:
                clue['success'] = False
                clue['message'] = texts.REACTION_NO_MESSAGE_PK
                return JsonResponse({'clue': clue})

            user_extension = request.user.userextension
            if user_extension is None:
                clue['success'] = False
                clue['message'] = texts.BAD_ACCESS
                return JsonResponse({'clue': clue})

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
                    clue['message'] = texts.REACTION_REMOVE_SUCCESSFULLY
                    return JsonResponse({'clue': clue})
                else:
                    message_react.status = get_reaction_status
                    message_react.save()
                    clue['success'] = True
                    clue['message'] = texts.REACTION_CHANGED_SUCCESSFULLY
                    return JsonResponse({'clue': clue})

            else:
                message_react_create = MessageReact.objects.create(user_extension=user_extension, message_id=message_pk,
                                                                   status=get_reaction_status)
                if message_react_create is not None:
                    clue['success'] = True
                    clue['message'] = texts.REACTION_CREATED_SUCCESSFULLY
                    return JsonResponse({'clue': clue})
                else:
                    clue['success'] = False
                    clue['message'] = texts.REACTION_CREATE_FAILED
                    return JsonResponse({'clue': clue})

@is_authenticated
def share(request):
    if request.method == "POST":
        clue = None
        message_shared_pk = None
        form = ShareForm(request.POST)


        # share버튼클릭 -> 버튼에 a태그로 /share/number=dlskfjwel/ 여기로 href걸고, 여기서 다른 뷰에서 get 요청시 아규먼트
        # 확인하고 가능한 경우인지 확인해서 render해줘야한다. 그다음 여기서 post 요청시 주소값에서 shared_pk 받고 form 에
        # form 데이터로 넘겨서 처리한 후 absolute url 로 redirect 해라
        # 바모울에서 comment 는 그 주소에서 id 받아서 쓰고 다시 렌더해주면 됨.
        try:
            message_shared_pk = request.POST['message_shared_pk']
        except KeyError:
            clue['success'] = False
            clue['message'] = texts.SHARED_PK_NOT_EXIST
            return JsonResponse({'clue': clue})

        message_text = request.POST['message_text']
        message_content = request.POST['message_content']



