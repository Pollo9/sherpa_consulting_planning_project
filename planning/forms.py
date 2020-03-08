from django import forms
import datetime
from .models import *


class ajouter_missionForm(ModelForm):
	class Meta:
		model = Bdd_missions
		fields = ['consultant','client','adresse','visible_consultant']


