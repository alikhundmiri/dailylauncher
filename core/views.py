from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import datetime


from .models import group, linklist
from .forms import NewGroupForm, NewLinkForm


def welcome(request):
	return render(request, 'welcome.html')

def index(request):
	today = datetime.today()
	if request.user.is_authenticated:
		# created_groups = get_object_or_404(group, user=request.user)
		created_groups = group.objects.filter(user=request.user)
	else:
		return HttpResponseRedirect('/register')

	# for g in created_groups.all():
		# print(g.group_name)
		# for l in g.website.all():
			# print("\t\t" + str(l))
		# print("\n")
	
	context = {
		"groups" : created_groups,
		"today" : today,
	}
	return render(request, 'user_home.html', context)

@login_required
def card_create(request):
	if request.user.is_authenticated:
		pass
	else:
		raise Http404
	form = NewGroupForm(request.POST or None)
	inline = NewLinkForm(request.POST or None)
	if form.is_valid():
		if inline.is_valid():
			instance1 = inline.save(commit=False)
			instance1.save()
			inline.save_m2m()
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		form.save_m2m()
		# messages.success(request, "Successfully Created")
		# return HttpResponseRedirect(instance.get_absolute_url())
		return HttpResponseRedirect("/")
	context = {
		"form" : form,
	}
	return render(request, 'general_form.html', context)

