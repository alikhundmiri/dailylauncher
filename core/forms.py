from django import forms
from django.forms.formsets import BaseFormSet
from django.core.validators import URLValidator

from .models import group, linklist


# FORM FOR INDIVIDUAL LINKS
class NewLinkForm(forms.Form):
	title  = forms.CharField(
					max_length=50,
					widget=forms.TextInput(attrs={
							'placeholder' : 'Example: Github'
						}), 
					required=False)

	link = forms.CharField(
					max_length=100,
					widget=forms.TextInput(attrs={
							'placeholder' : 'Example: Https://www.github.com'
						}),
					required=False,
					)
	protocol = forms.ChoiceField(choices=linklist.WEB_PROTOCOL, required=False)

# FORM FOR NEW CARD, WHICH WILL BE USED TO NEST THE ABOVE FORM
class NewGroupForm(forms.Form):

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)

		super(NewGroupForm, self).__init__(*args, **kwargs)

		self.fields['group_name'] = forms.CharField(
										max_length=50,
							widget=forms.TextInput(attrs={
							'placeholder' : 'Example: Work Mode or Netflix & chill.',
						}))

		# I am not declaring field 'user' because I think 
		# it will be saved by itself. as declared in models

class BaseLinkFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        anchors = []
        urls = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                anchor = form.cleaned_data['title']
                url = form.cleaned_data['link']

                # Check that no two links have the same anchor or URL
                if anchor and url:
                    if anchor in anchors:
                        duplicates = True
                    anchors.append(anchor)

                    if url in urls:
                        duplicates = True
                    urls.append(url)

                if duplicates:
                    raise forms.ValidationError(
                        'Links must have unique Names and URLs.',
                        code='duplicate_links'
                    )

                # Check that all links have both an anchor and URL
                if url and not anchor:
                    raise forms.ValidationError(
                        'All links must have an anchor.',
                        code='missing_anchor'
                    )
                elif anchor and not url:
                    raise forms.ValidationError(
                        'All links must have a URL.',
                        code='missing_URL'
                    )
