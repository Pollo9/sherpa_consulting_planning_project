from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import *

def index(request):
	context = locals()
	template = "index.html"
	return render(request,template,context)

def messagerie(request):
	context = locals()
	template = "messagerie.html"
	return render(request,template,context)

def planning(request):
	formateurs = Bdd_formateurs.objects.all()
	missions = Bdd_missions.objects.all()

	context = locals()
	template = "planning.html"
	return render(request,template,context)

