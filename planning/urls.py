from django.conf.urls import url
from . import views

urlpatterns = [
	    url(r'^$', views.index, name='index'),
	    url(r'^messagerie/', views.messagerie, name='messagerie'),
	    url(r'^planning/', views.planning, name='planning'),
	]