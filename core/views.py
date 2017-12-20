from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect

from .models import group, linklist



def welcome(request):
	return render(request, 'welcome.html')

def index(request):
	if request.user.is_authenticated:
		# created_groups = get_object_or_404(group, user=request.user)
		created_groups = group.objects.filter(user=request.user)
	else:
		return HttpResponseRedirect('/welcome')

	# for g in created_groups.all():
		# print(g.group_name)
		# for l in g.website.all():
			# print("\t\t" + str(l))
		# print("\n")
	
	context = {
		"groups" : created_groups,
	}
	return render(request, 'user_home.html', context)
