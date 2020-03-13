from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.db.models import Q
from twilio.rest import Client
from django_twilio.decorators import twilio_view
from .models import *
from planning.models import Bdd_messages, Bdd_user_django
from .forms import *

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

from compte.models import *

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


# @login_required
def planning(request):
	# if not(request.user.groups.filter(name__in=["Admi"]).exists()):
	# 	return HttpResponseRedirect('/messagerie')

	# all_user = User.objects.all()

	# current_user = User.objects.create_user('test','test@gmail.com','azertyuiop')
	# current_user.profile.telephone = "test"
	# current_user.save()

	# moi = request.user
	
	# group = Group.objects.get(name="Formateur")
	# moi.groups.add(group)
	# moi.save()
	adresses = Bdd_adresse_client.objects.all()
	clients = Bdd_client.objects.all()
	consultants = Bdd_consultants.objects.all()
	missions = Bdd_missions.objects.all()
	if(request.method == 'POST' and 'ajouter_mission' in request.POST):
		form = ajouter_missionForm(request.POST, request.FILES)
		if form.is_valid():
			
			ajouter_obj = form.save(commit="false")
			ajouter_obj.date_debut = request.POST.get('date_debut', '')
			ajouter_obj.date_fin = request.POST.get('date_fin', '')
			ajouter_obj.status = request.POST.get('status', '')

			ajouter_obj.save()
		return HttpResponseRedirect('/planning')

	if(request.method == 'POST' and 'modifier_mission' in request.POST):
		form = ajouter_missionForm(request.POST, request.FILES)
		print(request.POST.get('id'))
		mission = Bdd_missions.objects.get(id = request.POST.get('id'))
		mission.date_debut = request.POST.get('date-debut')
		mission.date_fin = request.POST.get('date-fin')
		mission.client = Bdd_client.objects.get(id = request.POST.get('client'))
		mission.adresse = Bdd_adresse_client.objects.get(id = request.POST.get('adresse'))
		if request.POST["visible_consultants"]:
			mission.visible_consultant = True;
		else:
			mission.visible_consultant = False;
			
		mission.save()
		return HttpResponseRedirect('/planning')
			

	context = locals()
	template = "planning.html"
	return render(request,template,context)

def missions(request, id=0):
	clients = Bdd_client.objects.all()
	adresses = Bdd_adresse_client.objects.all()
	consultants = Bdd_consultants.objects.all()
	missions = Bdd_missions.objects.all()

	if request.POST.get('mission-envoyer'):
		m = Bdd_missions()
		m.date_debut = request.POST.get('date-debut')
		m.date_fin = request.POST.get('date-fin')
		m.client = Bdd_client.objects.get(id = request.POST.get('client'))
		m.adresse = Bdd_adresse_client.objects.get(id = request.POST.get('adresse'))
		if request.POST.get('visible') == 'oui':
			m.visible_consultant = True
		else:
			m.visible_consultant = False
		if request.POST.get('consultant') != "":
			m.consultant = Bdd_consultants.objects.get(id = request.POST.get('consultant'))
			m.status = "E"
		else:
			m.status = "A"
		m.save()

	if int(id) != 0:
		mission_selectionnee = Bdd_missions.objects.get(id = int(id))
	else:
		mission_selectionnee = None

	if request.POST.get('mission-modifier'):
		m = Bdd_missions.objects.get(id = request.POST.get('id'))
		m.date_debut = request.POST.get('date-debut')
		m.date_fin = request.POST.get('date-fin')
		m.client = Bdd_client.objects.get(id = request.POST.get('client'))
		m.adresse = Bdd_adresse_client.objects.get(id = request.POST.get('adresse'))
		if request.POST.get('visible') == 'oui':
			m.visible_consultant = True
		else:
			m.visible_consultant = False
		if request.POST.get('consultant') != "":
			m.consultant = Bdd_consultants.objects.get(id = request.POST.get('consultant'))
			m.status = "E"
		else:
			m.consultant = None
			m.status = "A"
		m.save()
		mission_selectionnee = None

	nb_missions = missions.count()
	nb_missions_attribuer = Bdd_missions.objects.filter(status = "A").count()
	nb_missions_attente = Bdd_missions.objects.filter(status = "E").count()
	nb_missions_historique = Bdd_missions.objects.filter(status = "H").count()

	context = locals()
	template = "missions.html"
	return render(request,template,context)


def clients(request, id=0, adresse=0):
	clients = Bdd_client.objects.all()
	mission_types = Bdd_mission_type_client.objects.all()
	adresses = Bdd_adresse_client.objects.all()

	if request.POST.get('client-envoyer'):
		c = Bdd_client()
		c.nom = request.POST.get('nom')
		c.code_couleur = request.POST.get('code-couleur')
		c.save()
		c.mission_type.add(Bdd_mission_type_client.objects.get(id = request.POST.get('mission-type')))
		if request.POST.get('archive') == 'oui':
			c.archive = True
		else:
			c.archive = False
		c.save()

	if int(id) != 0:
		client_selectionnee = Bdd_client.objects.get(id = int(id))
	else:
		client_selectionnee = None

	if request.POST.get('client-modifier'):
		c = Bdd_client.objects.get(id = request.POST.get('id'))
		c.nom = request.POST.get('nom')
		c.code_couleur = request.POST.get('code-couleur')
		c.mission_type.add(Bdd_mission_type_client.objects.get(id = request.POST.get('mission-type')))
		if request.POST.get('archive') == 'oui':
			c.archive = True
		else:
			c.archive = False
		c.save()
		client_selectionnee = None

	if request.POST.get('adresse-envoyer'):
		a = Bdd_adresse_client()
		a.nom = request.POST.get('nom')
		a.adresse = request.POST.get('adresse')
		a.code_postal = request.POST.get('code-postal')
		a.ville = request.POST.get('ville')
		a.client = Bdd_client.objects.get(id = request.POST.get('client'))
		a.save()

	if int(adresse) != 0:
		adresse_selectionnee = Bdd_adresse_client.objects.get(id = int(adresse))
	else:
		adresse_selectionnee = None

	if request.POST.get('adresse-modifier'):
		a = Bdd_adresse_client.objects.get(id = request.POST.get('id'))
		a.nom = request.POST.get('nom')
		a.adresse = request.POST.get('adresse')
		a.code_postal = request.POST.get('code-postal')
		a.ville = request.POST.get('ville')
		a.client = Bdd_client.objects.get(id = request.POST.get('client'))
		a.save()
		adresse_selectionnee = None

	nb_clients = clients.count()
	nb_clients_actifs = Bdd_client.objects.filter(archive = False).count()
	nb_clients_archives = Bdd_client.objects.filter(archive = True).count()
	nb_adresses = adresses.count()

	context = locals()
	template = "client.html"
	return render(request,template,context)


def consultants(request, id=0):
	user_django = Bdd_user_django.objects.all()
	consultants = Bdd_consultants.objects.all()
	themes = Bdd_theme.objects.all()

	if request.POST.get('consultant-envoyer'):
		c = Bdd_consultants()
		c.user_django = Bdd_user_django.objects.get(id = request.POST.get('user'))
		c.diminutif = c.user_django.prenom[0]+c.user_django.nom[0]
		c.telephone = request.POST.get('telephone')
		c.adresse = request.POST.get('adresse')
		if request.POST.get('permission') == 'oui':
			c.permission = True
		else:
			c.permission = False
		if request.POST.get('archive') == 'oui':
			c.archive = True
		else:
			c.archive = False
		c.save()
		c.theme_junior.add(Bdd_theme.objects.get(id = request.POST.get('junior')))
		c.theme_confirme.add(Bdd_theme.objects.get(id = request.POST.get('confirme')))
		c.theme_senior.add(Bdd_theme.objects.get(id = request.POST.get('senior')))
		c.save()

	if int(id) != 0:
		consultant_selectionnee = Bdd_consultants.objects.get(id = int(id))
	else:
		consultant_selectionnee = None

	if request.POST.get('consultant-modifier'):
		c = Bdd_consultants.objects.get(id = request.POST.get('id'))
		c.user_django = Bdd_user_django.objects.get(id = request.POST.get('user'))
		c.diminutif = c.user_django.prenom[0]+c.user_django.nom[0]
		c.telephone = request.POST.get('telephone')
		c.adresse = request.POST.get('adresse')
		if request.POST.get('permission') == 'oui':
			c.permission = True
		else:
			c.permission = False
		if request.POST.get('archive') == 'oui':
			c.archive = True
		else:
			c.archive = False
		c.theme_junior.add(Bdd_theme.objects.get(id = request.POST.get('junior')))
		c.theme_confirme.add(Bdd_theme.objects.get(id = request.POST.get('confirme')))
		c.theme_senior.add(Bdd_theme.objects.get(id = request.POST.get('senior')))
		c.save()
		consultant_selectionnee = None

	nb_consultants = consultants.count()
	nb_consultants_actif = Bdd_consultants.objects.filter(archive = False).count()
	nb_consultants_archive = Bdd_consultants.objects.filter(archive = True).count()

	context = locals()
	template = "consultant.html"
	return render(request,template,context)