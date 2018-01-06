from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_domainonly_email(value):
	"""
	Let's validate the email passed is in the domain "yourdomain.com"
	"""
	if not "yourdomain.com" in value:
		raise ValidationError(_"Sorry, the email submitted is invalid. All emails have to be registered on this domain only.", status='invalid')


def url_validator(value):
	regex = re.compile(
		# r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	
