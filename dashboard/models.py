from django.db import models

# Create your models here.
class version_entry(models.Model):
	version_no			=		models.CharField(max_length=5, default="v0.0.1", blank=False, null=False)
	version_name		=		models.CharField(max_length=1000, default="New update", blank=False, null=False)
	version_detail		=		models.TextField(max_length=10000, default="Bugs Fixed, and improvements implemented.", blank=False, null=False)

	timestamp			=		models.DateTimeField(auto_now=False, auto_now_add=True)
	updated				=		models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return(self.version_name + str(" - ") + self.version_no)

	def get_absolute_url(self):
		return reverse("user:home", kwargs={"id" : self.id})

	class Meta:
		ordering 	=		["-timestamp", "-updated"]


