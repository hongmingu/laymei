from django.conf.urls import url
from renoauth import views


urlpatterns = [
    url(r'test/$', views.test, name='test'),
    url(r'test2/$', views.test2, name='test2'),

    url(r'^$', views.accounts, name='accounts'),


    url(r'^email/key/send/$', views.email_key_send, name='email_key_send'),
    url(r'^email/key/confirm/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.email_key_confirm, name='email_key_confirm'),


    url(r'^login/$', views.log_in, name='log_in'),
    url(r'^logout/$', views.log_out, name='log_out'),

    url(r'^username/change/$', views.username_change, name='username_change'),

    url(r'^password/change/$', views.password_change, name='password_change'),
    url(r'^password/reset/$', views.password_reset, name='password_reset'),

    url(r'^email/add/$', views.email_add, name='email_add'),
]
'''
    url(r'^create/$', views.main_create_log_in, name='create'),
'''