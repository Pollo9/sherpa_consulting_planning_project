from django import forms
import datetime
from .models import *

# A LAISSER MEME SI ON UTILISE PAS LE FORM
class ajouter_missionForm(ModelForm):
	class Meta:
		model = Bdd_missions
		fields = ['consultant','client','adresse','visible_consultant']