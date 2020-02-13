from django.contrib import admin
from .models import *


class Bdd_consultantsAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','nom','prenom','diminutif','nom_de_compte','mdp', 'telephone','mail','adresse')


admin.site.register(Bdd_consultants,Bdd_consultantsAdmin)
