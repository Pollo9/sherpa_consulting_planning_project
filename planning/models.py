from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth.models import User


class Bdd_user_django(models.Model):

	id = models.AutoField(primary_key = True)
	nom_de_compte = models.CharField(default=' ',max_length=400)
	mdp = models.CharField(default=' ',max_length=400)
	mail = models.EmailField(max_length = 254)
	nom = models.CharField(default=' ',max_length=400)
	prenom = models.CharField(default=' ',max_length=400)
	
	class Meta:
		verbose_name = "User Django"
		ordering = ['id']
	
	def __str__(self):
		return self.nom_de_compte


class Bdd_theme(models.Model):

	id = models.AutoField(primary_key = True)
	nom = models.CharField(default=' ',max_length=400)
	
	class Meta:
		verbose_name = "Thème"
		ordering = ['id']
	
	def __str__(self):
		return self.nom


class Bdd_consultants(models.Model):

	id = models.AutoField(primary_key = True)
	diminutif = models.CharField(default=' ',max_length=400)
	telephone = models.CharField(default=' ',max_length=400)
	adresse = models.CharField(default=' ',max_length=400)
	permission = models.BooleanField(default=False)
	user_django = models.OneToOneField(Bdd_user_django, related_name='user_django', default='')
	theme_junior = models.ManyToManyField(Bdd_theme, related_name='theme_junior')
	theme_confirme = models.ManyToManyField(Bdd_theme, related_name='theme_confirme')
	theme_senior = models.ManyToManyField(Bdd_theme, related_name='theme_senior')
	
	class Meta:
		verbose_name = "Consultant"
		ordering = ['id']
	
	def __str__(self):
		return self.user_django.nom


class Bdd_piece_jointe_client(models.Model):

	id = models.AutoField(primary_key = True)
	nom = models.CharField(default=' ',max_length=400)
	document = models.FileField()
	date_upload = models.DateField(default=timezone.now)
	client = models.ForeignKey('Bdd_client')
	
	class Meta:
		verbose_name = "Pièce Jointe Client"
		ordering = ['id']
	
	def __str__(self):
		return self.nom


class Bdd_mission_type_client(models.Model):

	id = models.AutoField(primary_key = True)
	nom = models.CharField(default=' ',max_length=400)
	theme = models.ManyToManyField(Bdd_theme)
	piece_jointe = models.ManyToManyField(Bdd_piece_jointe_client,blank=True)
	
	class Meta:
		verbose_name = "Mission Type Client"
		ordering = ['id']
	
	def __str__(self):
		return self.nom


class Bdd_client(models.Model):

	id = models.AutoField(primary_key = True)
	nom = models.CharField(default=' ',max_length=400)
	code_couleur = models.CharField(default=' ',max_length=400)
	mission_type = models.ManyToManyField(Bdd_mission_type_client)
	
	class Meta:
		verbose_name = "Client"
		ordering = ['id']
	
	def __str__(self):
		return self.nom


class Bdd_adresse_client(models.Model):

	id = models.AutoField(primary_key = True)
	nom = models.CharField(default=' ',max_length=400)
	adresse = models.CharField(default=' ',max_length=400)
	code_postal = models.CharField(default=' ',max_length=400)
	ville = models.CharField(default=' ',max_length=400)
	client = models.ForeignKey('Bdd_client')
	
	class Meta:
		verbose_name = "Adresse Client"
		ordering = ['id']
	
	def __str__(self):
		return self.nom


class Bdd_missions(models.Model):

	STATUS_CHOICES = [
		("A", "En Attente"),
		("C", "En Cours"),
		("T", "Terminée"),
	]

	id = models.AutoField(primary_key = True)
	date_debut = models.CharField(default='',max_length=400)
	date_fin = models.CharField(default='',max_length=400)
	consultant = models.ForeignKey('Bdd_consultants', default='')
	client = models.ForeignKey('Bdd_client', default='')
	adresse = models.ForeignKey('Bdd_adresse_client', default='')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='')
	visible_consultant = models.BooleanField(default='')
	
	class Meta:
		verbose_name = "Mission"
		ordering = ['id']
	
	def __str__(self):
		return self.client.nom+' ('+self.status+')'


class Bdd_messages(models.Model):

	id = models.AutoField(primary_key = True)
	envoyeur = models.ForeignKey('Bdd_user_django', related_name='envoyeur')
	receveur = models.ForeignKey('Bdd_user_django', related_name='receveur')
	message = models.TextField()
	date = models.DateTimeField(default=timezone.now, verbose_name="Date d'envoi")
	lu = models.BooleanField(default = False)
	
	class Meta:
		verbose_name = "Message"
		ordering = ['date']
	
	def __str__(self):
		return self.message