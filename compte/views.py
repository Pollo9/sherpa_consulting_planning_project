from django.shortcuts import render

def login(request):
	context = locals()
	template = "account/login.html"
	return render(request,template,context)
