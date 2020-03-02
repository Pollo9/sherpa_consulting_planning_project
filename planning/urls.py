from django.conf.urls import url
from . import views

urlpatterns = [
	    url(r'^$', views.index, name='index'),
	    url(r'^messagerie/$', views.messagerie, name='messagerie'),
	    url(r'^messagerie/(?P<id>[0-9]+)-(?P<nom>[\w-]+)-(?P<all>[01])/$', views.messages, name='messages'),
	    url(r'^sms/$', views.sms),
	    url(r'^planning/', views.planning, name='planning'),
	]