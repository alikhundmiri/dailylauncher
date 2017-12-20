from django.contrib import admin

# Register your models here.
from .models import group, linklist


class GroupAdmin(admin.ModelAdmin):
	list_display = ['user', 'group_name']
	list_filter = ['user', 'group_name']
	search_fields = ['user', 'group_name']
	filter_horizontal = ['website']

class LinkListAdmin(admin.ModelAdmin):
	list_display = ['user','title', 'link', 'visit_count']
	list_filter = ['user','title', 'link']
	search_fields = ['user','title', 'link', 'visit_count']


admin.site.register(group, GroupAdmin)
admin.site.register(linklist, LinkListAdmin)