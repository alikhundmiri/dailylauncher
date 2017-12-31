from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import datetime
from django.forms.formsets import formset_factory

from django.conf import settings

from .models import group, linklist
from .forms import NewGroupForm, NewLinkForm, BaseLinkFormSet

def price(request):
	dbug = settings.DEBUG

	context = {
		'dbug' : dbug,
	}
	return render(request, 'price.html', context)

def welcome(request):
	dbug = settings.DEBUG
	context = {
		'dbug' : dbug
	}
	return render(request, 'welcome.html', context)

def index(request):
	dbug = settings.DEBUG
	today = datetime.today()
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
		"today" : today,
		'dbug' : dbug,
	}
	return render(request, 'user_home.html', context)

@login_required
def card_create(request):
	dbug = settings.DEBUG

	if request.user.is_authenticated:
		pass
	else:
		raise Http404

	user = request.user
	new_group = group()

	# Create the formset, with specific form and formset we want.
	LinkFormSet = formset_factory(NewLinkForm, formset=BaseLinkFormSet, extra=4, min_num=1, max_num=5, validate_max=True, validate_min=True)

	if request.method == "POST":

		group_form = NewGroupForm(request.POST, user=user)
		link_formset = LinkFormSet(request.POST)

		if group_form.is_valid() and link_formset.is_valid():
			# save group info
			# new_group = group_form.save(commit=False)
			new_group.group_name = group_form.cleaned_data.get('group_name')
			new_group.user = user
			new_group.save()
			# now save the data for each form in formset
			gname = new_group.group_name
			new_links = []
			for link_form in link_formset:
				if link_form.is_valid():
					link = link_form.cleaned_data.get('link')
					title = link_form.cleaned_data.get('title')
					if title and link:
						model_instance = linklist(user=user, card=new_group)
						setattr(model_instance, 'link', link)
						setattr(model_instance, 'title', title)
						new_links.append(model_instance)						
			try:
				with transaction.atomic():
					# Replace the old with the new
					# linklist.objects.filter(title=title).delete()
					linklist.objects.bulk_create(new_links)
					# and notify our users that it worked
					messages.success(request, "You have updated your card")

			except IntegrityError: # if the transaction failed
				messages.error(request, 'There was an error saving your card')
			return HttpResponseRedirect("/")


	else:
		group_form = NewGroupForm(user=user)
		link_formset = LinkFormSet()

	context = {
		'group_form' : group_form,
		'link_formset' : link_formset,
		"nbar" : "New Card",
		'dbug' : dbug,
	}
	return render(request, 'general_form.html', context)

@login_required
def edit_card(request):
	'''
	Change the below one to suit the edit feature.
	This should go by id, fetch the card details, and verify is the requested user and id's user is same
	'''
	dbug = settings.DEBUG

	if request.user.is_authenticated:
		pass
	else:
		raise Http404

	user = request.user
	new_group = group()
	# Create the formset, with specifit form and formset we want.
	LinkFormSet = formset_factory(NewLinkForm, formset=BaseLinkFormSet)

	# getting our existing link data for this user, this will be used as initial data
	user_links = linklist.objects.filter(user=user).order_by('title')
	link_data = [{'link' : l.link, 'title' : l.title} for l in user_links]

	if request.method == "POST":
		group_form = NewGroupForm(request.POST, user=user)
		link_formset = NewLinkForm(request.POST)

		if group_form.is_valid() and link_formset.is_valid():
			# save group info
			# new_group = group_form.save(commit=False)
			new_group.group_name = group_form.cleaned_data.get('group_name')
			# group_form.save_m2m()
			new_group.user = user
			new_group.save()

			# now save the data for each form in formset
			new_links = []

			for link_form in link_formset:
				link = link_form.cleaned_data.get('link')
				title = link_form.cleaned_data.get('title')

				if title and link:
					new_links.append(linklist(user=user, title=title, link=link, card=new_group.group_name))

			try:
				with transaction.atomic():
					# Replace the old with the new
					linklist.objects.filter(title=title).delete()
					linklist.objects.bulk_create(new_links)

					# and notify our users that it worked
					messages.success(request, "You have updated your card")
			except IntegrityError: # if the transaction failed
				messages.error(request, 'There was an error saving your card')
				return HttpResponseRedirect("/")
			# new_group.save()
			# link_form.save_m2m()

	else:
		group_form = NewGroupForm(user=user)
		link_formset = LinkFormSet(initial=link_data)

	context = {
		'group_form' : group_form,
		'link_formset' : link_formset,
		"nbar" : "New Card",
		'dbug' : dbug,
	}
	return render(request, 'general_form.html', context)
	