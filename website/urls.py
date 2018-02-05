from django.conf.urls import url
from renoauth import views


urlpatterns = [
    url(r'^$', views.main_create_log_in, name='main'),
]
