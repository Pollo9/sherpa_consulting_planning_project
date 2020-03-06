from django import forms
import datetime
from .models import *



class DateInput(forms.DateInput):
	input_type = 'datetime-local'

class ajouter_missionForm(forms.Form):
	nom = forms.CharField(label='nom', max_length=100)
	description = forms.CharField(label='description', max_length=100)
	formateur = forms.CharField(label='formateur', max_length=100)
	date = forms.DateTimeField(initial=datetime.date.today, widget=DateInput)


