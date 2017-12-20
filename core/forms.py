from django import forms
from .models import group, linklist


class NewGroupForm(forms.ModelForm):
	website = forms.ModelMultipleChoiceField(queryset=linklist.objects.all())
	class Meta:
		model = group
		fields = [
			"group_name",
			"website"
		]
	def __init__(self, *args, **kwargs):
		# Only in case we build the form from an instance
		# (otherwise, 'toppings' list should be empty)
		if kwargs.get('instance'):
			# We get the 'initial' keyword argument or initialize it
			# as a dict if it didn't exist.                
			initial = kwargs.setdefault('initial', {})
			# The widget for a ModelMultipleChoiceField expects
			# a list of primary key for the selected data.
			initial['website'] = [t.pk for t in kwargs['instance'].topping_set.all()]

		forms.ModelForm.__init__(self, *args, **kwargs)

	# Overriding save allows us to process the value of 'toppings' field    
	def save(self, commit=True):
		# Get the unsave Pizza instance
		instance = forms.ModelForm.save(self, False)

		# Prepare a 'save_m2m' method for the form,
		old_save_m2m = self.save_m2m
		def save_m2m():
			old_save_m2m()
			# This is where we actually link the pizza with toppings
			instance.topping_set.clear()
			for topping in self.cleaned_data['website']:
				instance.topping_set.add(topping)
		self.save_m2m = save_m2m

		# Do we need to save all changes now?
		if commit:
			instance.save()
			self.save_m2m()

		return instance


class NewLinkForm(forms.ModelForm):
	class Meta:
		model = linklist
		fields = [
			"title",
			"link",
		]

# class NewLinkForm(forms.Form):
# 	title = forms.CharField(max_length=50)
# 	link = forms.CharField(max_length=100)

# class NewGroupForm(forms.Form):
# 	group_name = forms.CharField(max_length=50)
# 	website = forms.ModelMultipleChoiceField(queryset=linklist.objects.all())

