from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.db.models import Q
from twilio.rest import Client
from django_twilio.decorators import twilio_view
from .models import *
from planning.models import Bdd_messages, Bdd_user_django

def index(request):
	context = locals()
	template = "index.html"
	return render(request,template,context)


def messagerie(request):
	consultants = Bdd_user_django.objects.filter(user_django__id__isnull=False)

	notif = {}
	for c in consultants:
		print(c.id)
		msg = Bdd_messages.objects.filter(envoyeur__id = c.id).order_by('-date')[:10][::-1]
		compteur = 0
		for m in msg:
			if not m.lu:
				compteur += 1
		notif[c.id] = compteur

	msg = None
	consultant_selectionne = None

	context = locals()
	template = "messagerie.html"
	return render(request,template,context)


def messages(request, id, nom, all):
	see_all = int(all)
	consultants = Bdd_user_django.objects.filter(user_django__id__isnull=False)

	try:
	    consultant_selectionne = Bdd_user_django.objects.get(id = id, nom = nom)
	except SomeModel.DoesNotExist:
	    consultant_selectionne = None

	if request.POST.get('message-envoyer'):
		if request.POST.get('message-texte') != '':
			account_sid = settings.TWILIO_ACCOUNT_SID
			auth_token = settings.TWILIO_AUTH_TOKEN
			client = Client(account_sid, auth_token)

			message = client.messages \
			                .create(
			                     body = request.POST.get('message-texte'),
			                     from_ = settings.TWILIO_NUMBER,
			                     to = consultant_selectionne.user_django.telephone
			                 )

			m = Bdd_messages()
			e = Bdd_user_django.objects.get(nom = 'Consulting', prenom = 'Sherpa')
			r = consultant_selectionne

			m.message = request.POST.get('message-texte')
			m.envoyeur = e
			m.receveur = r
			m.lu = True
			m.save()

	if consultant_selectionne:
		msg_count = Bdd_messages.objects.filter(Q(envoyeur__id = consultant_selectionne.id)|Q(receveur__id = consultant_selectionne.id)).count()
		if see_all == 1:
			msg = Bdd_messages.objects.filter(Q(envoyeur__id = consultant_selectionne.id)|Q(receveur__id = consultant_selectionne.id))
		else:
			msg = Bdd_messages.objects.filter(Q(envoyeur__id = consultant_selectionne.id)|Q(receveur__id = consultant_selectionne.id)).order_by('-date')[:10][::-1]
		for m in msg:
			m.lu = True
			m.save()
	else:
		msg = None

	notif = {}
	for c in consultants:
		msg_notif = Bdd_messages.objects.filter(envoyeur__id = c.id).order_by('-date')[:10][::-1]
		compteur = 0
		for m in msg_notif:
			if not m.lu:
				compteur += 1
		notif[c.id] = compteur

	context = locals()
	template = "messagerie.html"
	return render(request,template,context)


@twilio_view
def sms(request):
	m = Bdd_messages()
	r = Bdd_user_django.objects.get(user_django__telephone = request.POST.get('To'))
	e = Bdd_user_django.objects.get(user_django__telephone = request.POST.get('From'))
	
	m.message = request.POST.get('Body')
	m.envoyeur = e
	m.receveur = r
	m.save()



def planning(request):
	consultants = Bdd_consultants.objects.all()
	missions = Bdd_missions.objects.all()
	formateurs = Bdd_formateurs.objects.all()

	context = locals()
	template = "planning.html"
	return render(request,template,context)