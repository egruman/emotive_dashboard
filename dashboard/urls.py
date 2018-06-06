from django.conf.urls import url, include
from django.contrib import admin

from . import views

app_name= 'dashboard'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sms/$', views.sms_response, name='sms'),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^text/$', views.text, name='text'),
    url(r'^edit(?P<msg>[0-9]+)/$', views.edit, name='edit')
]