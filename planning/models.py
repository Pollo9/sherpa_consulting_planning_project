from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth.models import User



class Bdd_consultants(models.Model):

	id = models.AutoField(primary_key = True)
	nom = models.CharField(default=' ',max_length=400)
	prenom = models.CharField(default=' ',max_length=400)
	diminutif = models.CharField(default=' ',max_length=400)
	nom_de_compte = models.CharField(default=' ',max_length=400)
	mdp = models.CharField(default=' ',max_length=400)
	telephone = models.CharField(default=' ',max_length=400)
	mail = models.EmailField(max_length = 254) 
	adresse = models.CharField(default=' ',max_length=400)
	
	class Meta:
		verbose_name = "Consultant"
		ordering = ['id']
	
	def __str__(self):
		return self.nom


class Bdd_messages(models.Model):

	id = models.AutoField(primary_key = True)
	envoyeur = models.ForeignKey('Bdd_consultants', related_name='envoyeur')
	receveur = models.ForeignKey('Bdd_consultants', related_name='receveur')
	message = models.TextField()
	date = models.DateTimeField(default=timezone.now, verbose_name="Date d'envoi")
	lu = models.BooleanField(default = False)
	
	class Meta:
		verbose_name = "Message"
		ordering = ['date']
	
	def __str__(self):
		return self.message



class Bdd_formateurs(models.Model):

	id = models.AutoField(primary_key = True)
	nom = models.CharField(default=' ',max_length=400)
	
	
	class Meta:
		verbose_name = "Formateur"
		ordering = ['id']
	
	def __str__(self):
		return self.nom

class Bdd_missions(models.Model):

	id = models.AutoField(primary_key = True)
	nom = models.CharField(default=' ',max_length=400)
	description = models.CharField(default=' ',max_length=400)
	formateur = models.CharField(default=' ',max_length=400)
	date = models.DateField(default=' ',max_length=400)
	
	
	class Meta:
		verbose_name = "Mission"
		ordering = ['id']
	
	def __str__(self):
		return self.nom

