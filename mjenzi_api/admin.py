from django.contrib import admin

from .models import Project, Materials, Requests, Reports

admin.site.register(Project)
admin.site.register()
admin.site.register(Reports)
admin.site.register(Requests)
