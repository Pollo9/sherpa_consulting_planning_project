from django.conf.urls import url
from . import views

urlpatterns = [
	    url(r'^$', views.index, name='index'),
	    url(r'^messagerie/$', views.messagerie, name='messagerie'),
	    url(r'^messagerie/(?P<username>[\w+.@-]+)&(?P<all>[01])/$', views.message, name='message'),
	    url(r'^planning/', views.planning, name='planning'),
	    url(r'^missions/$', views.missions, name='missions'),
	    url(r'^ajouter_missions/$', views.add_missions, name='ajouter_missions'),
		url(r'^modifier_missions/(?P<id_mission>[0-9]+)$', views.edit_missions, name='modifier_missions'),
	    url(r'^client/$', views.clients, name='clients'),
	    url(r'^ajouter_client/$', views.add_clients, name='ajouter_client'),
	    url(r'^modifier_client/(?P<id_client>[0-9]+)$', views.edit_clients, name='modifier_client'),
	    url(r'^consultant/$', views.consultants, name='consultants'),
	    url(r'^ajouter_consultant/$', views.add_consultants, name='ajouter_consultants'),
	    url(r'^modifier_consultant/(?P<id_consultant>[0-9]+)$', views.edit_consultants, name='modifier_consultants'),
	]