from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError, transaction
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import datetime
from django.forms.formsets import formset_factory

from django.conf import settings
from django.contrib.auth.models import User 
from core.models import group, linklist
from core.forms import NewGroupForm, NewLinkForm, BaseLinkFormSet

# for average
from statistics import mean 

from collections import Counter

# dashboard for users
@login_required
def index(request):
	if request.user.is_authenticated:
		pass
	else:
		raise Http404

	# total cards
	_cards = group.objects.filter(user=request.user)
	total_cards = _cards.count()

	# total links
	_links = linklist.objects.filter(user=request.user)
	total_links = _links.count()

	cards_quantity = []
	links_quantity = []
	linkspercard = _cards.annotate(links__count=Count('card_content'))


	# average links per card
	for links in linkspercard:
		links_quantity.append(links.links__count)

	avg_links_per_card = round(mean(links_quantity))

	# common Link name 
	link_name = []
	for link in _links:
		link_name.append(link.title)
	avg_link_name = Counter(link_name)
	# print(link_name)
	# print("total_cards: " + str(total_cards))
	# print("total_links: " + str(total_links))
	# print("avg_links_per_card: " + str(avg_links_per_card))


	context = {
		'total_cards' : total_cards,
		'total_links' : total_links,
		'avg_links_per_card': avg_links_per_card,
	}
	return render(request, 'dashboard/userdash.html', context)

# dashboard for superusers
"""
	number of signups, DONE
	number of cards created, DONE
	number of links created, DONE
	number of links per card > find average, DONE
	number of cards per user > find average, DONW
	common link
	common card name
"""

@user_passes_test(lambda u: u.is_authenticated)
def superdash(request):
	if request.user.is_authenticated:
		pass
	else:
		raise Http404
	# total users 
	_user = User.objects.all()
	total_user = _user.count()

	# total cards
	_cards = group.objects.all()
	total_cards = _cards.count()

	# total links
	_links = linklist.objects.all()
	total_links = _links.count()

	cards_quantity = []
	links_quantity = []
	linkspercard = _cards.annotate(links__count=Count('card_content'))

	# average card per user
	for cards in _cards:
		cards_quantity.append(cards.user.username)

	card_counts_per_user = round(mean(Counter(cards_quantity).values()))

	# average links per card
	for links in linkspercard:
		links_quantity.append(links.links__count)

	avg_links_per_card = round(mean(links_quantity))

	# common Link name 
	link_name = []
	for link in _links:
		link_name.append(link.title)
	avg_link_name = Counter(link_name)
	# print(link_name)
	# print("total_user: " + str(total_user))
	# print("total_cards: " + str(total_cards))
	# print("total_links: " + str(total_links))
	# print("card_counts_per_user: " + str(card_counts_per_user))
	# print("avg_links_per_card: " + str(avg_links_per_card))


	context = {
		'total_user' : total_user,
		'total_cards' : total_cards,
		'total_links' : total_links,
		'card_counts_per_user': card_counts_per_user,
		'avg_links_per_card': avg_links_per_card,
	}
	return render(request, "dashboard/superdash.html" ,context)

def version(request):
	context = {

	}
	return render(request, 'dashboard/version_detail.html', context)

def version_detail(request, id=None):
	context = {

	}
	return render(request, 'dashboard/version_history.html', context)