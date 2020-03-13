from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.db.models import Q
from twilio.rest import Client
from django_twilio.decorators import twilio_view
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *


@login_required
def index(request):
	admin = False
	if request.user.groups.filter(name__in=["Admin"]).exists():
		admin = True
	else:
		if request.user.user_django.archive:
			return HttpResponseRedirect('/login')
	context = locals()
	template = "index.html"
	return render(request,template,context)

# @login_required
def planning(request):
	admin = False
	if request.user.groups.filter(name__in=["Admin"]).exists():
		admin = True
	else:
		if request.user.user_django.archive:
			return HttpResponseRedirect('/login')
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


@login_required
def messagerie(request):
	admin = False
	if request.user.groups.filter(name__in=["Admin"]).exists():
		admin = True
	else:
		if request.user.user_django.archive:
			return HttpResponseRedirect('/login')			

	if admin:
		consultants = User.objects.filter(Q(groups__name__in=['Consultant'])&Q(user_django__archive=False))
	else:
		consultants = User.objects.filter(groups__name__in=['Admin'])

	notif = {}
	for c in consultants:
		msg = Bdd_messages.objects.filter(envoyeur__username = c.username).order_by('-date')[:10][::-1]
		compteur = 0
		for m in msg:
			if not m.lu:
				compteur += 1
		notif[c.username] = compteur

	msg = None
	consultant_selectionne = None

	context = locals()
	template = "messagerie.html"
	return render(request,template,context)


@login_required
def message(request, username, all):
	admin = False
	if request.user.groups.filter(name__in=["Admin"]).exists():
		admin = True
	else:
		if request.user.user_django.archive:
			return HttpResponseRedirect('/login')

	see_all = int(all)
	if admin:
		consultants = User.objects.filter(Q(groups__name__in=['Consultant'])&Q(user_django__archive=False))
	else:
		consultants = User.objects.filter(groups__name__in=['Admin'])

	try:
	    consultant_selectionne = User.objects.get(username = username)
	except SomeModel.DoesNotExist:
	    consultant_selectionne = None

	if request.POST.get('message-envoyer'):
		if request.POST.get('message-texte') != '':
			account_sid = settings.TWILIO_ACCOUNT_SID
			auth_token = settings.TWILIO_AUTH_TOKEN
			client = Client(account_sid, auth_token)

			if admin:
				message = client.messages \
				                .create(
				                     body = request.POST.get('message-texte'),
				                     from_ = settings.TWILIO_NUMBER,
				                     to = consultant_selectionne.user_django.telephone
				                 )
			else:
				message = client.messages \
				                .create(
				                     body = request.POST.get('message-texte'),
				                     from_ = request.user.user_django.telephone,
				                     to = settings.TWILIO_NUMBER
				                 )

			m = Bdd_messages()
			e = request.user
			r = consultant_selectionne

			m.message = request.POST.get('message-texte')
			m.envoyeur = e
			m.receveur = r
			m.lu = False
			m.save()

	if consultant_selectionne:
		msg_count = Bdd_messages.objects.filter(Q(envoyeur__username = consultant_selectionne.username)|Q(receveur__username = consultant_selectionne.username)).count()
		if see_all == 1:
			msg = Bdd_messages.objects.filter(Q(envoyeur__username = consultant_selectionne.username)|Q(receveur__username = consultant_selectionne.username))
		else:
			msg = Bdd_messages.objects.filter(Q(envoyeur__username = consultant_selectionne.username)|Q(receveur__username = consultant_selectionne.username)).order_by('-date')[:10][::-1]
		for m in msg:
			if m.envoyeur.username == consultant_selectionne.username:
				m.lu = True
				m.save()
	else:
		msg = None

	notif = {}
	for c in consultants:
		msg_notif = Bdd_messages.objects.filter(envoyeur__username = c.username).order_by('-date')[:10][::-1]
		compteur = 0
		for m in msg_notif:
			if not m.lu:
				compteur += 1
		notif[c.username] = compteur

	context = locals()
	template = "messagerie.html"
	return render(request,template,context)


@twilio_view
def sms(request):
	m = Bdd_messages()
	r = User.objects.get(user_django__telephone = request.POST.get('To'))
	e = User.objects.get(user_django__telephone = request.POST.get('From'))
	
	m.message = request.POST.get('Body')
	m.envoyeur = e
	m.receveur = r
	m.save()



####################
##### Missions #####
####################


@login_required
def missions(request):
	if not(request.user.groups.filter(name__in=["Admin"]).exists()):
		return HttpResponseRedirect('/login')
	else:
		admin = True

	if request.POST.get('action_missions') == "supp_element":
		mission_selectionnee = request.POST.getlist('selection_missions')
		for id_mission in mission_selectionnee:
			m = Bdd_missions.objects.get(id = id_mission)
			m.delete()
		nb_missions_supp = str(len(mission_selectionnee))
		if nb_missions_supp == '0':
			messages.warning(request, 'Des éléments doivent être sélectionnés afin d\'appliquer les actions. Aucun élément n\'a été modifié.')
		elif nb_missions_supp == '1':
			messages.success(request, 'La suppression d\'une mission a réussi.')
		else:
			messages.success(request, 'La suppression de '+ nb_missions_supp +' missions a réussi.')

	if request.POST.get('delete'):
		m = Bdd_missions.objects.get(id = request.POST.get('id_mission'))
		m.delete()
		messages.success(request, 'La suppression de la mission réussie.')

	clients = Bdd_client.objects.all()
	adresses = Bdd_adresse_client.objects.all()
	consultants = Bdd_consultants.objects.all()
	missions = Bdd_missions.objects.all()

	nb_missions = missions.count()
	nb_missions_attribuer = Bdd_missions.objects.filter(status = "A").count()
	nb_missions_attente = Bdd_missions.objects.filter(status = "E").count()
	nb_missions_historique = Bdd_missions.objects.filter(status = "H").count()

	context = locals()
	template = "missions.html"
	return render(request,template,context)


@login_required
def edit_missions(request, id_mission):
	if not(request.user.groups.filter(name__in=["Admin"]).exists()):
		return HttpResponseRedirect('/login')
	else:
		admin = True

	clients = Bdd_client.objects.all()
	adresses = Bdd_adresse_client.objects.all()
	consultants = Bdd_consultants.objects.all()
	mission_selectionnee = Bdd_missions.objects.get(id = id_mission)

	if request.POST.get('edit'):
		mission_selectionnee.date_debut = request.POST.get('date-debut')
		mission_selectionnee.date_fin = request.POST.get('date-fin')
		mission_selectionnee.client = Bdd_client.objects.get(id = request.POST.get('client'))
		mission_selectionnee.adresse = Bdd_adresse_client.objects.get(id = request.POST.get('adresse'))
		if request.POST.get('visible') == 'oui':
			mission_selectionnee.visible_consultant = True
		else:
			mission_selectionnee.visible_consultant = False
		if request.POST.get('consultant') != "":
			mission_selectionnee.consultant = Bdd_consultants.objects.get(id = request.POST.get('consultant'))
			mission_selectionnee.status = "E"
		else:
			mission_selectionnee.consultant = None
			mission_selectionnee.status = "A"
		mission_selectionnee.save()
		messages.success(request, 'La mission a bien été modifiée.')
		return redirect(missions)

	context = locals()
	template = "edit_missions.html"
	return render(request,template,context)


@login_required
def add_missions(request):
	if not(request.user.groups.filter(name__in=["Admin"]).exists()):
		return HttpResponseRedirect('/login')
	else:
		admin = True

	clients = Bdd_client.objects.all()
	adresses = Bdd_adresse_client.objects.all()
	consultants = Bdd_consultants.objects.all()

	if request.POST.get('add'):
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
			m.consultant = None
			m.status = "A"
		m.save()
		messages.success(request, 'La mission a bien été ajoutée.')
		return redirect(missions)

	context = locals()
	template = "add_missions.html"
	return render(request,template,context)


##################
##### Clients #####
##################


@login_required
def clients(request):
	if not(request.user.groups.filter(name__in=["Admin"]).exists()):
		return HttpResponseRedirect('/login')
	else:
		admin = True

	if request.POST.get('action_client') == "supp_element":
		client_selectionne = request.POST.getlist('selection_clients')
		for id_client in client_selectionne:
			c = Bdd_client.objects.get(id = id_client)
			c.delete()
		nb_clients_supp = str(len(client_selectionne))
		if nb_clients_supp == '0':
			messages.warning(request, 'Des éléments doivent être sélectionnés afin d\'appliquer les actions. Aucun élément n\'a été modifié.')
		elif nb_clients_supp == '1':
			messages.success(request, 'La suppression d\'un client a réussi.')
		else:
			messages.success(request, 'La suppression de '+ nb_clients_supp +' clients a réussi.')

	if request.POST.get('delete'):
		c = Bdd_client.objects.get(id = request.POST.get('id_client'))
		c.delete()
		messages.success(request, 'La suppression du client a réussi.')

	if request.POST.get('action_adresse') == "supp_element":
		adresse_selectionnee = request.POST.getlist('selection_clients')
		for id_adresse in adresse_selectionnee:
			a = Bdd_adresse_client.objects.get(id = id_adresse)
			a.delete()
		nb_adresses_supp = str(len(adresse_selectionnee))
		if nb_adresses_supp == '0':
			messages.warning(request, 'Des éléments doivent être sélectionnés afin d\'appliquer les actions. Aucun élément n\'a été modifié.')
		elif nb_adresses_supp == '1':
			messages.success(request, 'La suppression d\'une adresse a réussi.')
		else:
			messages.success(request, 'La suppression de '+ nb_adresses_supp +' adresses a réussi.')

	if request.POST.get('delete_adresse'):
		a = Bdd_adresse_client.objects.get(id = request.POST.get('id_adresse'))
		a.delete()
		messages.success(request, 'La suppression de l\'adresse a réussi.')

	mission_types = Bdd_mission_type_client.objects.all()
	adresses = Bdd_adresse_client.objects.all()
	clients = Bdd_client.objects.all()

	nb_clients = clients.count()
	nb_clients_actifs = Bdd_client.objects.filter(archive = False).count()
	nb_clients_archives = Bdd_client.objects.filter(archive = True).count()
	nb_adresses = adresses.count()

	context = locals()
	template = "client.html"
	return render(request,template,context)


@login_required
def edit_clients(request, id_client):
	if not(request.user.groups.filter(name__in=["Admin"]).exists()):
		return HttpResponseRedirect('/login')
	else:
		admin = True

	mission_types = Bdd_mission_type_client.objects.all()
	adresses = Bdd_adresse_client.objects.all()
	client_selectionne = Bdd_client.objects.get(id = id_client)

	if request.POST.get('edit'):
		client_selectionne.nom = request.POST.get('nom')
		client_selectionne.code_couleur = request.POST.get('couleur')
		client_selectionne.mission_type.clear()
		client_selectionne.mission_type.add(Bdd_mission_type_client.objects.get(id = request.POST.get('type')))
		if request.POST.get('archive') == 'oui':
			client_selectionne.archive = True
		else:
			client_selectionne.archive = False
		client_selectionne.save()
		messages.success(request, 'Le client a bien été modifié.')
		return redirect(clients)

	context = locals()
	template = "edit_client.html"
	return render(request,template,context)


@login_required
def add_clients(request):
	if not(request.user.groups.filter(name__in=["Admin"]).exists()):
		return HttpResponseRedirect('/login')
	else:
		admin = True

	mission_types = Bdd_mission_type_client.objects.all()
	adresses = Bdd_adresse_client.objects.all()

	if request.POST.get('add'):
		c = Bdd_client()
		c.nom = request.POST.get('nom')
		c.code_couleur = request.POST.get('couleur')
		c.save()
		c.mission_type.add(Bdd_mission_type_client.objects.get(id = request.POST.get('type')))
		if request.POST.get('archive') == 'oui':
			c.archive = True
		else:
			c.archive = False
		c.save()
		messages.success(request, 'Le client a bien été ajouté.')
		return redirect(clients)

	context = locals()
	template = "add_client.html"
	return render(request,template,context)


#######################
##### Consultants #####
#######################


@login_required
def consultants(request):
	if not(request.user.groups.filter(name__in=["Admin"]).exists()):
		return HttpResponseRedirect('/login')
	else:
		admin = True

	if request.POST.get('action_consultant') == "supp_element":
		consultant_selectionne = request.POST.getlist('selection_consultants')
		for id_consultant in consultant_selectionne:
			c = Bdd_consultants.objects.get(id = id_consultant)
			c.delete()
		nb_consultants_supp = str(len(consultant_selectionne))
		if nb_consultants_supp == '0':
			messages.warning(request, 'Des éléments doivent être sélectionnés afin d\'appliquer les actions. Aucun élément n\'a été modifié.')
		elif nb_consultants_supp == '1':
			messages.success(request, 'La suppression d\'un consultant a réussi.')
		else:
			messages.success(request, 'La suppression de '+ nb_consultants_supp +' consultants a réussi.')

	if request.POST.get('delete'):
		c = Bdd_consultants.objects.get(id = request.POST.get('id_consultant'))
		c.delete()
		messages.success(request, 'La suppression du consultant a réussi.')

	user_django = User.objects.all()
	consultants = Bdd_consultants.objects.all()
	themes = Bdd_theme.objects.all()

	nb_consultants = consultants.count()
	nb_consultants_actif = Bdd_consultants.objects.filter(archive = False).count()
	nb_consultants_archive = Bdd_consultants.objects.filter(archive = True).count()

	context = locals()
	template = "consultant.html"
	return render(request,template,context)


@login_required
def edit_consultants(request, id_consultant):
	if not(request.user.groups.filter(name__in=["Admin"]).exists()):
		return HttpResponseRedirect('/login')
	else:
		admin = True

	user_django = User.objects.filter((Q(groups__name__in=['Consultant'])&Q(user_django__isnull=True))|Q(user_django__id = id_consultant))
	themes = Bdd_theme.objects.all()
	consultant_selectionne = Bdd_consultants.objects.get(id = id_consultant)

	if request.POST.get('edit'):
		consultant_selectionne.user_django = User.objects.get(username = request.POST.get('user'))
		consultant_selectionne.diminutif = consultant_selectionne.user_django.first_name[0]+consultant_selectionne.user_django.last_name[0]
		consultant_selectionne.telephone = request.POST.get('telephone')
		consultant_selectionne.adresse = request.POST.get('adresse')
		if request.POST.get('permission') == 'oui':
			consultant_selectionne.permission = True
		else:
			consultant_selectionne.permission = False
		if request.POST.get('archive') == 'oui':
			consultant_selectionne.archive = True
		else:
			consultant_selectionne.archive = False
		consultant_selectionne.theme_junior.clear()
		consultant_selectionne.theme_confirme.clear()
		consultant_selectionne.theme_senior.clear()
		consultant_selectionne.theme_junior.add(Bdd_theme.objects.get(id = request.POST.get('junior')))
		consultant_selectionne.theme_confirme.add(Bdd_theme.objects.get(id = request.POST.get('confirme')))
		consultant_selectionne.theme_senior.add(Bdd_theme.objects.get(id = request.POST.get('senior')))
		consultant_selectionne.save()
		messages.success(request, 'Le consultant a bien été modifié.')
		return redirect(consultants)

	context = locals()
	template = "edit_consultant.html"
	return render(request,template,context)


@login_required
def add_consultants(request):
	if not(request.user.groups.filter(name__in=["Admin"]).exists()):
		return HttpResponseRedirect('/login')
	else:
		admin = True

	user_django = User.objects.filter(Q(groups__name__in=['Consultant'])&Q(user_django__isnull=True))
	themes = Bdd_theme.objects.all()

	if request.POST.get('add'):
		c = Bdd_consultants()
		c.user_django = User.objects.get(username = request.POST.get('user'))
		c.diminutif = c.user_django.first_name[0]+c.user_django.last_name[0]
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
		messages.success(request, 'Le consultant a bien été ajouté.')
		return redirect(consultants)

	context = locals()
	template = "add_consultant.html"
	return render(request,template,context)