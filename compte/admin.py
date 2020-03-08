from django.contrib import admin
from .models import *
class profileAdmin(admin.ModelAdmin):
	list_display = ('id',)

admin.site.register(profile,profileAdmin)
# Register your models here.
