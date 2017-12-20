from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
import random

def suggest_group():
	groups = ['Netflix and Chill','Amazon window Shopping','Social Networking''Social Life','Work mode', 'Apple News','Rabbit Hole','random Creeps of internet']

	return(random.choice(groups))

class group(models.Model):
	user			=		models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	slug			=		models.SlugField(unique=True)
	group_name		=		models.CharField(max_length=50, blank=False, null=False, default=suggest_group())
	website			=		models.ManyToManyField('linklist')

	timestamp		=		models.DateTimeField(auto_now=False, auto_now_add=True)
	updated			=		models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return(self.user.username)

	class Meta:
		ordering 	=		["-timestamp", "-updated"]



class linklist(models.Model):
	user 			=		models.ForeignKey(settings.AUTH_USER_MODEL, default=1,on_delete=models.CASCADE)
	title			=		models.CharField(max_length=50, blank=False, null=False)
	link 			=		models.CharField(max_length=100, blank=False, null=False)
	visit_count		=		models.IntegerField(default=0)
	timestamp		=		models.DateTimeField(auto_now=False, auto_now_add=True)
	updated			=		models.DateTimeField(auto_now=True, auto_now_add=False)
	def __str__(self):
		return(self.link)

	class Meta:
		ordering	=		["-timestamp", "-updated"]



def slug_for_group(instance, new_slug=None):
	slug = slugify(instance.group_name)
	if new_slug is not None:
		slug = new_slug
	qs = group.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		# print("slug: " + str(slug))
		a = slug.split('-')
		# print("a: " + str(a[0]))
		new_slug = "%s-%s" %(a[0], qs.first().id)
		# print("new_slug: " + str(new_slug))
		# new_slug = "%s-%s" %(slug, qs.first().id)
		return slug_for_group(instance, new_slug=new_slug)
	return slug

def pre_save_group(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slug_for_group(instance)

pre_save.connect(pre_save_group, sender=group)