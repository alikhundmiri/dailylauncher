# from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Count
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

def landing(request):
	dbug = settings.DEBUG
	context = {
		'dbug' : dbug
	}
	return render(request, 'landing.html', context)
	
def about(request):
	dbug = settings.DEBUG
	context = {
		'dbug' : dbug,
	}
	return render(request, 'about.html', context)


def index(request):
	dbug = settings.DEBUG
	today = datetime.today()
	if request.user.is_authenticated:
		pass
	else:
		return HttpResponseRedirect('/landing')

	created_groups = group.objects.filter(user=request.user).annotate(group__count=Count('card_content'))
	# the annotate will count the number of foreign keys connected to each of the item in this group.

	created_links = linklist.objects.filter(user=request.user)

	context = {
		"groups" : created_groups,
		'links' : created_links,
		"today" : today,
		'dbug' : dbug,
	}
	return render(request, 'core/user_home.html', context)

# create a new card
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
		'intro_text' : 'Create a new Card!',
		'button_text' : 'Create Card',
		'mid_level_text' : 'You can enter maximum 5 Links in a single card.',
	}
	return render(request, 'general_form.html', context)

# edit the card
@login_required
def card_edit(request, slug = None):
	
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
	# new_group = group()
	new_group = get_object_or_404(group, slug=slug)
	# print(new_group)
	# Create the formset, with specifit form and formset we want.
	LinkFormSet = formset_factory(NewLinkForm, formset=BaseLinkFormSet)

	# getting our existing link data for this user, this will be used as initial data
	user_links = linklist.objects.filter(card=new_group)

	link_data = [{'link' : l.link, 'title' : l.title} for l in user_links]
	group_data = {'user' : user, 'group_name' : new_group.group_name}
	if new_group.user == user:
		pass
	else:
		raise Http404


	if request.method == "POST":
		group_form = NewGroupForm(request.POST)
		link_formset = LinkFormSet(request.POST)

		if group_form.is_valid() and link_formset.is_valid():
			new_group.group_name = group_form.cleaned_data.get('group_name')
			new_group.user = user
			new_group.save()

			# now save the data for each form in formset
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
					# this will delete all the existing links associated with this card
					user_links.delete()
					# and save the new given ones in this form.
					linklist.objects.bulk_create(new_links)

					# and notify our users that it worked
					messages.success(request, "You have updated your card")
			except IntegrityError: # if the transaction failed
				messages.error(request, 'There was an error saving your card')
			return HttpResponseRedirect("/")
			# new_group.save()
			# link_form.save_m2m()

	else:
		group_form = NewGroupForm(initial=group_data)
		link_formset = LinkFormSet(initial=link_data)

	context = {
		'group_form' : group_form,
		'link_formset' : link_formset,
		"nbar" : "New Card",
		'dbug' : dbug,
		'intro_text' : 'Edit your card!',
		'button_text' : 'Save Changes',
		'mid_level_text' : 'You can enter maximum 5 Links in a single card.',		
	}
	return render(request, 'general_form.html', context)


# delete the card
@login_required
def card_delete(request, slug = None):

	user = request.user
	# new_group = group()
	select_card = get_object_or_404(group, slug=slug)

	if request.user.is_authenticated and select_card.user == user:
		select_card.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		raise Http404


	