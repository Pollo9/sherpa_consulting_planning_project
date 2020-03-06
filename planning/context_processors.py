from planning.models import Bdd_messages

def notif_total(request):
	msg = Bdd_messages.objects.all()
	notif_total = 0
	for m in msg:
		if not m.lu:
			notif_total += 1
	return {"notif_total": notif_total}