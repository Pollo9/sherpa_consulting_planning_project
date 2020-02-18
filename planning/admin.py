from django.contrib import admin
from .models import *


class Bdd_consultantsAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','nom','prenom','diminutif','nom_de_compte','mdp', 'telephone','mail','adresse')

class Bdd_formateursAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','nom')

class Bdd_missionsAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','nom','description','formateur','date')



admin.site.register(Bdd_consultants,Bdd_consultantsAdmin)
admin.site.register(Bdd_formateurs,Bdd_formateursAdmin)
admin.site.register(Bdd_missions,Bdd_missionsAdmin)