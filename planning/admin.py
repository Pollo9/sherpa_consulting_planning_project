from django.contrib import admin
from .models import *


class Bdd_userDjangoAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','nom_de_compte','mdp','mail','nom','prenom')

class Bdd_consultantsAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','diminutif','telephone','adresse', 'permission','user_django')

class Bdd_themeAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','nom')

class Bdd_pieceJointeClientAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','nom','document','date_upload','client')

class Bdd_missionTypeClientAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','nom')

class Bdd_clientAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','nom','code_couleur')

class Bdd_adresseClientAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','nom','adresse','code_postal','ville','client')

class Bdd_missionsAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','date_debut','date_fin','consultant','client','adresse','status','visible_consultant')

class Bdd_messagesAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','envoyeur','receveur','message','date','lu')

class Bdd_formateursAdmin(admin.ModelAdmin):
	search_fields = ['titre']
	list_display = ('id','nom')


admin.site.register(Bdd_user_django,Bdd_userDjangoAdmin)
admin.site.register(Bdd_consultants,Bdd_consultantsAdmin)
admin.site.register(Bdd_theme,Bdd_themeAdmin)
admin.site.register(Bdd_piece_jointe_client,Bdd_pieceJointeClientAdmin)
admin.site.register(Bdd_mission_type_client,Bdd_missionTypeClientAdmin)
admin.site.register(Bdd_client,Bdd_clientAdmin)
admin.site.register(Bdd_adresse_client,Bdd_adresseClientAdmin)
admin.site.register(Bdd_missions,Bdd_missionsAdmin)
admin.site.register(Bdd_messages,Bdd_messagesAdmin)
admin.site.register(Bdd_formateurs,Bdd_formateursAdmin)