from django.conf.urls import url
from . import views

urlpatterns = [
	    url(r'^$', views.index, name='index'),
	    url(r'^messagerie/$', views.messagerie, name='messagerie'),
	    url(r'^messagerie/(?P<id>[0-9]+)-(?P<nom>[\w-]+)-(?P<all>[01])/$', views.messages, name='messages'),
	    url(r'^sms/$', views.sms),
	    url(r'^planning/', views.planning, name='planning'),
	    url(r'^missions/$', views.missions, name='missions'),
	    url(r'^missions/(?P<id>[0-9]+)$', views.missions, name='missions'),
	    url(r'^client/$', views.clients, name='clients'),
	    url(r'^client/(?P<id>[0-9]+)-(?P<adresse>[0-9]+)$', views.clients, name='clients'),
	    url(r'^consultant/$', views.consultants, name='consultants'),
	    url(r'^consultant/(?P<id>[0-9]+)$', views.consultants, name='consultants'),
	]